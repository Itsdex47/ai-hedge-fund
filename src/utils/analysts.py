"""Constants and utilities related to analyst configuration.

Scoped to the valuation-challenge pivot: the registry holds the methods used
to reconstruct an independent value, not trading signal generators. Each entry
becomes a graph node via get_analyst_nodes().
"""

from src.agents.fundamentals import fundamentals_analyst_agent
from src.agents.valuation import valuation_analyst_agent

ANALYST_CONFIG = {
    "fundamentals_analyst": {
        "display_name": "Fundamentals Analyst",
        "description": "Financial Statement Specialist",
        "investing_style": "Deep dive into financial statements and metrics",
        "agent_func": fundamentals_analyst_agent,
        "type": "analyst",
        "order": 0,
    },
    "valuation_analyst": {
        "display_name": "Valuation Analyst",
        "description": "Intrinsic Value Specialist",
        "investing_style": "DCF, owner earnings, and other valuation models",
        "agent_func": valuation_analyst_agent,
        "type": "analyst",
        "order": 1,
    },
}

# Display order for analyst selection
ANALYST_ORDER = [
    ("Fundamentals Analyst", "fundamentals_analyst"),
    ("Valuation Analyst", "valuation_analyst"),
]

# Strategy presets
STRATEGIES = {
    "valuation": {
        "name": "Valuation",
        "description": "Multi-method intrinsic value reconstruction",
        "analysts": ["fundamentals_analyst", "valuation_analyst"],
    },
    "all": {
        "name": "All Analysts",
        "description": "Use every registered method",
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
