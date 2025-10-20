"""Constants and utilities related to analysts configuration - SIMPLIFIED VERSION."""

from src.agents import portfolio_manager
from src.agents.fundamentals import fundamentals_analyst_agent
from src.agents.peter_lynch import peter_lynch_agent
from src.agents.sentiment import sentiment_analyst_agent
from src.agents.technicals import technical_analyst_agent
from src.agents.valuation import valuation_analyst_agent
from src.agents.warren_buffett import warren_buffett_agent

# Simplified analyst configuration - 6 core analysts only
ANALYST_CONFIG = {
    "warren_buffett": {
        "display_name": "Warren Buffett",
        "description": "The Oracle of Omaha",
        "investing_style": "Value investing focused on strong fundamentals and competitive advantages",
        "agent_func": warren_buffett_agent,
        "type": "analyst",
        "order": 0,
    },
    "peter_lynch": {
        "display_name": "Peter Lynch",
        "description": "The 10-Bagger Hunter",
        "investing_style": "Growth at reasonable price - 'buy what you know' strategy",
        "agent_func": peter_lynch_agent,
        "type": "analyst",
        "order": 1,
    },
    "technical_analyst": {
        "display_name": "Technical Analyst",
        "description": "Chart Pattern Specialist",
        "investing_style": "Technical analysis using charts, trends, and momentum indicators",
        "agent_func": technical_analyst_agent,
        "type": "analyst",
        "order": 2,
    },
    "fundamentals_analyst": {
        "display_name": "Fundamentals Analyst",
        "description": "Financial Statement Specialist",
        "investing_style": "Deep dive into financial statements and metrics",
        "agent_func": fundamentals_analyst_agent,
        "type": "analyst",
        "order": 3,
    },
    "sentiment_analyst": {
        "display_name": "Sentiment Analyst",
        "description": "Market Sentiment Specialist",
        "investing_style": "Analyzes market sentiment, news, and insider trading",
        "agent_func": sentiment_analyst_agent,
        "type": "analyst",
        "order": 4,
    },
    "valuation_analyst": {
        "display_name": "Valuation Analyst",
        "description": "Intrinsic Value Specialist",
        "investing_style": "DCF, owner earnings, and other valuation models",
        "agent_func": valuation_analyst_agent,
        "type": "analyst",
        "order": 5,
    },
}

# Display order for analyst selection
ANALYST_ORDER = [
    ("Warren Buffett", "warren_buffett"),
    ("Peter Lynch", "peter_lynch"),
    ("Technical Analyst", "technical_analyst"),
    ("Fundamentals Analyst", "fundamentals_analyst"),
    ("Sentiment Analyst", "sentiment_analyst"),
    ("Valuation Analyst", "valuation_analyst"),
]

# Strategy presets
STRATEGIES = {
    "conservative": {
        "name": "Conservative",
        "description": "Value-focused with strong fundamentals",
        "analysts": ["warren_buffett", "fundamentals_analyst", "valuation_analyst"],
    },
    "growth": {
        "name": "Growth",
        "description": "Growth opportunities with momentum",
        "analysts": ["peter_lynch", "technical_analyst", "sentiment_analyst"],
    },
    "balanced": {
        "name": "Balanced",
        "description": "Mix of value, growth, and technical analysis",
        "analysts": ["warren_buffett", "peter_lynch", "technical_analyst", "valuation_analyst"],
    },
    "all": {
        "name": "All Analysts",
        "description": "Use all 6 analysts for comprehensive analysis",
        "analysts": list(ANALYST_CONFIG.keys()),
    },
}


def get_analyst_nodes():
    """Get the mapping of analyst keys to their (node_name, agent_func) tuples."""
    return {key: (f"{key}_agent", config["agent_func"]) for key, config in ANALYST_CONFIG.items()}


def get_agents_list():
    """Get the list of agents for API responses."""
    return [
        {
            "key": key,
            "display_name": config["display_name"],
            "description": config["description"],
            "investing_style": config["investing_style"],
            "order": config["order"],
        }
        for key, config in sorted(ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])
    ]


def get_strategy_analysts(strategy_name: str) -> list[str]:
    """Get the list of analyst keys for a given strategy."""
    strategy = STRATEGIES.get(strategy_name)
    if not strategy:
        return list(ANALYST_CONFIG.keys())  # Default to all
    return strategy["analysts"]
