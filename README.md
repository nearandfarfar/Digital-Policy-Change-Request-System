# digital_policy_change_request_system Flow

This project defines a declarative CrewAI Flow in `src/digital_policy_change_request_system/flow.yaml`.

## Install

```bash
crewai install
```

## Run

```bash
crewai run
```

Edit the declarative flow definition at `src/digital_policy_change_request_system/flow.yaml` to change the flow. Add reusable crews under `src/digital_policy_change_request_system/crews/`, custom Python tools under `src/digital_policy_change_request_system/tools/`, and shared knowledge files under `src/digital_policy_change_request_system/knowledge/`.

## Environment Configuration

This application supports both local and cloud-based CrewAI workflow execution.

Before running the application:

1. Clone the GitHub repository.
2. Copy `.env.example` to a new file named `.env`.
3. Open `.env` and enter your own API credentials and CrewAI Cloud deployment URL.
4. Set `CREWAI_EXECUTION_MODE` to `local` or `cloud`.
5. Save the file.

**Configuration variables**

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key used for local CrewAI execution |
| `CREWAI_CLOUD_URL` | URL of your deployed CrewAI Cloud application |
| `CREWAI_BEARER_TOKEN` | Bearer Token for authenticating CrewAI Cloud API requests |
| `CREWAI_EXECUTION_MODE` | Selects `local` or `cloud` execution |

**Security:** Never commit your actual `.env` file or share API credentials. The `.env.example` file contains placeholders only.

For step-by-step instructions, see the Part I and Part II laboratory guides in the `docs/` directory.
