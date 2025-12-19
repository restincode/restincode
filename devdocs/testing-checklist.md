# Testing Checklist

Before creating a PR for each memorial, validate the following:

## File Structure Validation

- [ ] JSON file created in `people/{filename}.json`
- [ ] Entry added to `peoplelist.json`
- [ ] Image saved in `images/{filename}.{ext}` (or default silhouette used)
- [ ] All filenames match exactly (case-sensitive check)

## JSON Validation

- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] All required fields present: `firstname` OR `lastname` OR `handle`, `death`, `issue`
- [ ] `maintext` wrapped in `<p>` tags
- [ ] No emojis in any field
- [ ] Arrays properly formatted (socialmedialinks, contributions, gallery)
- [ ] No empty string values in required fields

## Filename Consistency

- [ ] JSON filename matches entry in peoplelist.json `filename` field
- [ ] Image filename matches (without extension)
- [ ] Filename is lowercase
- [ ] No spaces in filename
- [ ] Special characters handled appropriately
- [ ] Filename unique (not duplicate of existing)

## Image Validation

- [ ] Main image exists at path specified in `mainimage`
- [ ] Image is web-optimized (under 500KB ideally)
- [ ] Image dimensions reasonable (not massive)
- [ ] Gallery images all exist if specified
- [ ] No broken image links

## URL Validation

- [ ] All social media URLs are valid and accessible
- [ ] Contribution URLs work (return 200 status)
- [ ] Obituary URL valid if provided
- [ ] Gallery image URLs accessible
- [ ] All URLs use HTTPS (or HTTP if HTTPS unavailable)

## Content Quality

- [ ] Biography (`maintext`) is coherent and respectful
- [ ] No placeholder text like "lorem ipsum"
- [ ] Handles/nicknames formatted consistently
- [ ] Birth/death years in expected format (YYYY or empty)
- [ ] Affiliations make sense

## Local Build Test

- [ ] `bundle exec jekyll build` completes without errors
- [ ] No warnings about missing images
- [ ] No JSON parsing errors
- [ ] Site builds successfully

## Memorial Page Test

- [ ] Memorial accessible at `http://localhost:4000/memorial.html?name={filename}`
- [ ] Page loads without 404
- [ ] Main image displays correctly
- [ ] Biography displays without HTML errors
- [ ] Social media links render
- [ ] Contributions section displays
- [ ] Gallery images load (if present)

## Homepage Integration Test

- [ ] Person appears on homepage at `http://localhost:4000/`
- [ ] Display name correct
- [ ] Sortable by name
- [ ] Clicking entry navigates to memorial page

## Pre-commit Hook Test

- [ ] Run prettier on all modified files
- [ ] Ensure no trailing whitespace
- [ ] Ensure files end with newline
- [ ] Verify not committing to main branch directly

## Git Validation

- [ ] Branch name follows pattern: `add-person-{issue-number}-{filename}`
- [ ] Commit message follows format (no emojis)
- [ ] Only modified files: person JSON, peoplelist.json, image file(s)
- [ ] No unrelated changes included

## PR Validation

- [ ] PR title: "Add {displayname} memorial"
- [ ] PR description includes:
  - Link to original issue
  - Summary of person
  - Note about image source
  - Checklist of files changed
- [ ] PR links to issue via "Closes #XXX" or "Addresses #XXX"
- [ ] Labels appropriate (if any)

## Issue Update Validation

- [ ] Issue label changed from "Add Person" to "Person Added"
- [ ] Issue remains open (never close person issues)
- [ ] Comment added to issue linking to PR

## Archive Validation (if implemented)

- [ ] All URLs submitted to archive.org or archive.today
- [ ] Archive URLs stored or logged
- [ ] Archival failures logged for manual follow-up

## Error Cases to Test

- [ ] Missing image (should use default silhouette)
- [ ] Minimal data (name + death year only)
- [ ] Special characters in name
- [ ] Very long biography (should truncate gracefully)
- [ ] Duplicate filename attempt (should handle)
- [ ] Invalid URLs (should skip or log error)

## Automation-Specific Checks

- [ ] Processing logged to `logs/processing.log`
- [ ] Success/failure status recorded
- [ ] Can resume from this point if process interrupted
- [ ] Dry-run mode produces expected output without modifying files

## Sample Test Cases

### Test Case 1: Well-Documented Person (Dan Kaminsky)

- All fields populated
- Multiple images
- Many contributions
- Extensive social media

### Test Case 2: Minimal Data Person (AP Delchi)

- Basic name
- Death year
- No image
- No biography

### Test Case 3: Special Characters (Ozzie "Cheshire Catalyst" Osband)

- Nickname in quotes
- Special characters
- Handle extraction

## Final Validation

Before submitting PR:

- [ ] All checklist items above pass
- [ ] Manual review of generated memorial page
- [ ] Spot check for respectfulness and accuracy
- [ ] Verify this is a person (not spam/test issue)
- [ ] Confirm person meets site criteria (hacker/infosec professional)
