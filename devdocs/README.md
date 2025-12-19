# RestInCode Issue Processing Automation

This directory contains documentation and tooling for automating the processing of GitHub Issues to create memorial entries on the RestInCode site.

## Project Overview

**Goal:** Automate the processing of 42+ "Add Person" and 14+ "Add Data" GitHub Issues to create memorial JSON files, update the site, and submit PRs.

**Approach:** Fully automated system that processes issues autonomously, creates individual PRs per person, and handles minimal data gracefully.

**Priority:** Focus on high-profile individuals first (Dan Kaminsky, Kris Nova, Kevin Mitnick, Adrian Lamo, Bram Moolenaar, etc.)

## Documentation Structure

- `architecture.md` - System architecture and design decisions
- `phases.md` - Implementation phases and milestones
- `data-mapping.md` - How GitHub Issue data maps to JSON schema
- `testing-checklist.md` - Testing requirements before PR creation
- `high-priority-list.md` - List of high-profile individuals to process first
- `progress-tracker.md` - Track which issues have been processed

## Current Status

**Phase:** Planning and documentation
**Issues to Process:** 42 Add Person, 14 Add Data
**Completed:** 0
**In Progress:** 0

## Quick Start

See `phases.md` for implementation roadmap.
