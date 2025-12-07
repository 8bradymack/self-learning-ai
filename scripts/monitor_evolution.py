#!/usr/bin/env python3
"""
Evolution Monitor - Real-time monitoring of evolution progress
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
import json
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import os

console = Console()


def get_latest_log():
    """Get the most recent evolution log file"""
    log_dir = Path("data/logs")
    if not log_dir.exists():
        return None

    log_files = list(log_dir.glob("evolution_*.json"))
    if not log_files:
        return None

    return max(log_files, key=lambda p: p.stat().st_mtime)


def get_latest_checkpoint():
    """Get the most recent checkpoint"""
    checkpoint_dir = Path("data/checkpoints")
    if not checkpoint_dir.exists():
        return None

    checkpoints = list(checkpoint_dir.glob("evolution_checkpoint_*.json"))
    if not checkpoints:
        return None

    return max(checkpoints, key=lambda p: p.stat().st_mtime)


def create_status_table():
    """Create a real-time status display"""

    memory = VectorMemory()
    stats = memory.get_stats()

    # Get latest log
    log_file = get_latest_log()
    log_data = {}
    if log_file:
        with open(log_file) as f:
            log_data = json.load(f)

    # Get latest checkpoint
    checkpoint_file = get_latest_checkpoint()
    checkpoint_data = {}
    if checkpoint_file:
        with open(checkpoint_file) as f:
            checkpoint_data = json.load(f)

    # Create main table
    table = Table(title="🧬 Evolution System Monitor", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    # Knowledge base stats
    table.add_row("Knowledge Base Size", f"{stats['total_items']:,} items")

    # Checkpoint stats
    if checkpoint_data:
        table.add_row("Last Checkpoint", checkpoint_data.get('timestamp', 'N/A'))
        table.add_row("Attempts Completed", f"{checkpoint_data.get('attempt', 0):,}")
        table.add_row("Successful Mutations", f"{checkpoint_data.get('successful_mutations', 0):,}")
        table.add_row("Failed Mutations", f"{checkpoint_data.get('failed_mutations', 0):,}")

        total = checkpoint_data.get('successful_mutations', 0) + checkpoint_data.get('failed_mutations', 0)
        if total > 0:
            success_rate = (checkpoint_data.get('successful_mutations', 0) / total) * 100
            table.add_row("Success Rate", f"{success_rate:.1f}%")

    # Log stats
    if log_data:
        start_time = datetime.fromisoformat(log_data.get('start_time', datetime.now().isoformat()))
        elapsed = (datetime.now() - start_time).total_seconds()
        table.add_row("Elapsed Time", f"{elapsed/3600:.1f} hours")

        if 'current_attempt' in log_data and 'max_attempts' in log_data:
            progress = (log_data['current_attempt'] / log_data['max_attempts']) * 100
            table.add_row("Progress", f"{progress:.2f}%")

    return Panel(table, border_style="green")


def monitor_live(interval: int = 10):
    """Live monitoring with auto-refresh"""

    console.print("\n[bold green]🧬 Evolution System Monitor[/bold green]")
    console.print("[yellow]Press Ctrl+C to exit[/yellow]\n")

    try:
        while True:
            console.clear()
            panel = create_status_table()
            console.print(panel)
            console.print(f"\n[dim]Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
            console.print(f"[dim]Refreshing every {interval} seconds...[/dim]")
            time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Monitoring stopped.[/yellow]")


def monitor_once():
    """Show status once and exit"""
    panel = create_status_table()
    console.print(panel)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Monitor evolution progress')
    parser.add_argument('--live', action='store_true', help='Live monitoring with auto-refresh')
    parser.add_argument('--interval', type=int, default=10, help='Refresh interval in seconds (default: 10)')
    args = parser.parse_args()

    if args.live:
        monitor_live(interval=args.interval)
    else:
        monitor_once()
