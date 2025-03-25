"""Test script for OpenRouter and Google Gemini API integration."""

import os

from dotenv import load_dotenv
from google import genai
from openai import OpenAI

# Load environment variables
load_dotenv()


def get_openrouter_response(prompt: str) -> str:
    """Get response from OpenRouter API.

    Args:
        prompt: The input prompt for the model

    Returns:
        The model's response text

    Raises:
        Exception: If API call fails
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": os.getenv("SITE_URL"),
                "X-Title": os.getenv("SITE_NAME"),
            },
            extra_body={},
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        return ""
    else:
        return completion.choices[0].message.content


def get_gemini_response(prompt: str) -> str:
    """Get response from Google's Gemini API.

    Args:
        prompt: The input prompt for the model

    Returns:
        The model's response text

    Raises:
        Exception: If API call fails
    """
    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
    except Exception as e:
        print(f"Gemini API error: {e}")
        return ""
    else:
        return response.text


def main() -> None:
    """Run API tests."""
    # Test OpenRouter
    print("\nTesting OpenRouter API:")
    print("-" * 50)
    openrouter_response = get_openrouter_response("What is the meaning of life?")
    if openrouter_response:
        print("OpenRouter Response:")
        print(openrouter_response)

    # Test Gemini
    print("\nTesting Gemini API:")
    print("-" * 50)
    gemini_response = get_gemini_response("Explain how AI works")
    if gemini_response:
        print("Gemini Response:")
        print(gemini_response)


if __name__ == "__main__":
    main()
