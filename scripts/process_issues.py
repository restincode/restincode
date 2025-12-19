#!/usr/bin/env python3
"""
RestInCode Issue Processing Automation

Processes GitHub Issues to create memorial JSON files and submit PRs.
"""

import os
import sys
import json
import re
import logging
import subprocess
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class IssueProcessor:
    """Main class for processing GitHub Issues into memorial entries."""

    def __init__(self, config_path: str = "scripts/config.yaml"):
        """Initialize the processor with configuration."""
        self.load_config(config_path)
        self.setup_logging()
        self.repo_root = Path.cwd()

    def load_config(self, config_path: str):
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        """Configure logging to file and console."""
        log_dir = Path(self.config['paths']['logs_dir'])
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Issue Processor initialized")

    def fetch_issues(self, label: str) -> List[Dict]:
        """
        Fetch issues from GitHub using gh CLI.

        Args:
            label: Issue label to filter by ('Add Person' or 'Add Data')

        Returns:
            List of issue dictionaries
        """
        self.logger.info(f"Fetching issues with label: {label}")

        cmd = [
            'gh', 'issue', 'list',
            '--repo', self.config['github']['repo'],
            '--label', label,
            '--limit', '100',
            '--json', 'number,title,body,author,comments,labels,url',
            '--state', 'open'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issues = json.loads(result.stdout)
            self.logger.info(f"Fetched {len(issues)} issues with label '{label}'")
            return issues
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to fetch issues: {e}")
            return []

    def fetch_issue_details(self, issue_number: int) -> Optional[Dict]:
        """
        Fetch detailed issue information including comments.

        Args:
            issue_number: GitHub issue number

        Returns:
            Issue dictionary with full details
        """
        self.logger.info(f"Fetching details for issue #{issue_number}")

        cmd = [
            'gh', 'issue', 'view', str(issue_number),
            '--repo', self.config['github']['repo'],
            '--json', 'number,title,body,author,comments,labels,url'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue = json.loads(result.stdout)
            return issue
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to fetch issue #{issue_number}: {e}")
            return None

    def parse_issue_template(self, issue_body: str) -> Dict[str, str]:
        """
        Parse issue template to extract structured data.

        Args:
            issue_body: Raw markdown body of the issue

        Returns:
            Dictionary of extracted fields
        """
        data = {}

        if not issue_body:
            return data

        # Define field patterns to extract (handle both - and * bullets)
        # Use [^\n\r]+ to match everything except newlines
        patterns = {
            'firstname': r'[*-]\s*First name:\s*([^\n\r]+)',
            'lastname': r'[*-]\s*Last name:\s*([^\n\r]+)',
            'handle': r'[*-]\s*Handle:\s*([^\n\r]+)',
            'birth': r'[*-]\s*Birth Year:\s*([^\n\r]+)',
            'death': r'[*-]\s*Death Year:\s*([^\n\r]+)',
            'obituary': r'[*-]\s*Link to Obituary:\s*([^\n\r]+)',
            'affiliations': r'[*-]\s*Group Affiliations:\s*([^\n\r]+)',
            'mainimage_url': r'[*-]\s*URL to main photo[^:]*:\s*([^\n\r]+)',
            'description': r'[*-]\s*Description of person[^:]*:\s*([^\n\r]+)',
            'twitter': r'[*-]\s*Twitter:\s*([^\n\r]+)',
            'github': r'[*-]\s*Github:\s*([^\n\r]+)',
            'linkedin': r'[*-]\s*LinkedIn:\s*([^\n\r]+)',
            'facebook': r'[*-]\s*Facebook:\s*([^\n\r]+)',
            'wikipedia': r'[*-]\s*Wikipedia:\s*([^\n\r]+)',
            'other_url': r'[*-]\s*Other:\s*([^\n\r]+)',
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, issue_body, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Clean up empty values and values that are just bullets
                if value and value not in ['', 'N/A', 'n/a', 'None', 'none'] and not value.startswith('*') and not value.startswith('-'):
                    data[field] = value

        # Extract contributions (can be multiple)
        contributions = []
        contrib_pattern = r'[*-]\s*Project name:\s*(.+?)[\n\r]+[*-]\s*Project URL:\s*(.+?)[\n\r]+[*-]\s*Project Description:\s*(.+?)(?=\n[*-]|\n\*\*|$)'
        for match in re.finditer(contrib_pattern, issue_body, re.IGNORECASE | re.DOTALL):
            title = match.group(1).strip()
            url = match.group(2).strip()
            desc = match.group(3).strip()
            if title and title not in ['', '[project name]']:
                contributions.append({'title': title, 'url': url, 'description': desc})
        if contributions:
            data['contributions'] = contributions

        # Extract gallery URLs
        gallery_match = re.search(r'\*\*Photo Gallery\*\*.*?URL\(s\).*?:(.+?)(?=\n\*\*|$)', issue_body, re.IGNORECASE | re.DOTALL)
        if gallery_match:
            gallery_text = gallery_match.group(1)
            # Find all URLs in the gallery section
            url_pattern = r'https?://[^\s\)]+(?:\.jpg|\.jpeg|\.png|\.gif)?'
            gallery_urls = re.findall(url_pattern, gallery_text, re.IGNORECASE)
            if gallery_urls:
                data['gallery_urls'] = gallery_urls

        return data

    def normalize_filename(self, name: str, handle: str = None) -> str:
        """
        Convert a person's name to a normalized filename.

        Args:
            name: Person's full name
            handle: Optional handle/nickname

        Returns:
            Normalized filename (lowercase, no spaces, no special chars)
        """
        # Use handle if provided and seems better
        if handle:
            # Remove @ symbol if present
            handle = handle.lstrip('@')
            # If handle is simple (no spaces), prefer it
            if ' ' not in handle:
                base = handle
            else:
                base = name
        else:
            base = name

        # Remove parenthetical nicknames
        base = re.sub(r'\([^)]*\)', '', base).strip()

        # Convert to lowercase
        base = base.lower()

        # Remove special characters, keep only alphanumeric
        base = re.sub(r'[^a-z0-9]+', '', base)

        return base

    def extract_person_data(self, issue: Dict) -> Dict:
        """
        Extract and structure person data from issue.

        Args:
            issue: GitHub issue dictionary

        Returns:
            Structured person data dictionary
        """
        self.logger.info(f"Extracting data from issue #{issue['number']}: {issue['title']}")

        # Parse the issue body
        parsed_data = self.parse_issue_template(issue.get('body', ''))

        # Also check comments for additional data
        for comment in issue.get('comments', []):
            comment_data = self.parse_issue_template(comment.get('body', ''))
            # Merge comment data (don't overwrite existing)
            for key, value in comment_data.items():
                if key not in parsed_data:
                    parsed_data[key] = value

        # Build person data structure
        person = {
            'issue_number': issue['number'],
            'issue_url': issue['url'],
            'firstname': parsed_data.get('firstname', ''),
            'lastname': parsed_data.get('lastname', ''),
            'handle': parsed_data.get('handle', ''),
            'birth': parsed_data.get('birth', ''),
            'death': parsed_data.get('death', ''),
            'obituary': parsed_data.get('obituary', ''),
            'affiliations': parsed_data.get('affiliations', ''),
            'description': parsed_data.get('description', ''),
            'mainimage_url': parsed_data.get('mainimage_url', ''),
            'socialmedialinks': [],
            'contributions': parsed_data.get('contributions', []),
            'gallery_urls': parsed_data.get('gallery_urls', []),
        }

        # Build social media links
        social_mapping = {
            'Twitter': 'twitter',
            'Github': 'github',
            'LinkedIn': 'linkedin',
            'Facebook': 'facebook',
            'Wikipedia': 'wikipedia',
            'Website': 'other_url',
        }

        for sitename, field in social_mapping.items():
            url = parsed_data.get(field, '')
            if url and url.startswith('http'):
                person['socialmedialinks'].append({'sitename': sitename, 'siteurl': url})

        # Generate display name
        if person['firstname'] and person['lastname']:
            displayname = f"{person['firstname']} {person['lastname']}"
        elif person['firstname']:
            displayname = person['firstname']
        elif person['lastname']:
            displayname = person['lastname']
        elif person['handle']:
            displayname = person['handle']
        else:
            # Fall back to issue title
            displayname = issue['title']

        # Add handle to display name if present
        if person['handle'] and person['handle'] not in displayname:
            displayname = f"{displayname} ({person['handle']})"

        person['displayname'] = displayname

        # Generate filename
        name_for_file = f"{person['firstname']} {person['lastname']}".strip()
        if not name_for_file:
            name_for_file = person['handle'] or displayname
        person['filename'] = self.normalize_filename(name_for_file, person['handle'])

        return person

    def generate_biography(self, person: Dict) -> str:
        """
        Generate HTML biography from person data.

        Args:
            person: Person data dictionary

        Returns:
            HTML biography string
        """
        bio = person.get('description', '')

        if not bio:
            # Generate placeholder bio
            name = person.get('firstname', person.get('handle', 'This individual'))
            affiliation = person.get('affiliations', '')
            if affiliation:
                bio = f"{name} was an information security professional and {affiliation} member."
            else:
                bio = f"{name} was an information security professional."

        # Wrap in paragraph tags
        if not bio.startswith('<p>'):
            bio = f"<p>{bio}</p>"

        return bio

    def generate_memorial_json(self, person: Dict) -> Dict:
        """
        Generate memorial JSON structure from person data.

        Args:
            person: Person data dictionary

        Returns:
            Complete memorial JSON dictionary
        """
        self.logger.info(f"Generating memorial JSON for {person['displayname']}")

        # Read template
        template_path = self.repo_root / self.config['paths']['template']
        with open(template_path, 'r') as f:
            memorial = json.load(f)

        # Populate fields
        memorial['firstname'] = person['firstname']
        memorial['lastname'] = person['lastname']
        memorial['handle'] = person['handle']
        memorial['birth'] = person['birth']
        memorial['death'] = person['death']
        memorial['obituary'] = person.get('obituary', '')
        memorial['issue'] = str(person['issue_number'])
        memorial['affiliations'] = person.get('affiliations', '')
        memorial['maintext'] = self.generate_biography(person)

        # Social media links (only non-empty)
        memorial['socialmedialinks'] = [
            link for link in person['socialmedialinks']
            if link.get('siteurl')
        ]

        # Contributions (only non-empty)
        memorial['contributions'] = [
            contrib for contrib in person.get('contributions', [])
            if contrib.get('title')
        ]

        # Main image - will be set during image processing
        # For now, use default if no URL provided
        if person.get('mainimage_url'):
            memorial['mainimage'] = f"/images/{person['filename']}.jpg"
        else:
            memorial['mainimage'] = "/images/face-silhouette-clipart.png"

        # Gallery - will be populated during image processing
        memorial['gallery'] = []

        return memorial

    def save_memorial_json(self, person: Dict, memorial: Dict, dry_run: bool = False) -> bool:
        """
        Save memorial JSON to file.

        Args:
            person: Person data dictionary
            memorial: Memorial JSON dictionary
            dry_run: If True, don't actually write file

        Returns:
            True if successful
        """
        filename = person['filename']
        json_path = self.repo_root / self.config['paths']['people_dir'] / f"{filename}.json"

        if dry_run:
            self.logger.info(f"[DRY RUN] Would save memorial JSON to: {json_path}")
            self.logger.info(f"[DRY RUN] Content: {json.dumps(memorial, indent=2)}")
            return True

        try:
            with open(json_path, 'w') as f:
                json.dump(memorial, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Ensure file ends with newline
            self.logger.info(f"Saved memorial JSON to: {json_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save memorial JSON: {e}")
            return False

    def prioritize_issues(self, issues: List[Dict]) -> List[Dict]:
        """
        Sort issues by priority (high-profile people first).

        Args:
            issues: List of issue dictionaries

        Returns:
            Sorted list of issues
        """
        high_profile = self.config['priorities']['high_profile']

        def get_priority(issue):
            title = issue['title']
            # Check if any high-profile name is in the title
            for idx, name in enumerate(high_profile):
                if name.lower() in title.lower():
                    return idx  # Lower number = higher priority
            return 999  # Low priority

        sorted_issues = sorted(issues, key=get_priority)

        self.logger.info(f"Prioritized {len(sorted_issues)} issues")
        for i, issue in enumerate(sorted_issues[:5]):
            self.logger.info(f"  Priority {i+1}: #{issue['number']} - {issue['title']}")

        return sorted_issues

    def process_issue(self, issue_number: int, dry_run: bool = False) -> bool:
        """
        Process a single issue end-to-end.

        Args:
            issue_number: GitHub issue number
            dry_run: If True, don't make any file changes

        Returns:
            True if successful
        """
        self.logger.info(f"{'[DRY RUN] ' if dry_run else ''}Processing issue #{issue_number}")

        # Fetch issue details
        issue = self.fetch_issue_details(issue_number)
        if not issue:
            return False

        # Extract person data
        person = self.extract_person_data(issue)

        # Validate minimum requirements
        if not person['filename']:
            self.logger.error(f"Cannot generate filename for issue #{issue_number}")
            return False
        if not person['death']:
            self.logger.warning(f"No death year for issue #{issue_number}")

        # Generate memorial JSON
        memorial = self.generate_memorial_json(person)

        # Save memorial JSON
        success = self.save_memorial_json(person, memorial, dry_run=dry_run)

        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Process RestInCode GitHub Issues to create memorials',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--issue', type=int, help='Process specific issue number')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Run without making any file changes (DEFAULT)')
    parser.add_argument('--live', action='store_true',
                        help='Actually create files (disables dry-run)')
    args = parser.parse_args()

    # Determine if this is a dry run
    dry_run = not args.live

    processor = IssueProcessor()

    # Show mode clearly
    mode = "DRY RUN MODE - NO CHANGES WILL BE MADE" if dry_run else "LIVE MODE - WILL CREATE FILES"
    processor.logger.info("=" * 60)
    processor.logger.info(f"MODE: {mode}")
    processor.logger.info("=" * 60)

    if not dry_run:
        processor.logger.warning("LIVE mode enabled - files will be created!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            processor.logger.info("Aborted by user")
            return 0

    # Default to test issue if none specified
    test_issue = args.issue or 197
    processor.logger.info(f"Processing issue #{test_issue}")

    success = processor.process_issue(test_issue, dry_run=dry_run)

    if success:
        processor.logger.info("Processing completed successfully")
    else:
        processor.logger.error("Processing failed")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
