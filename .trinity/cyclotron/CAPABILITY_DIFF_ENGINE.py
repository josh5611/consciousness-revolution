#!/usr/bin/env python3
"""
CAPABILITY_DIFF_ENGINE.py - Cross-PC Capability Analysis

Compares capability manifests across Trinity PCs to identify:
- Missing software/tools on each PC
- Unique capabilities per PC
- Synchronization opportunities
- Capability gaps and recommendations

Part of CYCLOTRON - The Trinity Capability Sync System

Author: C1 T2 (PC2 - DESKTOP-MSMCFH2)
Created: 2025-11-24
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any
from collections import defaultdict

# ============= Configuration =============

# Trinity PCs
PCS = ["PC1", "PC2", "PC3"]

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
MANIFESTS_DIR = BASE_DIR / ".trinity" / "capability_manifests"
REPORTS_DIR = BASE_DIR / ".trinity" / "cyclotron" / "reports"
HUB_DIR = BASE_DIR / "LOCAL_TRINITY_HUB" / "cyclotron_reports"

# Ensure directories exist
for dir_path in [MANIFESTS_DIR, REPORTS_DIR, HUB_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============= Data Classes =============

class CapabilityDiff:
    """Represents capability differences across Trinity."""

    def __init__(self):
        self.manifests = {}  # PC -> manifest
        self.software_matrix = defaultdict(dict)  # software -> PC -> version
        self.mcp_matrix = defaultdict(dict)  # mcp_tool -> PC -> config
        self.api_matrix = defaultdict(dict)  # api -> PC -> status
        self.unique_capabilities = defaultdict(list)  # PC -> [unique items]
        self.missing_capabilities = defaultdict(list)  # PC -> [missing items]
        self.sync_opportunities = []  # [(item, from_pc, to_pcs)]

# ============= Manifest Loading =============

def load_manifests() -> Dict[str, Dict]:
    """Load all available PC manifests."""
    manifests = {}

    for pc in PCS:
        manifest_file = MANIFESTS_DIR / f"{pc}_MANIFEST.json"

        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    manifests[pc] = json.load(f)
                print(f"✅ Loaded manifest: {pc}")
            except Exception as e:
                print(f"❌ Failed to load {pc} manifest: {e}")
        else:
            print(f"⚠️  Manifest not found: {pc} (skipping)")

    return manifests

# ============= Analysis Functions =============

def build_software_matrix(manifests: Dict[str, Dict]) -> Dict[str, Dict[str, str]]:
    """Build matrix of software across PCs."""
    matrix = defaultdict(dict)

    for pc, manifest in manifests.items():
        software_list = manifest.get("software_inventory", [])
        for software in software_list:
            name = software.get("name", "")
            version = software.get("version", "unknown")
            matrix[name][pc] = version

    return dict(matrix)

def build_mcp_matrix(manifests: Dict[str, Dict]) -> Dict[str, Dict[str, Any]]:
    """Build matrix of MCP tools across PCs."""
    matrix = defaultdict(dict)

    for pc, manifest in manifests.items():
        mcp_tools = manifest.get("mcp_tools", [])
        for tool in mcp_tools:
            name = tool.get("name", "")
            matrix[name][pc] = tool

    return dict(matrix)

def build_api_matrix(manifests: Dict[str, Dict]) -> Dict[str, Dict[str, str]]:
    """Build matrix of API keys across PCs."""
    matrix = defaultdict(dict)

    for pc, manifest in manifests.items():
        api_keys = manifest.get("api_keys", [])
        for api in api_keys:
            service = api.get("service", "")
            status = api.get("status", "unknown")
            matrix[service][pc] = status

    return dict(matrix)

def find_unique_capabilities(manifests: Dict[str, Dict], matrix: Dict) -> Dict[str, List[str]]:
    """Find capabilities unique to each PC."""
    unique = defaultdict(list)

    for item, pc_versions in matrix.items():
        if len(pc_versions) == 1:  # Only on one PC
            pc = list(pc_versions.keys())[0]
            unique[pc].append(item)

    return dict(unique)

def find_missing_capabilities(manifests: Dict[str, Dict], matrix: Dict) -> Dict[str, List[str]]:
    """Find capabilities missing on each PC."""
    missing = defaultdict(list)

    all_items = set(matrix.keys())
    for pc in manifests.keys():
        pc_items = set(item for item, pc_versions in matrix.items() if pc in pc_versions)
        missing_items = all_items - pc_items
        missing[pc] = list(missing_items)

    return dict(missing)

def find_sync_opportunities(manifests: Dict[str, Dict], software_matrix: Dict) -> List[tuple]:
    """Find high-value sync opportunities."""
    opportunities = []

    # Critical software that should be on all PCs
    critical_software = [
        "Python",
        "Node.js",
        "Git",
        "VSCode",
        "Claude Code"
    ]

    for software in critical_software:
        if software in software_matrix:
            have_pcs = set(software_matrix[software].keys())
            all_pcs = set(manifests.keys())
            missing_pcs = all_pcs - have_pcs

            if missing_pcs:
                from_pc = list(have_pcs)[0] if have_pcs else None
                if from_pc:
                    opportunities.append((
                        software,
                        from_pc,
                        list(missing_pcs),
                        "critical"
                    ))

    return opportunities

# ============= Report Generation =============

def generate_text_report(diff: CapabilityDiff) -> str:
    """Generate human-readable text report."""

    report = []
    report.append("=" * 80)
    report.append("TRINITY CAPABILITY DIFF REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"PCs Analyzed: {', '.join(diff.manifests.keys())}")
    report.append("")

    # Software Analysis
    report.append("-" * 80)
    report.append("SOFTWARE DISTRIBUTION")
    report.append("-" * 80)
    report.append("")

    total_software = len(diff.software_matrix)
    report.append(f"Total Software Packages: {total_software}")
    report.append("")

    # Software on all PCs
    on_all = [s for s, pcs in diff.software_matrix.items() if len(pcs) == len(diff.manifests)]
    report.append(f"✅ On All PCs ({len(on_all)}):")
    for software in sorted(on_all)[:10]:  # Top 10
        versions = diff.software_matrix[software]
        version_str = ", ".join(f"{pc}: {v}" for pc, v in versions.items())
        report.append(f"   • {software} ({version_str})")
    if len(on_all) > 10:
        report.append(f"   ... and {len(on_all) - 10} more")
    report.append("")

    # Unique software per PC
    report.append("🎯 Unique Capabilities:")
    for pc, items in diff.unique_capabilities.items():
        report.append(f"   {pc}: {len(items)} unique items")
        for item in sorted(items)[:5]:
            report.append(f"      • {item}")
        if len(items) > 5:
            report.append(f"      ... and {len(items) - 5} more")
    report.append("")

    # Missing software per PC
    report.append("⚠️  Missing Capabilities:")
    for pc, items in diff.missing_capabilities.items():
        report.append(f"   {pc}: {len(items)} missing items")
        for item in sorted(items)[:5]:
            report.append(f"      • {item}")
        if len(items) > 5:
            report.append(f"      ... and {len(items) - 5} more")
    report.append("")

    # Sync opportunities
    report.append("-" * 80)
    report.append("SYNCHRONIZATION OPPORTUNITIES")
    report.append("-" * 80)
    report.append("")

    if diff.sync_opportunities:
        report.append(f"Found {len(diff.sync_opportunities)} sync opportunities:")
        for software, from_pc, to_pcs, priority in diff.sync_opportunities:
            to_pcs_str = ", ".join(to_pcs)
            report.append(f"   [{priority.upper()}] {software}")
            report.append(f"      From: {from_pc}")
            report.append(f"      To: {to_pcs_str}")
        report.append("")
    else:
        report.append("No critical sync opportunities found.")
        report.append("")

    # MCP Tools
    if diff.mcp_matrix:
        report.append("-" * 80)
        report.append("MCP TOOLS DISTRIBUTION")
        report.append("-" * 80)
        report.append("")

        report.append(f"Total MCP Tools: {len(diff.mcp_matrix)}")
        for tool, pcs in diff.mcp_matrix.items():
            pcs_str = ", ".join(pcs.keys())
            report.append(f"   • {tool}: {pcs_str}")
        report.append("")

    # API Keys
    if diff.api_matrix:
        report.append("-" * 80)
        report.append("API KEYS DISTRIBUTION")
        report.append("-" * 80)
        report.append("")

        report.append(f"Total API Services: {len(diff.api_matrix)}")
        for service, pcs in diff.api_matrix.items():
            status_str = ", ".join(f"{pc}: {status}" for pc, status in pcs.items())
            report.append(f"   • {service}: {status_str}")
        report.append("")

    # Summary
    report.append("-" * 80)
    report.append("SUMMARY")
    report.append("-" * 80)
    report.append("")

    avg_software = sum(len([p for p in pcs if pc in pcs]) for pcs in diff.software_matrix.values()) // len(diff.manifests) if diff.manifests else 0
    report.append(f"Average software per PC: {avg_software}")
    report.append(f"Unique capabilities: {sum(len(items) for items in diff.unique_capabilities.values())}")
    report.append(f"Missing capabilities: {sum(len(items) for items in diff.missing_capabilities.values())}")
    report.append(f"Sync opportunities: {len(diff.sync_opportunities)}")
    report.append("")

    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    return "\n".join(report)

def generate_json_report(diff: CapabilityDiff) -> Dict:
    """Generate machine-readable JSON report."""

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pcs_analyzed": list(diff.manifests.keys()),
        "summary": {
            "total_software": len(diff.software_matrix),
            "total_mcp_tools": len(diff.mcp_matrix),
            "total_api_services": len(diff.api_matrix),
            "unique_capabilities": {pc: len(items) for pc, items in diff.unique_capabilities.items()},
            "missing_capabilities": {pc: len(items) for pc, items in diff.missing_capabilities.items()},
            "sync_opportunities": len(diff.sync_opportunities)
        },
        "software_matrix": diff.software_matrix,
        "mcp_matrix": diff.mcp_matrix,
        "api_matrix": diff.api_matrix,
        "unique_capabilities": diff.unique_capabilities,
        "missing_capabilities": diff.missing_capabilities,
        "sync_opportunities": [
            {
                "software": software,
                "from_pc": from_pc,
                "to_pcs": to_pcs,
                "priority": priority
            }
            for software, from_pc, to_pcs, priority in diff.sync_opportunities
        ]
    }

def generate_html_report(diff: CapabilityDiff) -> str:
    """Generate beautiful HTML report."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trinity Capability Diff Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 2.5em;
            background: linear-gradient(45deg, #00ff88, #00ffff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid rgba(0, 255, 136, 0.3);
            text-align: center;
        }}

        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #00ff88;
        }}

        .stat-label {{
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 10px;
        }}

        .section {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 2px solid rgba(0, 255, 136, 0.3);
            margin-bottom: 25px;
        }}

        .section h2 {{
            color: #00ff88;
            margin-bottom: 20px;
            border-bottom: 2px solid #00ff88;
            padding-bottom: 10px;
        }}

        .matrix-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        .matrix-table th,
        .matrix-table td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .matrix-table th {{
            color: #00ff88;
            font-weight: bold;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }}

        .badge-success {{
            background: #00ff88;
            color: #000;
        }}

        .badge-warning {{
            background: #ffa500;
            color: #000;
        }}

        .badge-critical {{
            background: #ff6b6b;
            color: #fff;
        }}

        .pc-list {{
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }}

        .pc-card {{
            flex: 1;
            background: rgba(255, 255, 255, 0.03);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #00ff88;
        }}

        .pc-card h3 {{
            color: #00ffff;
            margin-bottom: 10px;
        }}

        ul {{
            list-style: none;
            padding-left: 0;
        }}

        ul li {{
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }}

        ul li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #00ff88;
        }}

        .opportunity {{
            background: rgba(255, 255, 255, 0.03);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #ffa500;
        }}

        .opportunity-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .opportunity-title {{
            font-size: 1.1em;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌌 Trinity Capability Diff Report</h1>
            <div class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div class="subtitle">PCs Analyzed: {', '.join(diff.manifests.keys())}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(diff.software_matrix)}</div>
                <div class="stat-label">Software Packages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(diff.mcp_matrix)}</div>
                <div class="stat-label">MCP Tools</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(diff.api_matrix)}</div>
                <div class="stat-label">API Services</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(diff.sync_opportunities)}</div>
                <div class="stat-label">Sync Opportunities</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 Capability Distribution</h2>
            <div class="pc-list">
"""

    # Per-PC stats
    for pc in diff.manifests.keys():
        unique_count = len(diff.unique_capabilities.get(pc, []))
        missing_count = len(diff.missing_capabilities.get(pc, []))
        html += f"""
                <div class="pc-card">
                    <h3>{pc}</h3>
                    <div>Unique: <span class="badge badge-success">{unique_count}</span></div>
                    <div>Missing: <span class="badge badge-warning">{missing_count}</span></div>
                </div>
"""

    html += """
            </div>
        </div>

        <div class="section">
            <h2>🔄 Synchronization Opportunities</h2>
"""

    if diff.sync_opportunities:
        for software, from_pc, to_pcs, priority in diff.sync_opportunities:
            badge_class = "badge-critical" if priority == "critical" else "badge-warning"
            to_pcs_str = ", ".join(to_pcs)
            html += f"""
            <div class="opportunity">
                <div class="opportunity-header">
                    <div class="opportunity-title">{software}</div>
                    <span class="badge {badge_class}">{priority.upper()}</span>
                </div>
                <div>From: <strong>{from_pc}</strong> → To: <strong>{to_pcs_str}</strong></div>
            </div>
"""
    else:
        html += "<p>No critical sync opportunities found.</p>"

    html += """
        </div>

        <div class="section">
            <h2>🎯 Unique Capabilities</h2>
            <div class="pc-list">
"""

    for pc, items in diff.unique_capabilities.items():
        html += f"""
                <div class="pc-card">
                    <h3>{pc} ({len(items)})</h3>
                    <ul>
"""
        for item in sorted(items)[:10]:
            html += f"                        <li>{item}</li>\n"
        if len(items) > 10:
            html += f"                        <li>... and {len(items) - 10} more</li>\n"
        html += """
                    </ul>
                </div>
"""

    html += """
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html

# ============= Main Analysis =============

def analyze_capabilities() -> CapabilityDiff:
    """Run full capability analysis."""

    print("\n" + "=" * 80)
    print("TRINITY CAPABILITY DIFF ENGINE")
    print("=" * 80 + "\n")

    # Load manifests
    print("Step 1: Loading manifests...")
    manifests = load_manifests()

    if not manifests:
        print("❌ No manifests found. Run CAPABILITY_MANIFEST.py on each PC first.")
        return None

    print(f"✅ Loaded {len(manifests)} manifest(s)\n")

    # Create diff object
    diff = CapabilityDiff()
    diff.manifests = manifests

    # Build matrices
    print("Step 2: Building capability matrices...")
    diff.software_matrix = build_software_matrix(manifests)
    diff.mcp_matrix = build_mcp_matrix(manifests)
    diff.api_matrix = build_api_matrix(manifests)
    print(f"✅ Software matrix: {len(diff.software_matrix)} items")
    print(f"✅ MCP matrix: {len(diff.mcp_matrix)} items")
    print(f"✅ API matrix: {len(diff.api_matrix)} items\n")

    # Find unique capabilities
    print("Step 3: Finding unique capabilities...")
    diff.unique_capabilities = find_unique_capabilities(manifests, diff.software_matrix)
    for pc, items in diff.unique_capabilities.items():
        print(f"   {pc}: {len(items)} unique items")
    print()

    # Find missing capabilities
    print("Step 4: Finding missing capabilities...")
    diff.missing_capabilities = find_missing_capabilities(manifests, diff.software_matrix)
    for pc, items in diff.missing_capabilities.items():
        print(f"   {pc}: {len(items)} missing items")
    print()

    # Find sync opportunities
    print("Step 5: Finding sync opportunities...")
    diff.sync_opportunities = find_sync_opportunities(manifests, diff.software_matrix)
    print(f"✅ Found {len(diff.sync_opportunities)} sync opportunities\n")

    return diff

def save_reports(diff: CapabilityDiff):
    """Save all report formats."""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Text report
    text_file = REPORTS_DIR / f"capability_diff_{timestamp}.txt"
    with open(text_file, 'w') as f:
        f.write(generate_text_report(diff))
    print(f"✅ Text report: {text_file}")

    # JSON report
    json_file = REPORTS_DIR / f"capability_diff_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(generate_json_report(diff), f, indent=2)
    print(f"✅ JSON report: {json_file}")

    # HTML report
    html_file = REPORTS_DIR / f"capability_diff_{timestamp}.html"
    with open(html_file, 'w') as f:
        f.write(generate_html_report(diff))
    print(f"✅ HTML report: {html_file}")

    # Copy to hub
    hub_file = HUB_DIR / f"capability_diff_latest.json"
    with open(hub_file, 'w') as f:
        json.dump(generate_json_report(diff), f, indent=2)
    print(f"✅ Hub report: {hub_file}")

# ============= CLI =============

def main():
    """Main entry point."""
    try:
        diff = analyze_capabilities()

        if diff:
            print("\nStep 6: Generating reports...")
            save_reports(diff)

            print("\n" + "=" * 80)
            print("ANALYSIS COMPLETE!")
            print("=" * 80)
            print(f"\nReports saved to: {REPORTS_DIR}")
            print(f"Hub report: {HUB_DIR}")
            print("\n✨ Capability diff analysis complete! ✨\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
