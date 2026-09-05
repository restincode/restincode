#!/usr/bin/env python3
"""Validate memorial data files.

Checks people/*.json against schema/person.schema.json and enforces the
cross-file conventions the site relies on:

  - every peoplelist.json entry points at an existing people/<filename>.json
  - every people/*.json (except _template.json) is listed exactly once
  - filenames are lowercase alphanumeric
  - local image paths exist under images/
  - link fields are http(s) URLs with no surrounding whitespace
  - text-only fields contain no HTML (maintext is the one HTML field)

people/_template.json is scaffolding with intentional blanks and is skipped.

Errors exit non-zero. Warnings are printed but do not fail the run.

Usage: scripts/validate_people.py [--root DIR]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema

FILENAME_RE = re.compile(r"^[a-z0-9]+$")
HTTP_RE = re.compile(r"^https?://\S+$")
HTML_RE = re.compile(r"<[a-zA-Z/!]|&[a-zA-Z#][a-zA-Z0-9]*;")
# Filenames that predate the lowercase-alphanumeric rule. Renaming them would
# change public memorial URLs, so they are allowed as-is. Do not add to this
# list for new entries.
LEGACY_FILENAMES = {"karenKrystalia", "obsèquesdepaolo"}

TEXT_FIELDS = ("firstname", "lastname", "handle", "affiliations", "birth", "death")

PEOPLELIST_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["people"],
    "properties": {
        "people": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["displayname", "filename"],
                "properties": {
                    "displayname": {"type": "string", "minLength": 1},
                    "filename": {"type": "string"},
                },
            },
        }
    },
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def load_json(path: Path, report: Report):
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        report.error(f"{path.parent.name}/{path.name}", f"cannot parse JSON: {exc}")
        return None


def check_schema(path: Path, data, validator: jsonschema.Validator, report: Report) -> None:
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
        report.error(str(path), f"schema: {loc}: {err.message}")


def check_text(where: str, field: str, value, report: Report) -> None:
    if isinstance(value, str) and HTML_RE.search(value):
        report.error(where, f"{field}: HTML is not allowed in this field: {value!r}")


def check_link(where: str, field: str, value, report: Report) -> None:
    if not isinstance(value, str) or value == "":
        return
    if value != value.strip():
        report.error(where, f"{field}: URL has surrounding whitespace: {value!r}")
    elif not HTTP_RE.match(value):
        report.error(where, f"{field}: not an http(s) URL: {value!r}")


def check_image(where: str, field: str, value, root: Path, report: Report) -> None:
    if not isinstance(value, str) or value == "":
        return
    if value.startswith("/images/"):
        if not (root / value.lstrip("/")).is_file():
            report.error(where, f"{field}: image not found: {value}")
    else:
        check_link(where, field, value, report)


def check_person(path: Path, data: dict, root: Path, report: Report) -> None:
    where = str(path.relative_to(root))

    for field in TEXT_FIELDS:
        check_text(where, field, data.get(field), report)

    check_link(where, "obituary", data.get("obituary"), report)
    check_image(where, "mainimage", data.get("mainimage"), root, report)

    for i, item in enumerate(data.get("socialmedialinks") or []):
        check_text(where, f"socialmedialinks[{i}].sitename", item.get("sitename"), report)
        check_link(where, f"socialmedialinks[{i}].siteurl", item.get("siteurl"), report)

    for i, item in enumerate(data.get("references") or []):
        check_text(where, f"references[{i}].title", item.get("title"), report)
        check_link(where, f"references[{i}].url", item.get("url"), report)

    for i, item in enumerate(data.get("contributions") or []):
        check_text(where, f"contributions[{i}].title", item.get("title"), report)
        check_text(where, f"contributions[{i}].description", item.get("description"), report)
        check_link(where, f"contributions[{i}].url", item.get("url"), report)

    for i, item in enumerate(data.get("gallery") or []):
        check_text(where, f"gallery[{i}].title", item.get("title"), report)
        check_text(where, f"gallery[{i}].caption", item.get("caption"), report)
        check_image(where, f"gallery[{i}].url", item.get("url"), root, report)
        if not item.get("title"):
            report.warn(where, f"gallery[{i}]: no title (used as the image alt text)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root: Path = args.root
    report = Report()

    schema = load_json(root / "schema" / "person.schema.json", report)
    if schema is None:
        return finish(report)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    person_validator = validator_cls(schema)
    list_validator = jsonschema.Draft202012Validator(PEOPLELIST_SCHEMA)

    people_dir = root / "people"
    files = {p.stem: p for p in sorted(people_dir.glob("*.json")) if p.stem != "_template"}

    peoplelist_path = root / "peoplelist.json"
    peoplelist = load_json(peoplelist_path, report)
    listed: dict[str, int] = {}
    if peoplelist is not None:
        check_schema(peoplelist_path.relative_to(root), peoplelist, list_validator, report)
        for entry in peoplelist.get("people", []):
            name = entry.get("filename", "")
            if name == "":
                continue  # intentional no-link card
            listed[name] = listed.get(name, 0) + 1
            if name not in files:
                report.error("peoplelist.json", f"'{name}' has no people/{name}.json")
        for name, count in listed.items():
            if count > 1:
                report.error("peoplelist.json", f"'{name}' is listed {count} times")

    for stem, path in files.items():
        where = str(path.relative_to(root))
        if stem not in listed:
            report.error(where, "not listed in peoplelist.json")
        if not FILENAME_RE.match(stem) and stem not in LEGACY_FILENAMES:
            report.error(where, "filename must be lowercase alphanumeric (a-z, 0-9)")
        data = load_json(path, report)
        if data is None:
            continue
        check_schema(path.relative_to(root), data, person_validator, report)
        if isinstance(data, dict):
            check_person(path, data, root, report)

    print(f"checked {len(files)} memorial files, {len(listed)} peoplelist entries")
    return finish(report)


def finish(report: Report) -> int:
    for msg in report.warnings:
        print(f"WARNING: {msg}")
    for msg in report.errors:
        print(f"ERROR: {msg}")
    print(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
