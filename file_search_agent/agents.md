# Azure AI Agents Toolkit

## Overview
This repo provides two helper scripts for managing Azure AI Agents with Azure AI Search grounding:
- `create_agent_with_file_search.py` provisions an agent that can query an Azure AI Search index through the `file_search` tool.
- `chat_with_agent.py` starts an ad hoc session with an existing agent and sends a single user prompt.

## Prerequisites
- Python 3.8+
- `requests` Python package (`pip install requests`)
- Azure OpenAI resource configured with the Agents API preview (2024-05-01-preview)
- Existing Azure AI Search connection attached to the same Azure OpenAI project

## Required Environment Variables
Export these before running either script:
- `AZURE_AI_ENDPOINT` – your Azure OpenAI endpoint (e.g. `https://contoso.openai.azure.com`).
- `AZURE_AI_PROJECT_NAME` – the project that contains your agents and search connections.
- `AZURE_AI_KEY` – Azure OpenAI API key with access to the project.
- `AZURE_AI_SEARCH_CONNECTION_ID` – resource ID for the Azure AI Search connection (create script only).
- `AZURE_AI_SEARCH_INDEX_NAME` – name of the search index to query (create script only).
- `AZURE_AI_AGENT_ID` – identifier of the agent you wish to chat with (chat script only).

## Usage
### Create an agent wired to Azure AI Search
```bash
export AZURE_AI_ENDPOINT="https://contoso.openai.azure.com"
export AZURE_AI_PROJECT_NAME="support-portal"
export AZURE_AI_KEY="<api-key>"
export AZURE_AI_SEARCH_CONNECTION_ID="/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Search/searchServices/<svc>"
export AZURE_AI_SEARCH_INDEX_NAME="kb-index"
python create_agent_with_file_search.py
```
The script returns the newly created agent payload; capture the `id` for use with the chat helper.

### Chat with an existing agent
```bash
export AZURE_AI_ENDPOINT="https://contoso.openai.azure.com"
export AZURE_AI_PROJECT_NAME="support-portal"
export AZURE_AI_KEY="<api-key>"
export AZURE_AI_AGENT_ID="agent_123"
python chat_with_agent.py
```
Enter a prompt when prompted; the script prints the JSON response from the session call.

## Customization Tips
- Change `MODEL_NAME` in `create_agent_with_file_search.py` to point at your preferred model deployment.
- Uncomment and adjust the `fields_mapping` block to align with your Azure AI Search index schema.
- Extend `chat_with_agent.py` with streaming support by setting `stream=True` on the POST request and iterating over chunks.

## Troubleshooting
- `401 Unauthorized`: confirm the API key and that the project allows agent operations.
- `404 Not Found`: verify the project name, agent id, and connection identifiers.
- `429 Too Many Requests`: throttle requests or review service quotas.
