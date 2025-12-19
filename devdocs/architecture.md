# System Architecture

## Overview

The automated memorial processing system is designed to:

1. Extract data from GitHub Issues
2. Generate memorial JSON files
3. Download and process images
4. Update peoplelist.json
5. Test memorials locally
6. Create PRs automatically

## Component Design

### 1. Issue Fetcher and Parser

**Location:** `scripts/process_issues.py`

**Responsibilities:**

- Query GitHub API for issues with "Add Person" or "Add Data" labels
- Parse issue templates to extract structured data
- Parse issue comments for additional context
- Handle various issue formats (some well-structured, some freeform)

**Key Functions:**

- `fetch_issues(label)` - Get all issues with specified label
- `parse_issue_template(issue_body)` - Extract fields from template
- `parse_comments(comments)` - Extract additional data from comments
- `prioritize_issues(issues, high_priority_list)` - Sort by priority

### 2. Data Processor

**Responsibilities:**

- Normalize person names to valid filenames
- Extract and validate all required/optional fields
- Generate placeholder text for missing biography
- Build complete person data structure

**Key Functions:**

- `normalize_filename(name)` - Convert name to valid filename (lowercase, no spaces, handle special chars)
- `extract_person_data(issue)` - Build person data dict from issue
- `generate_biography(person_data)` - Create bio text from available info
- `validate_data(person_data)` - Ensure minimum requirements met

**Filename Normalization Rules:**

- Convert to lowercase
- Remove/replace special characters
- Handle parenthetical nicknames (extract handle)
- Ensure uniqueness across existing files

### 3. Image Processor

**Responsibilities:**

- Download images from URLs or GitHub attachments
- Resize/optimize for web display
- Save with normalized filename
- Handle missing images (use default silhouette)

**Key Functions:**

- `download_image(url, filename)` - Fetch and save image
- `process_image(image_path)` - Resize/optimize
- `extract_github_attachment(issue)` - Get embedded images

### 4. URL Archiver

**Responsibilities:**

- Archive all URLs to archive.org and/or archive.today
- Store archive URLs in memorial data
- Handle archival failures gracefully

**Key Functions:**

- `archive_url(url)` - Submit to archive services
- `get_archived_url(url)` - Retrieve existing archive if available

### 5. Memorial Generator

**Responsibilities:**

- Create JSON file from template
- Update peoplelist.json with new entry (maintain alphabetical sort)
- Ensure all filenames match across files

**Key Functions:**

- `generate_memorial_json(person_data, issue_number)` - Create JSON file
- `update_peoplelist(displayname, filename)` - Add entry and sort
- `validate_filename_consistency(person)` - Check filename matches everywhere

### 6. Local Tester

**Responsibilities:**

- Run Jekyll build to verify no syntax errors
- Test memorial page loads correctly
- Validate image links work
- Check for broken URLs

**Key Functions:**

- `build_site()` - Run `bundle exec jekyll build`
- `test_memorial_page(filename)` - HTTP request to localhost:4000
- `validate_links(memorial_data)` - Check all URLs return 200

### 7. Git/GitHub Automator

**Responsibilities:**

- Create feature branches
- Commit changes with proper message format
- Push to remote
- Create PR via gh CLI
- Update issue labels
- Link PR to original issue

**Key Functions:**

- `create_branch(issue_number, person_name)` - Create and checkout branch
- `commit_changes(person_name, issue_number)` - Git commit with standard message
- `create_pr(branch_name, person_data, issue_number)` - Open PR via gh CLI
- `update_issue_labels(issue_number)` - Change "Add Person" to "Person Added"

## Data Flow

```
GitHub Issue
    ↓
Issue Fetcher/Parser → Person Data Structure
    ↓
Data Processor → Normalized/Validated Data
    ↓
Image Processor → Downloaded Images
    ↓
URL Archiver → Archived URLs
    ↓
Memorial Generator → JSON Files + peoplelist.json update
    ↓
Local Tester → Validation (pass/fail)
    ↓
Git/GitHub Automator → Branch + Commit + PR + Label Update
```

## Error Handling

- Log all operations to `logs/processing.log`
- On failure, save state to `progress-tracker.md`
- Allow resume from last successful operation
- Create failed issues list for manual review

## Configuration

**Config File:** `scripts/config.yaml`

```yaml
github:
  repo: restincode/restincode
  token: ${GITHUB_TOKEN}

archive:
  archive_org_enabled: true
  archive_today_enabled: true

processing:
  dry_run: false
  max_concurrent: 5

priorities:
  high_profile_people:
    - Kevin David Mitnick
    - Dan Kaminsky
    - Kris Nova
    - Adrian Lamo
    - Bram Moolenaar
```

## Dependencies

- Python 3.8+
- requests (HTTP requests)
- Pillow (image processing)
- PyYAML (config parsing)
- gh CLI (GitHub operations)
- Jekyll (testing)
