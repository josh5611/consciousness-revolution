#!/usr/bin/env python3
"""
PC1 Maintenance Daemon
Runs daily/weekly to keep system clean
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Locations
HOME = Path.home()
DESKTOP = HOME / "Desktop"
DOWNLOADS = HOME / "Downloads"
TEMP = Path(os.environ.get('TEMP', '/tmp'))
ARCHIVE = HOME / "AUTO_ARCHIVE"

# Ensure archive exists
ARCHIVE.mkdir(exist_ok=True)
(ARCHIVE / "desktop").mkdir(exist_ok=True)
(ARCHIVE / "downloads").mkdir(exist_ok=True)

def get_file_age_days(filepath):
    """Get file age in days"""
    mtime = os.path.getmtime(filepath)
    age = datetime.now() - datetime.fromtimestamp(mtime)
    return age.days

def clean_desktop():
    """Archive desktop files older than 7 days"""
    print("🧹 Cleaning Desktop...")
    moved = 0

    if not DESKTOP.exists():
        return 0

    archive_folder = ARCHIVE / "desktop" / datetime.now().strftime("%Y-%m-%d")

    for item in DESKTOP.iterdir():
        # Skip system files
        if item.name.startswith('.') or item.name in ['desktop.ini']:
            continue

        # Check age
        try:
            if get_file_age_days(item) > 7:
                archive_folder.mkdir(exist_ok=True)
                dest = archive_folder / item.name
                shutil.move(str(item), str(dest))
                moved += 1
                print(f"  📦 Archived: {item.name}")
        except Exception as e:
            print(f"  ⚠️ Skipped {item.name}: {e}")

    print(f"  ✅ Moved {moved} items from Desktop")
    return moved

def clean_downloads():
    """Archive downloads older than 14 days"""
    print("🧹 Cleaning Downloads...")
    moved = 0

    if not DOWNLOADS.exists():
        return 0

    archive_folder = ARCHIVE / "downloads" / datetime.now().strftime("%Y-%m-%d")

    for item in DOWNLOADS.iterdir():
        if item.name.startswith('.'):
            continue

        try:
            if get_file_age_days(item) > 14:
                archive_folder.mkdir(exist_ok=True)
                dest = archive_folder / item.name
                shutil.move(str(item), str(dest))
                moved += 1
                print(f"  📦 Archived: {item.name}")
        except Exception as e:
            print(f"  ⚠️ Skipped {item.name}: {e}")

    print(f"  ✅ Moved {moved} items from Downloads")
    return moved

def clean_temp():
    """Delete temp files older than 3 days"""
    print("🧹 Cleaning Temp...")
    deleted = 0

    for item in TEMP.iterdir():
        try:
            if get_file_age_days(item) > 3:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
                deleted += 1
        except:
            pass

    print(f"  ✅ Deleted {deleted} temp items")
    return deleted

def clean_old_archives():
    """Delete archives older than 30 days"""
    print("🧹 Cleaning old archives...")
    deleted = 0

    for subfolder in ['desktop', 'downloads']:
        folder = ARCHIVE / subfolder
        if not folder.exists():
            continue

        for item in folder.iterdir():
            try:
                if get_file_age_days(item) > 30:
                    shutil.rmtree(item)
                    deleted += 1
                    print(f"  🗑️ Deleted old archive: {item.name}")
            except:
                pass

    print(f"  ✅ Deleted {deleted} old archives")
    return deleted

def generate_report():
    """Generate maintenance report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "desktop_items": len(list(DESKTOP.iterdir())) if DESKTOP.exists() else 0,
        "downloads_items": len(list(DOWNLOADS.iterdir())) if DOWNLOADS.exists() else 0,
        "archive_size_mb": sum(f.stat().st_size for f in ARCHIVE.rglob('*') if f.is_file()) / (1024*1024)
    }
    return report

def run_maintenance():
    """Run full maintenance cycle"""
    print(f"\n{'='*50}")
    print(f"🔧 MAINTENANCE DAEMON - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")

    clean_desktop()
    clean_downloads()
    clean_temp()
    clean_old_archives()

    report = generate_report()

    print(f"\n{'='*50}")
    print(f"📊 REPORT")
    print(f"  Desktop items: {report['desktop_items']}")
    print(f"  Downloads items: {report['downloads_items']}")
    print(f"  Archive size: {report['archive_size_mb']:.1f} MB")
    print(f"{'='*50}\n")

    return report

if __name__ == "__main__":
    run_maintenance()
