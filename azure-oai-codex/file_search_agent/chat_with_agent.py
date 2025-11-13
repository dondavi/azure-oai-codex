#!/usr/bin/env python3
"""
Create a session and send a prompt to an existing Azure AI Agent.
Requires env vars:
  AZURE_AI_ENDPOINT
  AZURE_AI_PROJECT_NAME
  AZURE_AI_KEY
  AZURE_AI_AGENT_ID
"""

import json
import os
import sys
from typing import Final

import requests

API_VERSION: Final = "2024-05-01-preview"


def env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value.strip()


def create_session(endpoint: str, project: str, agent_id: str, headers: dict) -> str:
    url = f"{endpoint}/openai/projects/{project}/agents/{agent_id}/sessions?api-version={API_VERSION}"
    response = requests.post(url, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data["id"]


def send_message(endpoint: str, project: str, agent_id: str, session_id: str, headers: dict, user_text: str) -> dict:
    url = (
        f"{endpoint}/openai/projects/{project}/agents/{agent_id}/sessions/"
        f"{session_id}/responses?api-version={API_VERSION}"
    )
    payload = {
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


def main() -> None:
    endpoint = env("AZURE_AI_ENDPOINT").rstrip("/")
    project = env("AZURE_AI_PROJECT_NAME")
    api_key = env("AZURE_AI_KEY")
    agent_id = env("AZURE_AI_AGENT_ID")

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    session_id = create_session(endpoint, project, agent_id, headers)
    print(f"Session created: {session_id}")

    try:
        user_prompt = input("Ask the agent: ").strip()
    except EOFError:
        sys.exit("No prompt provided.")

    if not user_prompt:
        sys.exit("No prompt provided.")

    result = send_message(endpoint, project, agent_id, session_id, headers, user_prompt)

    print("\nAgent response:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
