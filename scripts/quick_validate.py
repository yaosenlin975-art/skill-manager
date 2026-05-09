#!/usr/bin/env python3
"""
Quick validation script for CoPaw skills
Validates SKILL.md frontmatter against copaw-architecture schema
"""

import sys
import re
import yaml
from pathlib import Path

# CoPaw v1.1.0 defined frontmatter fields
REQUIRED_PROPERTIES = {'name', 'description', 'metadata'}
ALLOWED_PROPERTIES = REQUIRED_PROPERTIES | {'author', 'license'}


def validate_skill(skill_path):
    """Validate a CoPaw skill directory"""
    skill_path = Path(skill_path)

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter (must start with ---)"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"

    # Check required fields
    missing = REQUIRED_PROPERTIES - set(frontmatter.keys())
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    # Check unexpected top-level fields
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        return False, f"Unexpected fields: {', '.join(sorted(unexpected))}. Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"

    # Validate name
    name = frontmatter.get('name', '')
    if not isinstance(name, str) or not re.match(r'^[a-z0-9-]+$', name.strip()):
        return False, f"Name must be kebab-case (lowercase letters, digits, hyphens): '{name}'"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' has invalid hyphens"
    if len(name) > 64:
        return False, f"Name too long ({len(name)}/64)"

    # Validate description
    desc = frontmatter.get('description', '')
    if not isinstance(desc, str):
        return False, "description must be a string"
    if len(desc) > 1024:
        return False, f"description too long ({len(desc)}/1024)"

    return True, "Valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_dir>")
        sys.exit(1)
    valid, msg = validate_skill(sys.argv[1])
    print(msg)
    sys.exit(0 if valid else 1)
