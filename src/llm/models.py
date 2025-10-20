"""Simplified LLM Model Configuration - Latest models + Your Ollama setup."""

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
            return "llama3" in self.model_name or "gpt-oss" in self.model_name
        return True

    def is_ollama(self) -> bool:
        """Check if the model is an Ollama model"""
        return self.provider == ModelProvider.OLLAMA


# Latest and greatest models - Updated January 2025
AVAILABLE_MODELS = [
    # OpenAI - Latest GPT-4 models
    LLMModel(display_name="GPT-4o (Latest) - Best Overall", model_name="gpt-4o", provider=ModelProvider.OPENAI),
    LLMModel(display_name="GPT-4o Mini - Fast & Cheap", model_name="gpt-4o-mini", provider=ModelProvider.OPENAI),
    LLMModel(display_name="o1 (Reasoning) - Advanced", model_name="o1", provider=ModelProvider.OPENAI),
    LLMModel(display_name="o1-mini (Reasoning) - Faster", model_name="o1-mini", provider=ModelProvider.OPENAI),

    # Anthropic - Latest Claude models (Sonnet 4 is newest as of Jan 2025)
    LLMModel(display_name="Claude Sonnet 4 (Latest) - Best Reasoning", model_name="claude-sonnet-4-20250514", provider=ModelProvider.ANTHROPIC),
    LLMModel(display_name="Claude Sonnet 3.7 - Very Good", model_name="claude-3-7-sonnet-20250219", provider=ModelProvider.ANTHROPIC),
    LLMModel(display_name="Claude Opus 4 - Most Powerful", model_name="claude-opus-4-20250514", provider=ModelProvider.ANTHROPIC),
]

# Your locally installed Ollama models
OLLAMA_MODELS = [
    LLMModel(display_name="GPT-OSS 20B Cloud (Your Model) - Recommended", model_name="gpt-oss:20b-cloud", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="GPT-OSS 20B (Your Model)", model_name="gpt-oss:20b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="Llama 3.1 (Your Model)", model_name="llama3.1:latest", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="Qwen 3 30B (Your Model)", model_name="qwen3:30b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="Gemma 3 12B (Your Model)", model_name="gemma3:12b", provider=ModelProvider.OLLAMA),
    LLMModel(display_name="DeepSeek R1 8B (Your Model)", model_name="deepseek-r1:8b", provider=ModelProvider.OLLAMA),
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
        print(f"🤖 Using Ollama model: {model_name}")
        return ChatOllama(model=model_name, base_url=base_url)

    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")
