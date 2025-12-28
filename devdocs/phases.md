# Implementation Phases

## Phase 1: Core Automation Script

**Goal:** Build the foundation for issue processing and data extraction

**Tasks:**

1. Create `scripts/process_issues.py` main script
2. Implement GitHub Issue fetcher using gh CLI or GitHub API
3. Build issue template parser (handle markdown format)
4. Implement filename normalization function
5. Create data extraction logic for all person fields
6. Build JSON generator from template
7. Add basic logging

**Deliverables:**

- Script can fetch and parse issues
- Can generate person data structure from issue
- Can create memorial JSON file

**Validation:**

- Process 2-3 sample issues in dry-run mode
- Verify JSON output matches template schema
- Check filename normalization works correctly

**Estimated Effort:** 2-4 hours

---

## Phase 2: Image and URL Processing

**Goal:** Handle image downloads and URL archiving

**Tasks:**

1. Implement image downloader (from URLs and GitHub attachments)
2. Add image processing (resize, optimize)
3. Create image filename matching logic
4. Implement URL archiver (archive.org API)
5. Add fallback to default silhouette for missing images
6. Handle various image formats (jpg, png, gif)

**Deliverables:**

- Images downloaded and saved correctly
- Image filenames match person filenames
- URLs archived (or logged if archiving fails)

**Validation:**

- Download images from GitHub issue attachments
- Test with various image URLs
- Verify archive.org integration works

**Estimated Effort:** 2-3 hours

---

## Phase 3: Site Integration

**Goal:** Update site files and validate changes

**Tasks:**

1. Implement peoplelist.json updater
2. Add alphabetical sorting logic
3. Build filename consistency validator
4. Create local Jekyll build tester
5. Implement memorial page HTTP test
6. Add link validator (check all URLs return 200)

**Deliverables:**

- peoplelist.json updates correctly
- All filenames match across files
- Local testing validates changes

**Validation:**

- Run Jekyll build without errors
- Access memorial page at localhost:4000
- Verify all images and links work

**Estimated Effort:** 2-3 hours

---

## Phase 4: Git and GitHub Automation

**Goal:** Automate PR creation and issue updates

**Tasks:**

1. Implement git branch creation
2. Add commit logic with proper message format
3. Build PR creation using gh CLI
4. Implement issue label updater
5. Add PR description generator (link to issue, summarize changes)
6. Create PR template population

**Deliverables:**

- Automatic branch creation per person
- Commits with proper format (no emojis!)
- PRs created and linked to issues
- Issue labels updated

**Validation:**

- Create test PR for one person
- Verify PR description is complete
- Check issue label changed correctly
- Ensure commit message follows guidelines

**Estimated Effort:** 2-3 hours

---

## Phase 5: Batch Processing and Error Handling

**Goal:** Process multiple issues reliably

**Tasks:**

1. Create priority queue system
2. Implement progress tracker (save state)
3. Add resume capability from last processed issue
4. Build error handler (log failures, continue processing)
5. Create dry-run mode for testing
6. Add concurrent processing (5-10 at a time)
7. Generate summary report after batch

**Deliverables:**

- Can process issues in batches
- Progress tracked and resumable
- Errors logged but don't stop processing
- Summary report of successes/failures

**Validation:**

- Process 5 issues in dry-run mode
- Simulate failure and test resume
- Verify progress tracking works

**Estimated Effort:** 2-3 hours

---

## Phase 6: High-Priority Execution

**Goal:** Process high-profile individuals

**Tasks:**

1. Review and refine high-priority list
2. Run dry-run on top 3 people
3. Manual review of generated files
4. Execute live processing for high-priority issues
5. Monitor PRs and address failures
6. Update progress tracker

**Deliverables:**

- 10-15 high-profile memorials created
- PRs submitted and merged
- Any issues documented

**Validation:**

- All PRs pass pre-commit hooks
- Memorials display correctly on site
- No broken links or images

**Estimated Effort:** 3-5 hours (includes monitoring)

---

## Phase 7: Full Backlog Processing

**Goal:** Clear remaining backlog

**Tasks:**

1. Process remaining "Add Person" issues
2. Process "Add Data" issues (update existing memorials)
3. Handle edge cases and failures manually
4. Generate final summary report
5. Update documentation with lessons learned

**Deliverables:**

- All 42 "Add Person" issues processed
- All 14 "Add Data" issues processed
- Backlog cleared

**Validation:**

- All PRs created
- Issue labels updated
- Site builds without errors

**Estimated Effort:** Variable (depends on failures)

---

## Phase 8: Cleanup and Documentation

**Goal:** Finalize automation system for future use

**Tasks:**

1. Refactor code for maintainability
2. Add comprehensive comments
3. Create README for scripts/
4. Document common failure modes and fixes
5. Create usage guide for future issues
6. Archive automation logs

**Deliverables:**

- Clean, documented codebase
- Usage documentation
- Automation can be run again for new issues

**Validation:**

- Code passes linting
- Documentation is clear
- Another person could run the automation

**Estimated Effort:** 2-3 hours

---

## Total Estimated Effort

**Development:** 15-20 hours
**Execution & Monitoring:** 5-10 hours
**Total:** 20-30 hours

## Success Criteria

- All 42 "Add Person" issues processed
- Individual PRs created for each person
- All memorials tested and validated
- Site builds and deploys successfully
- Issue labels updated appropriately
- Automation system documented for future use
