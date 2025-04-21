"""Test script for OpenRouter and Google Gemini API integration."""

import json
import os

import google.generativeai as genai
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model names from environment
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")


class ModelResponse(BaseModel):
    """Structured response from AI models."""

    model_name: str = Field(..., description="Name of the AI model")
    response_text: str = Field("", description="Raw response from the model")
    error: str | None = Field(None, description="Error message if any")
    latency_ms: float = Field(..., description="Response time in milliseconds")


def get_openrouter_response(prompt: str) -> ModelResponse:
    import time

    start_time = time.time()
    model_name = OPENROUTER_MODEL

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": os.getenv("SITE_URL") or "",
                "X-Title": os.getenv("SITE_NAME") or "",
            },
            extra_body={},
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        return ModelResponse(
            model_name=model_name,
            response_text="",
            error=str(e),
            latency_ms=(time.time() - start_time) * 1000,
        )
    else:
        return ModelResponse(
            model_name=model_name,
            response_text=str(completion.choices[0].message.content),
            error=None,
            latency_ms=(time.time() - start_time) * 1000,
        )


def get_gemini_response(prompt: str) -> ModelResponse:
    """Get response from Google's Gemini API."""
    import time

    start_time = time.time()
    model_name = "gemini-2.0-flash"
    api_key = os.getenv("GOOGLE_API_KEY")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(f"{url}?key={api_key}", headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()

        # Extract the response text from the result
        response_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        return ModelResponse(
            model_name=model_name,
            response_text=response_text,
            error=None,
            latency_ms=(time.time() - start_time) * 1000,
        )
    except Exception as e:
        return ModelResponse(
            model_name=model_name,
            response_text="",
            error=str(e),
            latency_ms=(time.time() - start_time) * 1000,
        )


def main() -> None:
    """Run API tests with structured output."""
    prompt = "What is the meaning of life?"
    responses = []

    # Test both models
    print(f"\nAsking both models: {prompt}")
    print("-" * 50)

    # Get responses
    responses.append(get_openrouter_response(prompt))
    responses.append(get_gemini_response(prompt))

    # Print structured output
    print("\nStructured Responses:")
    print(json.dumps([r.model_dump() for r in responses], indent=2))

    # Print comparison
    print("\nComparison:")
    for response in responses:
        print(f"\n{response.model_name}:")
        print("-" * 50)
        if response.error:
            print(f"Error: {response.error}")
        else:
            print(f"Response: {response.response_text}")
        print(f"Latency: {response.latency_ms:.2f}ms")


if __name__ == "__main__":
    main()
