"""Simplified LLM Model Configuration - Top 3 providers only."""

import os
import json
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from enum import Enum
from pydantic import BaseModel
from typing import Tuple, List
from pathlib import Path


class ModelProvider(str, Enum):
    """Enum for supported LLM providers - SIMPLIFIED TO TOP 3"""
    ANTHROPIC = "Anthropic"
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"


class LLMModel(BaseModel):
    """Represents an LLM model configuration"""
    display_name: str
    model_name: str
    provider: ModelProvider

    def to_choice_tuple(self) -> Tuple[str, str, str]:
        """Convert to format needed for questionary choices"""
        return (self.display_name, self.model_name, self.provider.value)

    def is_custom(self) -> bool:
        """Check if the model allows custom names"""
        return self.model_name == "-"

    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        if self.is_ollama():
            return "llama3" in self.model_name or "neural-chat" in self.model_name
        return True

    def is_ollama(self) -> bool:
        """Check if the model is an Ollama model"""
        return self.provider == ModelProvider.OLLAMA


# Simplified model list - top performing models only
AVAILABLE_MODELS = [
    LLMModel(display_name="GPT-4o (OpenAI) - Best Overall", model_name="gpt-4o", provider=ModelProvider.OPENAI),
    LLMModel(display_name="GPT-4o Mini (OpenAI) - Fast & Cheap", model_name="gpt-4o-mini", provider=ModelProvider.OPENAI),
    LLMModel(display_name="Claude 3.5 Sonnet (Anthropic) - Best Reasoning", model_name="claude-3-5-sonnet-latest", provider=ModelProvider.ANTHROPIC),
    LLMModel(display_name="Claude 3.5 Haiku (Anthropic) - Fast", model_name="claude-3-5-haiku-latest", provider=ModelProvider.ANTHROPIC),
]

OLLAMA_MODELS = [
    LLMModel(display_name="Llama 3.1 8B (Local)", model_name="llama3.1:8b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="Llama 3.1 70B (Local)", model_name="llama3.1:70b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="Custom Ollama Model", model_name="-", provider=ModelProvider.OLLAMA),
]

# Create LLM_ORDER in the format expected by the UI
LLM_ORDER = [model.to_choice_tuple() for model in AVAILABLE_MODELS]
OLLAMA_LLM_ORDER = [model.to_choice_tuple() for model in OLLAMA_MODELS]


def get_model_info(model_name: str, model_provider: str) -> LLMModel | None:
    """Get model information by model_name"""
    all_models = AVAILABLE_MODELS + OLLAMA_MODELS
    return next((model for model in all_models if model.model_name == model_name and model.provider == model_provider), None)


def get_models_list():
    """Get the list of models for API responses."""
    return [
        {
            "display_name": model.display_name,
            "model_name": model.model_name,
            "provider": model.provider.value
        }
        for model in AVAILABLE_MODELS
    ]


def get_model(model_name: str, model_provider: ModelProvider, api_keys: dict = None) -> ChatOpenAI | ChatAnthropic | ChatOllama | None:
    """Get the appropriate LLM model based on provider."""
    if model_provider == ModelProvider.OPENAI:
        api_key = (api_keys or {}).get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        if not api_key:
            print(f"❌ Error: OPENAI_API_KEY not found in .env file")
            raise ValueError("OpenAI API key required. Add OPENAI_API_KEY to your .env file.")
        return ChatOpenAI(model=model_name, api_key=api_key, base_url=base_url)

    elif model_provider == ModelProvider.ANTHROPIC:
        api_key = (api_keys or {}).get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print(f"❌ Error: ANTHROPIC_API_KEY not found in .env file")
            raise ValueError("Anthropic API key required. Add ANTHROPIC_API_KEY to your .env file.")
        return ChatAnthropic(model=model_name, api_key=api_key)

    elif model_provider == ModelProvider.OLLAMA:
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        base_url = os.getenv("OLLAMA_BASE_URL", f"http://{ollama_host}:11434")
        return ChatOllama(model=model_name, base_url=base_url)

    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")
