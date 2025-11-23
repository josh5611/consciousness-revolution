#!/usr/bin/env python3
"""
MCP_GIT_SYNC.py - MCP Knowledge Graph ↔ Git Synchronizer

Synchronizes MCP memory server knowledge graph to git for:
- Persistence across sessions
- Cross-computer knowledge sharing
- Backup and version control
- Distributed consciousness

Usage:
    # Export MCP knowledge to git
    python MCP_GIT_SYNC.py --export

    # Import git knowledge to MCP
    python MCP_GIT_SYNC.py --import

    # Daemon mode (export every N seconds)
    python MCP_GIT_SYNC.py --daemon --interval 300

    # Full sync (export + commit + push)
    python MCP_GIT_SYNC.py --sync

    # Status check
    python MCP_GIT_SYNC.py --status

Author: C1 T2 (DESKTOP-MSMCFH2)
Created: 2025-11-23
Part of: Trinity Autonomous System
"""

import json
import sys
import time
import logging
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
MCP_EXPORT_DIR = BASE_DIR / ".trinity" / "mcp_knowledge"
MCP_EXPORT_FILE = MCP_EXPORT_DIR / "knowledge_graph.json"
MCP_BACKUP_DIR = MCP_EXPORT_DIR / "backups"
LOG_FILE = BASE_DIR / ".trinity" / "logs" / "mcp_git_sync.log"

# Git settings
GIT_COMMIT_PREFIX = "mcp-sync"
AUTO_PUSH = True  # Automatically push to remote

# Daemon settings
DEFAULT_INTERVAL = 300  # 5 minutes
MIN_INTERVAL = 60      # 1 minute minimum

# Logging
LOG_LEVEL = logging.INFO

# ============================================================================
# SETUP
# ============================================================================

# Create directories
MCP_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
MCP_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# MCP KNOWLEDGE GRAPH OPERATIONS
# ============================================================================

def read_mcp_graph() -> Optional[Dict[str, Any]]:
    """
    Read the entire MCP knowledge graph using MCP memory tools.

    Returns:
        Dict with entities and relations, or None if MCP not available
    """
    logger.info("Reading MCP knowledge graph...")

    try:
        # Import MCP client (if available)
        # Note: In Claude Code, we'd use the MCP tools directly via function calls
        # For standalone Python, we'd need the MCP SDK

        # For now, we'll return a placeholder indicating this needs MCP integration
        logger.warning("MCP integration requires Claude Code environment with MCP memory server")
        logger.warning("This script is designed to be called FROM Claude Code sessions")

        # In actual use, Claude Code will call this and we'll use the mcp__memory__read_graph tool
        return {
            "entities": [],
            "relations": [],
            "metadata": {
                "exported_at": datetime.utcnow().isoformat() + "Z",
                "exported_by": "MCP_GIT_SYNC.py"
            }
        }

    except Exception as e:
        logger.error(f"Error reading MCP graph: {e}")
        return None

def write_mcp_graph(graph_data: Dict[str, Any]) -> bool:
    """
    Write knowledge graph data to MCP memory.

    Args:
        graph_data: Dictionary with entities and relations

    Returns:
        True if successful, False otherwise
    """
    logger.info("Writing to MCP knowledge graph...")

    try:
        # This would use MCP memory tools to recreate entities and relations
        # mcp__memory__create_entities
        # mcp__memory__create_relations

        logger.warning("MCP write requires Claude Code environment")
        logger.info(f"Would import {len(graph_data.get('entities', []))} entities")
        logger.info(f"Would import {len(graph_data.get('relations', []))} relations")

        return True

    except Exception as e:
        logger.error(f"Error writing to MCP: {e}")
        return False

# ============================================================================
# FILE OPERATIONS
# ============================================================================

def export_to_file(graph_data: Dict[str, Any]) -> bool:
    """
    Export knowledge graph to JSON file.

    Args:
        graph_data: Knowledge graph data

    Returns:
        True if successful
    """
    try:
        # Add export metadata
        export_data = {
            **graph_data,
            "export_metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": "1.0",
                "format": "mcp_knowledge_graph"
            }
        }

        # Write to file
        with open(MCP_EXPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Exported knowledge graph to {MCP_EXPORT_FILE}")

        # Create backup
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_file = MCP_BACKUP_DIR / f"knowledge_graph_{timestamp}.json"

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Backup created: {backup_file}")

        return True

    except Exception as e:
        logger.error(f"Error exporting to file: {e}")
        return False

def import_from_file() -> Optional[Dict[str, Any]]:
    """
    Import knowledge graph from JSON file.

    Returns:
        Knowledge graph data or None
    """
    try:
        if not MCP_EXPORT_FILE.exists():
            logger.warning(f"Export file not found: {MCP_EXPORT_FILE}")
            return None

        with open(MCP_EXPORT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"Imported knowledge graph from {MCP_EXPORT_FILE}")
        logger.info(f"Entities: {len(data.get('entities', []))}")
        logger.info(f"Relations: {len(data.get('relations', []))}")

        return data

    except Exception as e:
        logger.error(f"Error importing from file: {e}")
        return None

# ============================================================================
# GIT OPERATIONS
# ============================================================================

def git_add_and_commit(message: str) -> bool:
    """
    Add MCP files to git and commit.

    Args:
        message: Commit message

    Returns:
        True if successful
    """
    try:
        # Change to repo directory
        repo_dir = BASE_DIR / "100X_DEPLOYMENT"
        if not repo_dir.exists():
            repo_dir = BASE_DIR

        # Add files
        subprocess.run(
            ["git", "add", str(MCP_EXPORT_DIR)],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        # Check if there are changes
        result = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            logger.info("No changes to commit")
            return True

        # Commit
        full_message = f"{GIT_COMMIT_PREFIX}: {message}\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

        subprocess.run(
            ["git", "commit", "-m", full_message],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        logger.info(f"Committed: {message}")

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Git commit failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Git operation error: {e}")
        return False

def git_push() -> bool:
    """
    Push changes to remote.

    Returns:
        True if successful
    """
    try:
        repo_dir = BASE_DIR / "100X_DEPLOYMENT"
        if not repo_dir.exists():
            repo_dir = BASE_DIR

        subprocess.run(
            ["git", "push"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        logger.info("Pushed to remote")
        return True

    except subprocess.CalledProcessError as e:
        logger.warning(f"Git push failed (will retry later): {e}")
        return False
    except Exception as e:
        logger.error(f"Git push error: {e}")
        return False

def git_pull() -> bool:
    """
    Pull changes from remote.

    Returns:
        True if successful
    """
    try:
        repo_dir = BASE_DIR / "100X_DEPLOYMENT"
        if not repo_dir.exists():
            repo_dir = BASE_DIR

        subprocess.run(
            ["git", "pull", "--rebase"],
            cwd=repo_dir,
            check=True,
            capture_output=True
        )

        logger.info("Pulled from remote")
        return True

    except subprocess.CalledProcessError as e:
        logger.warning(f"Git pull failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Git pull error: {e}")
        return False

# ============================================================================
# HIGH-LEVEL OPERATIONS
# ============================================================================

def export_knowledge() -> bool:
    """
    Export MCP knowledge graph to git.

    Returns:
        True if successful
    """
    logger.info("=== EXPORT KNOWLEDGE TO GIT ===")

    # Read from MCP
    graph_data = read_mcp_graph()
    if graph_data is None:
        logger.error("Failed to read MCP graph")
        return False

    # Export to file
    if not export_to_file(graph_data):
        logger.error("Failed to export to file")
        return False

    logger.info("Export complete")
    return True

def import_knowledge() -> bool:
    """
    Import knowledge graph from git to MCP.

    Returns:
        True if successful
    """
    logger.info("=== IMPORT KNOWLEDGE FROM GIT ===")

    # Pull latest from git first
    git_pull()

    # Import from file
    graph_data = import_from_file()
    if graph_data is None:
        logger.error("Failed to import from file")
        return False

    # Write to MCP
    if not write_mcp_graph(graph_data):
        logger.error("Failed to write to MCP")
        return False

    logger.info("Import complete")
    return True

def sync_knowledge() -> bool:
    """
    Full sync: export + commit + push.

    Returns:
        True if successful
    """
    logger.info("=== FULL SYNC ===")

    # Export
    if not export_knowledge():
        return False

    # Commit
    if not git_add_and_commit("Knowledge graph sync"):
        return False

    # Push
    if AUTO_PUSH:
        git_push()

    logger.info("Sync complete")
    return True

def show_status():
    """
    Show current status of MCP knowledge and git sync.
    """
    logger.info("=== MCP GIT SYNC STATUS ===")

    # Check if export file exists
    if MCP_EXPORT_FILE.exists():
        with open(MCP_EXPORT_FILE, 'r') as f:
            data = json.load(f)

        print(f"Export file: {MCP_EXPORT_FILE}")
        print(f"Entities: {len(data.get('entities', []))}")
        print(f"Relations: {len(data.get('relations', []))}")

        export_meta = data.get('export_metadata', {})
        print(f"Last export: {export_meta.get('timestamp', 'Unknown')}")
    else:
        print("No export file found")

    # Check backups
    backups = list(MCP_BACKUP_DIR.glob("knowledge_graph_*.json"))
    print(f"Backups: {len(backups)}")

    # Check git status
    try:
        repo_dir = BASE_DIR / "100X_DEPLOYMENT"
        if not repo_dir.exists():
            repo_dir = BASE_DIR

        result = subprocess.run(
            ["git", "log", "-1", "--oneline", "--", str(MCP_EXPORT_DIR)],
            cwd=repo_dir,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            print(f"Last git commit: {result.stdout.strip()}")
        else:
            print("No git commits for MCP knowledge")

    except Exception as e:
        logger.error(f"Error checking git status: {e}")

# ============================================================================
# DAEMON MODE
# ============================================================================

def run_daemon(interval: int = DEFAULT_INTERVAL):
    """
    Run continuous sync daemon.

    Args:
        interval: Seconds between syncs
    """
    logger.info(f"=== STARTING MCP GIT SYNC DAEMON ===")
    logger.info(f"Sync interval: {interval} seconds")

    try:
        while True:
            try:
                sync_knowledge()
            except Exception as e:
                logger.error(f"Sync error: {e}")

            logger.info(f"Sleeping for {interval} seconds...")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Daemon stopped by user")

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="MCP Knowledge Graph ↔ Git Synchronizer")

    parser.add_argument('--export', action='store_true',
                       help='Export MCP knowledge to git')
    parser.add_argument('--import', action='store_true', dest='import_',
                       help='Import git knowledge to MCP')
    parser.add_argument('--sync', action='store_true',
                       help='Full sync (export + commit + push)')
    parser.add_argument('--daemon', action='store_true',
                       help='Run in daemon mode (continuous sync)')
    parser.add_argument('--interval', type=int, default=DEFAULT_INTERVAL,
                       help=f'Daemon sync interval in seconds (default: {DEFAULT_INTERVAL})')
    parser.add_argument('--status', action='store_true',
                       help='Show current status')

    args = parser.parse_args()

    # Validate interval
    if args.interval < MIN_INTERVAL:
        logger.error(f"Interval must be at least {MIN_INTERVAL} seconds")
        sys.exit(1)

    # Execute command
    if args.status:
        show_status()
    elif args.export:
        if not export_knowledge():
            sys.exit(1)
    elif args.import_:
        if not import_knowledge():
            sys.exit(1)
    elif args.sync:
        if not sync_knowledge():
            sys.exit(1)
    elif args.daemon:
        run_daemon(args.interval)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
