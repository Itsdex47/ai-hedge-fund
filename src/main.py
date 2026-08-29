import sys
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from colorama import Fore, Style, init
import questionary
from src.agents.portfolio_manager import portfolio_management_agent
from src.agents.risk_manager import risk_management_agent
from src.graph.state import AgentState
from src.utils.display import print_trading_output
from src.utils.analysts import ANALYST_ORDER, get_analyst_nodes, STRATEGIES, get_strategy_analysts
from src.utils.progress import progress
from src.llm.models import LLM_ORDER, OLLAMA_LLM_ORDER, get_model_info, ModelProvider
from src.utils.ollama import ensure_ollama_and_model

import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)


def parse_hedge_fund_response(response):
    """Parses a JSON string and returns a dictionary."""
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}\nResponse: {repr(response)}")
        return None
    except TypeError as e:
        print(f"Invalid response type (expected string, got {type(response).__name__}): {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while parsing response: {e}\nResponse: {repr(response)}")
        return None


##### Run the Hedge Fund #####
def run_hedge_fund(
    tickers: list[str],
    start_date: str,
    end_date: str,
    portfolio: dict,
    show_reasoning: bool = False,
    selected_analysts: list[str] = [],
    model_name: str = "gpt-4.1",
    model_provider: str = "OpenAI",
):
    # Start progress tracking
    progress.start()

    try:
        # Create a new workflow if analysts are customized
        if selected_analysts:
            workflow = create_workflow(selected_analysts)
            agent = workflow.compile()
        else:
            # Create default workflow with all analysts
            workflow = create_workflow()
            agent = workflow.compile()

        final_state = agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content="Make trading decisions based on the provided data.",
                    )
                ],
                "data": {
                    "tickers": tickers,
                    "portfolio": portfolio,
                    "start_date": start_date,
                    "end_date": end_date,
                    "analyst_signals": {},
                },
                "metadata": {
                    "show_reasoning": show_reasoning,
                    "model_name": model_name,
                    "model_provider": model_provider,
                },
            },
        )

        return {
            "decisions": parse_hedge_fund_response(final_state["messages"][-1].content),
            "analyst_signals": final_state["data"]["analyst_signals"],
        }
    finally:
        # Stop progress tracking
        progress.stop()


def start(state: AgentState):
    """Initialize the workflow with the input message."""
    return state


def create_workflow(selected_analysts=None):
    """Create the workflow with selected analysts."""
    workflow = StateGraph(AgentState)
    workflow.add_node("start_node", start)

    # Get analyst nodes from the configuration
    analyst_nodes = get_analyst_nodes()

    # Default to all analysts if none selected
    if selected_analysts is None:
        selected_analysts = list(analyst_nodes.keys())
    # Add selected analyst nodes
    for analyst_key in selected_analysts:
        node_name, node_func = analyst_nodes[analyst_key]
        workflow.add_node(node_name, node_func)
        workflow.add_edge("start_node", node_name)

    # Always add risk and portfolio management
    workflow.add_node("risk_management_agent", risk_management_agent)
    workflow.add_node("portfolio_manager", portfolio_management_agent)

    # Connect selected analysts to risk management
    for analyst_key in selected_analysts:
        node_name = analyst_nodes[analyst_key][0]
        workflow.add_edge(node_name, "risk_management_agent")

    workflow.add_edge("risk_management_agent", "portfolio_manager")
    workflow.add_edge("portfolio_manager", END)

    workflow.set_entry_point("start_node")
    return workflow


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🤖 AI Hedge Fund - SIMPLIFIED VERSION\nAnalyze stocks using AI investor agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use a strategy preset
  python src/main.py --tickers AAPL --strategy valuation

  # Use all registered methods (default)
  python src/main.py --tickers AAPL,MSFT,GOOGL

  # Show detailed reasoning
  python src/main.py --tickers AAPL --show-reasoning

Available Strategies:
  valuation - Multi-method intrinsic value reconstruction
  all       - Use every registered method
        """
    )
    parser.add_argument("--tickers", type=str, help="Comma-separated list of stock ticker symbols")
    parser.add_argument("--strategy", type=str, choices=list(STRATEGIES.keys()), help="Strategy preset (valuation/all)")
    parser.add_argument("--initial-cash", type=float, default=100000.0, help="Initial cash position (default: $100,000)")
    parser.add_argument("--margin-requirement", type=float, default=0.0, help="Margin requirement (default: 0.0)")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD). Defaults to 3 months ago")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD). Defaults to today")
    parser.add_argument("--show-reasoning", action="store_true", help="Show detailed reasoning from each agent")
    parser.add_argument("--ollama", action="store_true", help="Use local Ollama models")
    parser.add_argument("--profile", type=str, help="User profile name for personalized analysis (e.g., 'Conservative Retirement')")
    parser.add_argument("--list-profiles", action="store_true", help="List available user profiles and exit")

    args = parser.parse_args()

    # Handle --list-profiles
    if args.list_profiles:
        from src.user.profile import list_profiles
        profiles = list_profiles()
        if profiles:
            print(f"\n{Fore.CYAN}📋 Available Profiles:{Style.RESET_ALL}\n")
            for profile_name in profiles:
                print(f"  • {profile_name}")
            print(f"\n{Fore.WHITE}Usage: python src/main.py --tickers AAPL --profile \"Conservative Retirement\"{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}No profiles found. Create one with:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  python -c 'from src.user.profile import create_default_profiles; create_default_profiles()'{Style.RESET_ALL}\n")
        sys.exit(0)

    # Check that tickers are provided
    if not args.tickers:
        print(f"\n{Fore.RED}❌ Error: --tickers argument is required{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}Usage: python src/main.py --tickers AAPL,MSFT{Style.RESET_ALL}\n")
        sys.exit(1)

    # Parse tickers from comma-separated string
    tickers = [ticker.strip().upper() for ticker in args.tickers.split(",")]

    # Load user profile if specified
    user_profile = None
    preference_filter = None
    if args.profile:
        from src.user.profile import get_profile
        from src.user.preferences import PreferenceFilter

        user_profile = get_profile(args.profile)
        if not user_profile:
            print(f"\n{Fore.RED}❌ Error: Profile '{args.profile}' not found.{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Use --list-profiles to see available profiles.{Style.RESET_ALL}\n")
            sys.exit(1)

        preference_filter = PreferenceFilter(user_profile)

        # Display profile info
        print(f"\n{Fore.CYAN}👤 Using Profile: {user_profile.profile_name}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Risk Tolerance: {user_profile.risk_tolerance.title()}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Time Horizon: {user_profile.time_horizon} years{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Primary Objective: {user_profile.primary_objective.replace('_', ' ').title()}{Style.RESET_ALL}")

        if user_profile.exclude_sectors:
            print(f"{Fore.YELLOW}  ⚠️  Excluding sectors: {', '.join(user_profile.exclude_sectors)}{Style.RESET_ALL}")

        # Filter tickers based on preferences
        filtered_tickers = []
        for ticker in tickers:
            is_allowed, reason = preference_filter.is_ticker_allowed(ticker)
            if is_allowed:
                filtered_tickers.append(ticker)
            else:
                print(f"{Fore.RED}  ❌ Filtered out {ticker}: {reason}{Style.RESET_ALL}")

        if not filtered_tickers:
            print(f"\n{Fore.RED}❌ All tickers were filtered out by your preferences.{Style.RESET_ALL}\n")
            sys.exit(1)

        tickers = filtered_tickers
        print()

    # Select analysts based on strategy or interactive mode
    selected_analysts = None

    if args.strategy:
        # Use strategy preset
        selected_analysts = get_strategy_analysts(args.strategy)
        strategy_info = STRATEGIES[args.strategy]
        print(f"\n{Fore.CYAN}📊 Strategy: {strategy_info['name']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{strategy_info['description']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Using analysts: {', '.join(selected_analysts)}{Style.RESET_ALL}\n")
    elif sys.stdin.isatty():
        # Interactive mode: let user choose
        choices = questionary.checkbox(
            "Select your AI analysts (or use --strategy flag for presets):",
            choices=[questionary.Choice(display, value=value) for display, value in ANALYST_ORDER],
            instruction="\nPress Space to select, Enter to confirm (or Ctrl+C to exit)",
            validate=lambda x: len(x) > 0 or "You must select at least one analyst.",
            style=questionary.Style(
                [
                    ("checkbox-selected", "fg:green"),
                    ("selected", "fg:green noinherit"),
                    ("highlighted", "noinherit"),
                    ("pointer", "noinherit"),
                ]
            ),
        ).ask()

        if not choices:
            print("\n\nExiting...")
            sys.exit(0)
        else:
            selected_analysts = choices
            print(f"\n{Fore.GREEN}Selected analysts: {', '.join(choices)}{Style.RESET_ALL}\n")
    else:
        # Non-interactive mode: use all analysts
        selected_analysts = [value for _, value in ANALYST_ORDER]
        print(f"{Fore.CYAN}Using all 6 analysts{Style.RESET_ALL}\n")

    # Select LLM model based on whether Ollama is being used
    model_name = ""
    model_provider = ""

    if args.ollama:
        print(f"{Fore.CYAN}Using Ollama for local LLM inference.{Style.RESET_ALL}")

        if sys.stdin.isatty():
            # Select from Ollama-specific models
            model_name: str = questionary.select(
                "Select your Ollama model:",
                choices=[questionary.Choice(display, value=value) for display, value, _ in OLLAMA_LLM_ORDER],
                style=questionary.Style(
                    [
                        ("selected", "fg:green bold"),
                        ("pointer", "fg:green bold"),
                        ("highlighted", "fg:green"),
                        ("answer", "fg:green bold"),
                    ]
                ),
            ).ask()

            if not model_name:
                print("\n\nInterrupt received. Exiting...")
                sys.exit(0)

            if model_name == "-":
                model_name = questionary.text("Enter the custom model name:").ask()
                if not model_name:
                    print("\n\nInterrupt received. Exiting...")
                    sys.exit(0)
        else:
            # Non-interactive mode: use first Ollama model
            model_name = OLLAMA_LLM_ORDER[0][1]  # Get the value from first option
            print(f"{Fore.YELLOW}Running in non-interactive mode. Using default Ollama model: {model_name}{Style.RESET_ALL}")

        # Ensure Ollama is installed, running, and the model is available
        if not ensure_ollama_and_model(model_name):
            print(f"{Fore.RED}Cannot proceed without Ollama and the selected model.{Style.RESET_ALL}")
            sys.exit(1)

        model_provider = ModelProvider.OLLAMA.value
        print(f"\nSelected {Fore.CYAN}Ollama{Style.RESET_ALL} model: {Fore.GREEN + Style.BRIGHT}{model_name}{Style.RESET_ALL}\n")
    else:
        if sys.stdin.isatty():
            # Use the standard cloud-based LLM selection
            model_choice = questionary.select(
                "Select your LLM model:",
                choices=[questionary.Choice(display, value=(name, provider)) for display, name, provider in LLM_ORDER],
                style=questionary.Style(
                    [
                        ("selected", "fg:green bold"),
                        ("pointer", "fg:green bold"),
                        ("highlighted", "fg:green"),
                        ("answer", "fg:green bold"),
                    ]
                ),
            ).ask()

            if not model_choice:
                print("\n\nInterrupt received. Exiting...")
                sys.exit(0)

            model_name, model_provider = model_choice

            # Get model info using the helper function
            model_info = get_model_info(model_name, model_provider)
            if model_info:
                if model_info.is_custom():
                    model_name = questionary.text("Enter the custom model name:").ask()
                    if not model_name:
                        print("\n\nInterrupt received. Exiting...")
                        sys.exit(0)

                print(f"\nSelected {Fore.CYAN}{model_provider}{Style.RESET_ALL} model: {Fore.GREEN + Style.BRIGHT}{model_name}{Style.RESET_ALL}\n")
            else:
                model_provider = "Unknown"
                print(f"\nSelected model: {Fore.GREEN + Style.BRIGHT}{model_name}{Style.RESET_ALL}\n")
        else:
            # Non-interactive mode: use first cloud model
            model_name = LLM_ORDER[0][1]  # model name
            model_provider = LLM_ORDER[0][2]  # provider
            print(f"{Fore.YELLOW}Running in non-interactive mode. Using default model: {model_name} ({model_provider}){Style.RESET_ALL}\n")

    # Create the workflow with selected analysts
    workflow = create_workflow(selected_analysts)
    app = workflow.compile()

    # Validate dates if provided
    if args.start_date:
        try:
            datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format")

    if args.end_date:
        try:
            datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in YYYY-MM-DD format")

    # Set the start and end dates
    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")
    if not args.start_date:
        # Calculate 3 months before end_date
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = (end_date_obj - relativedelta(months=3)).strftime("%Y-%m-%d")
    else:
        start_date = args.start_date

    # Initialize portfolio with cash amount and stock positions
    portfolio = {
        "cash": args.initial_cash,  # Initial cash amount
        "margin_requirement": args.margin_requirement,  # Initial margin requirement
        "margin_used": 0.0,  # total margin usage across all short positions
        "positions": {
            ticker: {
                "long": 0,  # Number of shares held long
                "short": 0,  # Number of shares held short
                "long_cost_basis": 0.0,  # Average cost basis for long positions
                "short_cost_basis": 0.0,  # Average price at which shares were sold short
                "short_margin_used": 0.0,  # Dollars of margin used for this ticker's short
            }
            for ticker in tickers
        },
        "realized_gains": {
            ticker: {
                "long": 0.0,  # Realized gains from long positions
                "short": 0.0,  # Realized gains from short positions
            }
            for ticker in tickers
        },
    }

    # Run the hedge fund
    result = run_hedge_fund(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        portfolio=portfolio,
        show_reasoning=args.show_reasoning,
        selected_analysts=selected_analysts,
        model_name=model_name,
        model_provider=model_provider,
    )
    print_trading_output(result)
