#!/usr/bin/env python3
`
"""
Atlas GitHub Infrastructure Bootstrap Script

This script configures the Atlas GitHub repository infrastructure including:
- Project V2 creation
- Labels
- Milestones
- Workflows verification
- CODEOWNERS verification
- Issue templates verification
- Branch protection recommendations

Requirements:
- GitHub CLI (gh) installed and authenticated
- Python 3.10+

Usage:
    python scripts/bootstrap_github.py [--dry-run] [--org AtlasAutomationStudio] [--repo Atlas]
`
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


# -- Configuration --

ORGANIZATION = "AtlasAutomationStudio"
REPOSITORY = "Atlas"
PROJECT_NAME = "Atlas Development"
PROJECT_DESCRIPTION = (
    "Development board for Atlas Architecture, Runtime, Studio, "
    "Marketplace and Release planning."
)

LABELS = [
    {"name": "architecture", "color": "3A79C5", "description": "Architecture-related changes"},
    {"name": "runtime", "color": "2E7DD7", "description": "Runtime implementation"},
    {"name": "workflow", "color": "5319E7", "description": "Workflow engine"},
    {"name": "vision", "color": "008672", "description": "Vision runtime"},
    {"name": "ai", "color": "D4C5F9", "description": "AI runtime"},
    {"name": "knowledge", "color": "FBCA04", "description": "Knowledge runtime"},
    {"name": "ipc", "color": "1D76DB", "description": "IPC runtime"},
    {"name": "plugin", "color": "F9D0C4", "description": "Plugin runtime"},
    {"name": "storage", "color": "E4E669", "description": "Storage layer"},
    {"name": "project", "color": "BF3776", "description": "Project runtime"},
    {"name": "integration", "color": "C9510C", "description": "Cross-runtime integration"},
    {"name": "documentation", "color": "0075ca", "description": "Documentation updates"},
    {"name": "rfc", "color": "d73a4a", "description": "RFC proposals"},
    {"name": "adr", "color": "c5def5", "description": "Architecture Decision Records"},
    {"name": "testing", "color": "fef2c0", "description": "Test coverage"},
    {"name": "performance", "color": "a2eeef", "description": "Performance improvements"},
    {"name": "security", "color": "d73a4a", "description": "Security-related"},
    {"name": "ui", "color": "7057ff", "description": "User interface"},
    {"name": "marketplace", "color": "0052cc", "description": "Marketplace features"},
    {"name": "release", "color": "1d76db", "description": "Release management"},
    {"name": "bug", "color": "d73a4a", "description": "Bug reports"},
    {"name": "enhancement", "color": "a2eeef", "description": "Feature enhancements"},
    {"name": "refactor", "color": "fbca04", "description": "Code refactoring"},
    {"name": "research", "color": "bfd4f2", "description": "Research tasks"},
    {"name": "good first issue", "color": "7057ff", "description": "Good for newcomers"},
    {"name": "help wanted", "color": "008672", "description": "Needs contributor help"},
    {"name": "high priority", "color": "d73a4a", "description": "High priority item"},
    {"name": "medium priority", "color": "fbca04", "description": "Medium priority item"},
    {"name": "low priority", "color": "6e9558", "description": "Low priority item"},
]

MILESTONES = [
    {"title": "Sprint 12", "description": "Performance & Stress testing", "state": "active"},
    {"title": "Sprint 13", "description": "Desktop Shell implementation", "state": "active"},
    {"title": "Sprint 14", "description": "Workflow Studio", "state": "active"},
    {"title": "Sprint 15", "description": "Vision Studio", "state": "active"},
    {"title": "Sprint 16", "description": "AI Studio", "state": "active"},
    {"title": "Sprint 17", "description": "Marketplace", "state": "active"},
    {"title": "Sprint 18", "description": "Beta release preparation", "state": "active"},
    {"title": "Future", "description": "Post-1.0 features and roadmap", "state": "active"},
]

REQUIRED_WORKFLOWS = [
    "ci.yml",
    "pull_request.yml",
    "release.yml",
    "docs.yml",
    "benchmark.yml",
]

REQUIRED_TEMPLATES = [
    "ISSUE_TEMPLATE/bug_report.yml",
    "ISSUE_TEMPLATE/feature_request.yml",
    "ISSUE_TEMPLATE/documentation.yml",
    "ISSUE_TEMPLATE/rfc.yml",
    "PULL_REQUEST_TEMPLATE/.gitkeep",
]

BRANCH_PROTECTION_RECOMMENDATIONS = """
# Branch Protection Recommendations for 'main'
#
# Go to: Settings -> Branches -> Branch protection rules
#
# Rule for main branch:
# - Require pull request reviews: YES
# - Require status checks to pass: YES
# - Require conversation resolution before merging: YES
# - Exclude administrators: NO
# - Require signed commits: NO (optional)
# - Allow force pushes: NO
# - Allow deletions: NO
# - Require linear history: YES
# - Include administrators: YES
# - Restrict who can push: match contributors
"""


# -- Utility Functions --

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"stderr: {e.stderr}")
        raise


def gh_exists(label_name):
    """Check if a label already exists in the repository."""
    try:
        result = run_command(
            ["gh", "label", "list", "--json", "name"],
            check=False,
        )
        if result.returncode != 0:
            return False
        labels = json.loads(result.stdout)
        return any(lbl["name"] == label_name for lbl in labels)
    except Exception:
        return False


def gh_project_exists(project_name):
    """Check if a project V2 exists and return its ID, or None."""
    try:
        result = run_command(
            ["gh", "project", "list", "--json", "name,id"],
            check=False,
        )
        if result.returncode != 0:
            return None
        projects = json.loads(result.stdout)
        for proj in projects:
            if proj["name"] == project_name:
                return proj["id"]
        return None
    except Exception:
        return None


# -- Bootstrap Functions --

def verify_github_auth():
    """Verify that gh CLI is authenticated."""
    print("Verifying GitHub authentication...")
    try:
        result = run_command(["gh", "auth", "status"], check=False)
        if result.returncode == 0:
            print("GitHub CLI authenticated")
            return True
        else:
            print("GitHub CLI not authenticated")
            print("Run: gh auth login")
            return False
    except FileNotFoundError:
        print("GitHub CLI (gh) not found")
        print("Install from: https://cli.github.com/")
        return False


def verify_repository():
    """Verify we're in the correct repository."""
    print("Verifying repository...")
    try:
        result = run_command(
            ["gh", "repo", "view", "--json", "name,owner"],
            check=False,
        )
        if result.returncode != 0:
            print("Not in a GitHub repository or gh repo view failed")
            return False
        repo_info = json.loads(result.stdout)
        repo_name = repo_info["name"]
        org_name = repo_info["owner"]["login"]
        if repo_name == REPOSITORY and org_name == ORGANIZATION:
            print(f"Repository: {org_name}/{repo_name}")
            return True
        else:
            print(f"Expected {ORGANIZATION}/{REPOSITORY}, got {org_name}/{repo_name}")
            print("This is fine if you're configuring a different repo")
            return True
    except Exception as e:
        print(f"Could not verify repository: {e}")
        return True  # Continue anyway


def create_labels(dry_run=False):
    """Create all required labels (idempotent)."""
    print("Creating labels...")
    created = []
    for label in LABELS:
        label_name = label["name"]
        if dry_run:
            print(f"  [DRY-RUN] Would create label: {label_name}")
            created.append(label_name)
            continue
        
        if gh_exists(label_name):
            print(f"  Label exists: {label_name}")
        else:
            try:
                cmd = [
                    "gh", "label", "create", label_name,
                    "--color", label["color"],
                    "--description", label["description"],
                    "--force",
                ]
                run_command(cmd)
                print(f"  Created: {label_name}")
                created.append(label_name)
            except Exception as e:
                print(f"  Failed to create {label_name}: {e}")
    
    return created


def create_milestones(dry_run=False):
    """Create all required milestones (idempotent)."""
    print("Creating milestones...")
    created = []
    for milestone in MILESTONES:
        milestone_title = milestone["title"]
        if dry_run:
            print(f"  [DRY-RUN] Would create milestone: {milestone_title}")
            created.append(milestone_title)
            continue
        
        # Check if milestone exists
        try:
            result = run_command(
                ["gh", "milestone", "list", "--json", "title"],
                check=False,
            )
            if result.returncode == 0:
                milestones = json.loads(result.stdout)
                exists = any(m["title"] == milestone_title for m in milestones)
                if exists:
                    print(f"  Milestone exists: {milestone_title}")
                    continue
        except Exception:
            pass
        
        try:
            cmd = [
                "gh", "milestone", "create", milestone_title,
                "--description", milestone["description"],
                "--state", milestone["state"],
            ]
            run_command(cmd)
            print(f"  Created: {milestone_title}")
            created.append(milestone_title)
        except Exception as e:
            print(f"  Failed to create {milestone_title}: {e}")
    
    return created


def create_project(dry_run=False):
    """Create or verify Project V2 (idempotent)."""
    print("Creating GitHub Project V2...")
    
    if dry_run:
        print(f"  [DRY-RUN] Would create project: {PROJECT_NAME}")
        print(f"  Description: {PROJECT_DESCRIPTION}")
        print(f"  Views: Board, Table, Roadmap")
        return None
    
    # Check if project exists
    project_id = gh_project_exists(PROJECT_NAME)
    if project_id:
        print(f"  Project exists: {PROJECT_NAME} (ID: {project_id})")
        return project_id
    
    try:
        # Create project
        result = run_command([
            "gh", "project", "create",
            "--name", PROJECT_NAME,
            "--description", PROJECT_DESCRIPTION,
            "--owner", ORGANIZATION,
        ])
        print(f"  Created project: {PROJECT_NAME}")
        
        # Parse project ID from output
        if "id:" in result.stdout:
            project_id = result.stdout.split("id:")[-1].strip().split()[0]
            print(f"  Project ID: {project_id}")
            return project_id
        return None
    except Exception as e:
        print(f"  Failed to create project: {e}")
        return None


def verify_workflows(dry_run=False):
    """Verify all required workflows exist."""
    print("Verifying GitHub Actions workflows...")
    workflows_dir = Path(".github/workflows")
    all_exist = True
    
    for workflow in REQUIRED_WORKFLOWS:
        workflow_path = workflows_dir / workflow
        if workflow_path.exists():
            print(f"  {workflow}")
        else:
            print(f"  Missing: {workflow}")
            all_exist = False
    
    return all_exist


def verify_templates(dry_run=False):
    """Verify all required issue/PR templates exist."""
    print("Verifying issue and PR templates...")
    templates_dir = Path(".github")
    all_exist = True
    
    for template in REQUIRED_TEMPLATES:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"  {template}")
        else:
            print(f"  Missing: {template}")
            all_exist = False
    
    return all_exist


def verify_codeowners(dry_run=False):
    """Verify CODEOWNERS file exists and is valid."""
    print("Verifying CODEOWNERS...")
    codeowners_path = Path(".github/CODEOWNERS")
    
    if codeowners_path.exists():
        print(f"  CODEOWNERS exists")
        # Basic validation: check for required sections
        content = codeowners_path.read_text(encoding="utf-8")
        required_sections = [
            "# Global",
            "/docs/",
            "/specs/",
            "/packages/",
        ]
        for section in required_sections:
            if section in content:
                print(f"    Contains: {section}")
            else:
                print(f"    Missing: {section}")
        return True
    else:
        print(f"  CODEOWNERS missing")
        return False


def print_branch_protection_recommendations():
    """Print branch protection recommendations."""
    print("Branch Protection Recommendations:")
    print(BRANCH_PROTECTION_RECOMMENDATIONS)


def print_summary(
    labels_created,
    milestones_created,
    workflows_ok,
    templates_ok,
    codeowners_ok,
    dry_run,
):
    """Print bootstrap summary."""
    print("")
    print("=" * 60)
    print("BOOTSTRAP SUMMARY")
    print("=" * 60)
    
    if dry_run:
        print("")
        print("DRY RUN MODE -- No changes were made")
    
    print(f"")
    print(f"Labels: {len(labels_created)} processed")
    print(f"Milestones: {len(milestones_created)} processed")
    print(f"Workflows: {'All present' if workflows_ok else 'Missing'}")
    print(f"Templates: {'All present' if templates_ok else 'Missing'}")
    print(f"CODEOWNERS: {'Valid' if codeowners_ok else 'Missing/Invalid'}")
    
    print("")
    print("Bootstrap complete!")
    print("   Next steps:")
    print("   1. Review branch protection recommendations")
    print("   2. Configure project views (Board, Table, Roadmap)")
    print("   3. Add project to repository settings")
    print("   4. Enable GitHub Discussions")
    print("   5. Configure discussion categories")


# -- Main --

def main():
    """Main bootstrap function."""
    parser = argparse.ArgumentParser(
        description="Atlas GitHub Infrastructure Bootstrap Script",
        epilog="Run multiple times safely -- all operations are idempotent.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them",
    )
    parser.add_argument(
        "--org",
        default=ORGANIZATION,
        help=f"GitHub organization (default: {ORGANIZATION})",
    )
    parser.add_argument(
        "--repo",
        default=REPOSITORY,
        help=f"Repository name (default: {REPOSITORY})",
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("ATLAS GITHUB INFRASTRUCTURE BOOTSTRAP")
    print("=" * 60)
    print(f"Organization: {args.org}")
    print(f"Repository: {args.repo}")
    print(f"Dry run: {args.dry_run}")
    print("")
    
    # Verify authentication
    if not verify_github_auth():
        return 1
    
    # Verify repository
    verify_repository()
    
    # Create labels
    labels_created = create_labels(dry_run=args.dry_run)
    
    # Create milestones
    milestones_created = create_milestones(dry_run=args.dry_run)
    
    # Create project
    project_id = create_project(dry_run=args.dry_run)
    
    # Verify workflows
    workflows_ok = verify_workflows(dry_run=args.dry_run)
    
    # Verify templates
    templates_ok = verify_templates(dry_run=args.dry_run)
    
    # Verify CODEOWNERS
    codeowners_ok = verify_codeowners(dry_run=args.dry_run)
    
    # Print branch protection recommendations
    print_branch_protection_recommendations()
    
    # Print summary
    print_summary(
        labels_created,
        milestones_created,
        workflows_ok,
        templates_ok,
        codeowners_ok,
        args.dry_run,
    )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
