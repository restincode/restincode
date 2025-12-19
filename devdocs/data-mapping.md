# Data Mapping: GitHub Issue → Memorial JSON

This document describes how data from GitHub Issues maps to the memorial JSON schema.

## Issue Template Structure

Standard "Add Person" issue template:

```markdown
**General Info**

- First name: {firstname}
- Last name: {lastname}
- Handle: {handle}
- Birth Year: {birth}
- Death Year: {death}
- Link to Obituary: {obituary_url}
- Group Affiliations: {affiliations}
- URL to main photo (or attach to Issue): {image_url}
- Description of person and/or activities: {bio}
- Facebook memorial group URL: {memorial_url}

**Social Media Links**

- Twitter: {twitter_url}
- Github: {github_url}
- LinkedIn: {linkedin_url}
- Facebook: {facebook_url}
- Other: {other_url}

**Contributions**

- Project name: {project_name}
- Project URL: {project_url}
- Project Description: {project_desc}

**Photo Gallery**

- URL(s) to additional photos: {gallery_urls}
```

## Memorial JSON Schema

Target structure (from `people/_template.json`):

```json
{
  "firstname": "",
  "lastname": "",
  "handle": "",
  "birth": "",
  "death": "",
  "obituary": "",
  "issue": "",
  "affiliations": "",
  "mainimage": "/images/{filename}.{ext}",
  "maintext": "<p>Biography in HTML</p>",
  "socialmedialinks": [
    { "sitename": "Twitter", "siteurl": "https://..." },
    { "sitename": "Github", "siteurl": "https://..." }
  ],
  "contributions": [{ "title": "", "url": "", "description": "" }],
  "gallery": [{ "url": "/images/{filename}.{ext}", "title": "", "caption": "" }]
}
```

## Field Mappings

### Direct Mappings

| Issue Field        | JSON Field     | Notes                                            |
| ------------------ | -------------- | ------------------------------------------------ |
| First name         | `firstname`    | Trim whitespace                                  |
| Last name          | `lastname`     | Trim whitespace                                  |
| Handle             | `handle`       | Remove @ if present                              |
| Birth Year         | `birth`        | Accept various formats (YYYY, "Nov 4 1986", etc) |
| Death Year         | `death`        | Accept various formats                           |
| Link to Obituary   | `obituary`     | Validate URL                                     |
| Group Affiliations | `affiliations` | Comma-separated list                             |
| Issue number       | `issue`        | String of issue number                           |

### Computed Mappings

| Computed Value  | Target Field                  | Logic                                                                      |
| --------------- | ----------------------------- | -------------------------------------------------------------------------- |
| Display name    | Used in peoplelist.json       | `{firstname} {lastname}` or `{firstname} {lastname} ({handle})`            |
| Filename        | JSON filename, image filename | Normalize: lowercase, remove spaces/special chars, use handle if ambiguous |
| Main image path | `mainimage`                   | `/images/{normalized_filename}.{ext}` or default silhouette                |

### Complex Mappings

#### Biography (`maintext`)

**Sources (in order of preference):**

1. "Description of person and/or activities" field from issue
2. First paragraph from Wikipedia link (if provided)
3. Constructed from obituary excerpt
4. Minimal placeholder: "Information security professional and {affiliations} member."

**Processing:**

- Wrap in `<p>` tags
- Preserve line breaks as separate paragraphs
- Convert markdown links to HTML
- Strip emojis
- Maximum 500 words (truncate if longer)

#### Social Media Links (`socialmedialinks`)

**Logic:**

- Only include entries with non-empty URLs
- Standardize site names: "Twitter", "Github", "LinkedIn", "Facebook", "Website", "Other"
- Accept variations: Twitter/X, Github/GitHub
- Validate URLs (must start with http:// or https://)

**Example:**

```json
[
  { "sitename": "Twitter", "siteurl": "https://twitter.com/username" },
  { "sitename": "Github", "siteurl": "https://github.com/username" }
]
```

#### Contributions (`contributions`)

**Sources:**

1. Explicit contributions from issue template
2. Links from issue comments
3. Wikipedia "Known for" section

**Logic:**

- Parse multiple contribution blocks from issue
- Extract project name, URL, description
- Generate description from URL if not provided (e.g., "GitHub repository for {project}")
- Limit to top 5 most significant

#### Gallery (`gallery`)

**Sources:**

1. Photo Gallery URLs from issue
2. Embedded images in issue body
3. Images from issue comments
4. GitHub attachment URLs

**Logic:**

- Download and save each image
- Generate title: "Photo of {firstname} {lastname}"
- Generate caption: "{firstname} at {event}" (if context available) or generic
- First gallery image can also be mainimage if no main photo specified

## Special Cases

### Minimal Data Issues

If issue contains only:

- Name (first/last or handle)
- Death year

Generate:

- Filename from name
- Placeholder bio
- Default silhouette image
- Issue number for reference

### Duplicate Filenames

If normalized filename already exists:

1. Append handle if available
2. Append middle initial if available
3. Append birth/death year
4. Append incremental number as last resort

### Missing Images

If no image URL provided:

- Use default: `/images/face-silhouette-clipart.png`
- Log for manual follow-up

### URL Variations

Handle common URL issues:

- Twitter → X domain changes
- HTTP vs HTTPS
- Trailing slashes
- Mobile URLs (m.twitter.com → twitter.com)

## Validation Rules

Before generating JSON, validate:

1. At least firstname OR lastname OR handle present
2. Death year present (required field)
3. Issue number valid
4. All URLs well-formed
5. Image URLs accessible (or fallback to default)
6. Filename unique in people/ directory
7. Filename matches across all files

## Example Mapping

**Issue #169: Dan Kaminsky**

```
First name: Dan
Last name: Kaminsky
Death Year: 2021 (Apr 23)
Twitter: https://twitter.com/dakami
Wikipedia: https://en.wikipedia.org/wiki/Dan_Kaminsky
```

**Generated:**

```json
{
  "firstname": "Dan",
  "lastname": "Kaminsky",
  "handle": "",
  "birth": "",
  "death": "2021",
  "obituary": "",
  "issue": "169",
  "affiliations": "",
  "mainimage": "/images/dankaminsky.jpg",
  "maintext": "<p>Dan Kaminsky was a prominent security researcher...</p>",
  "socialmedialinks": [
    {"sitename": "Twitter", "siteurl": "https://twitter.com/dakami"},
    {"sitename": "Wikipedia", "siteurl": "https://en.wikipedia.org/wiki/Dan_Kaminsky"}
  ],
  "contributions": [...],
  "gallery": [...]
}
```

**Filename:** `dankaminsky.json`
**peoplelist.json entry:** `{"displayname": "Dan Kaminsky", "filename": "dankaminsky"}`
