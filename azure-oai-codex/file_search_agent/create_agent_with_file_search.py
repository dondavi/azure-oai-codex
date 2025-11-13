#!/usr/bin/env python3
"""
Create an Azure AI Agent wired to Azure AI Search via the file_search tool.
Requires env vars:
  AZURE_AI_ENDPOINT
  AZURE_AI_PROJECT_NAME
  AZURE_AI_KEY
  AZURE_AI_SEARCH_CONNECTION_ID
  AZURE_AI_SEARCH_INDEX_NAME
Optional tweak MODEL_NAME to match your deployment.
"""

import json
import os
import sys
from typing import Final

import requests

API_VERSION: Final = "2024-05-01-preview"
MODEL_NAME: Final = "gpt-4o-mini"


def env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value.strip()


def main() -> None:
    endpoint = env("AZURE_AI_ENDPOINT").rstrip("/")
    project = env("AZURE_AI_PROJECT_NAME")
    api_key = env("AZURE_AI_KEY")
    connection_id = env("AZURE_AI_SEARCH_CONNECTION_ID")
    index_name = env("AZURE_AI_SEARCH_INDEX_NAME")

    url = f"{endpoint}/openai/projects/{project}/agents?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    payload = {
        "name": "file-search-agent",
        "description": "Answers questions using documents indexed in Azure AI Search.",
        "instructions": (
            "You are a helpful assistant. Search the knowledge base through the file_search tool "
            "before answering so responses stay grounded in indexed content."
        ),
        "model": MODEL_NAME,
        "tools": [
            {"type": "file_search"}
        ],
        "tool_resources": {
            "file_search": [
                {
                    "connection_id": connection_id,
                    "index_name": index_name,
                    # Uncomment and tailor if your index uses custom field names.
                    # "fields_mapping": {
                    #     "content_field": "content",
                    #     "title_field": "title",
                    #     "url_field": "sourceurl",
                    #     "vector_fields": ["content_vector"]
                    # }
                }
            ]
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
    except requests.HTTPError as err:
        print("Request failed:", err, file=sys.stderr)
        if err.response is not None:
            print("Response body:", err.response.text, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
