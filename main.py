#!/usr/bin/env python3
"""
Main Entry Point for Self-Learning AI System
"""

import sys
from pathlib import Path
import argparse
import logging
from rich.console import Console
from rich.logging import RichHandler

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.core.model_loader import ModelLoader
from src.memory.vector_store import VectorMemory
from src.api.ai_apis import AIAPIs
from src.learning.learning_loop import LearningLoop
from src.safety.self_modifier import SelfModifier

# Setup rich console for better output
console = Console()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           SELF-LEARNING AI SYSTEM v0.1                       ║
║                                                              ║
║  A continual learning AI that learns from APIs, the web,     ║
║  and can modify its own code to improve over time.           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def initialize_system():
    """Initialize all system components"""
    console.print("\n[bold yellow]Initializing system components...[/bold yellow]\n")

    try:
        # Initialize components
        model_loader = ModelLoader()
        memory = VectorMemory()
        apis = AIAPIs()
        learning_loop = LearningLoop()
        self_modifier = SelfModifier()

        console.print("✓ Model Loader initialized", style="green")
        console.print("✓ Vector Memory initialized", style="green")
        console.print("✓ API Integrations initialized", style="green")
        console.print("✓ Learning Loop initialized", style="green")
        console.print("✓ Self-Modifier initialized", style="green")

        return {
            "model_loader": model_loader,
            "memory": memory,
            "apis": apis,
            "learning_loop": learning_loop,
            "self_modifier": self_modifier
        }

    except Exception as e:
        console.print(f"\n[bold red]Error initializing system: {e}[/bold red]")
        raise


def run_learning_mode(components, iterations=5):
    """Run in continuous learning mode"""
    console.print(f"\n[bold green]Starting Learning Mode ({iterations} iterations)[/bold green]\n")

    learning_loop = components['learning_loop']

    try:
        learning_loop.run_learning_cycle(n_iterations=iterations)

        console.print("\n[bold green]✓ Learning cycle complete![/bold green]")

        # Show stats
        stats = learning_loop.memory.get_stats()
        console.print(f"\n[bold cyan]Knowledge Base Stats:[/bold cyan]")
        console.print(f"  Total items: {stats['total_items']}")
        console.print(f"  Sources: {stats['sources']}")

    except Exception as e:
        console.print(f"\n[bold red]Error during learning: {e}[/bold red]")
        raise


def run_self_modification_mode(components):
    """Run in self-modification mode"""
    console.print("\n[bold yellow]Starting Self-Modification Mode[/bold yellow]\n")

    self_modifier = components['self_modifier']

    # Example modification goals
    goals = [
        "Improve the learning rate hyperparameter for better training",
        "Optimize the question generation strategy",
        "Add a new data source for learning"
    ]

    for goal in goals:
        console.print(f"\n[cyan]Testing modification goal:[/cyan] {goal}")

        result = self_modifier.propose_and_test_modification(goal)

        if result['success']:
            console.print(f"[green]✓ Modification successful![/green]")
        else:
            console.print(f"[red]✗ Modification failed: {result.get('reason')}[/red]")


def run_interactive_mode(components):
    """Run in interactive mode"""
    console.print("\n[bold green]Starting Interactive Mode[/bold green]")
    console.print("Type 'help' for commands, 'exit' to quit\n")

    model_loader = components['model_loader']
    memory = components['memory']
    apis = components['apis']

    # Load model for interactive use
    if model_loader.model is None:
        console.print("Loading model...")
        model_loader.load_base_model()

    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ")

            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yellow]Goodbye![/yellow]")
                break

            elif user_input.lower() == 'help':
                console.print("""
[bold]Available commands:[/bold]
  learn <n>     - Run n learning iterations
  stats         - Show knowledge base statistics
  ask <query>   - Ask the AI a question
  search <query>- Search the knowledge base
  modify <goal> - Propose a self-modification
  exit/quit     - Exit the program
""")

            elif user_input.lower().startswith('learn'):
                parts = user_input.split()
                n = int(parts[1]) if len(parts) > 1 else 1
                run_learning_mode(components, iterations=n)

            elif user_input.lower() == 'stats':
                stats = memory.get_stats()
                console.print(f"\n[cyan]Knowledge Base:[/cyan]")
                console.print(f"  Total items: {stats['total_items']}")
                console.print(f"  Sources: {stats['sources']}\n")

            elif user_input.lower().startswith('ask'):
                query = user_input[4:].strip()
                if query:
                    # Get context from memory
                    context = memory.retrieve_context(query)

                    # Generate response
                    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
                    response = model_loader.generate(prompt, max_length=512)

                    console.print(f"\n[bold green]AI:[/bold green] {response}\n")

            elif user_input.lower().startswith('search'):
                query = user_input[7:].strip()
                if query:
                    results = memory.search(query, n_results=3)
                    console.print(f"\n[cyan]Search results for '{query}':[/cyan]\n")
                    for i, result in enumerate(results, 1):
                        console.print(f"{i}. {result['text'][:200]}...")
                        console.print(f"   Source: {result['metadata'].get('source', 'unknown')}\n")

            elif user_input.lower().startswith('modify'):
                goal = user_input[7:].strip()
                if goal:
                    result = components['self_modifier'].propose_and_test_modification(goal)
                    if result['success']:
                        console.print("[green]✓ Modification successful![/green]")
                    else:
                        console.print(f"[red]✗ Failed: {result.get('reason')}[/red]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Self-Learning AI System")
    parser.add_argument(
        '--mode',
        choices=['learn', 'modify', 'interactive'],
        default='interactive',
        help='Operation mode'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=5,
        help='Number of learning iterations (for learn mode)'
    )

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Initialize system
    components = initialize_system()

    # Run in selected mode
    if args.mode == 'learn':
        run_learning_mode(components, iterations=args.iterations)
    elif args.mode == 'modify':
        run_self_modification_mode(components)
    else:
        run_interactive_mode(components)


if __name__ == "__main__":
    main()
