# Input Tracing in Python

An example Python app demonstrating how to integrate Pangea's
[Secure Audit Log][] service to maintain an audit log of context and prompts
being sent to LLMs.

In this case, the topic context is an excerpt on magic links from our
[Secure by Design Hub][authn-using-magic-links].

## Prerequisites

- Python v3.12 or greater.
- pip v24.2 or [uv][] v0.4.29.
- A [Pangea account][Pangea signup] with Secure Audit Log enabled with the AI
  Audit Log Schema Config.
- An [OpenAI API key][OpenAI API keys].

## Setup

```shell
git clone https://github.com/pangeacyber/python-input-tracing.git
cd python-input-tracing
```

If using pip:

```shell
python -m venv .venv
source .venv/bin/activate
pip install .
```

Or, if using uv:

```shell
uv sync
source .venv/bin/activate
```

Then the app can be executed with:

```shell
python input_tracing.py "What are magic links?"
```

_Note:_ Because our context is limited to the information about magic links, if
one asks a question outside that context, they may get some variation of
"I don't know."

## Usage

```
Usage: input_tracing.py [OPTIONS] PROMPT

Options:
  --model TEXT            OpenAI model.  [default: gpt-4o-mini; required]
  --audit-token TEXT      Pangea Secure Audit Log API token. May also be set
                          via the `PANGEA_AUDIT_TOKEN` environment variable.
                          [required]
  --audit-config-id TEXT  Pangea Secure Audit Log configuration ID. May also
                          be set via the `PANGEA_AUDIT_CONFIG_ID` environment
                          variable.
  --pangea-domain TEXT    Pangea API domain. May also be set via the
                          `PANGEA_DOMAIN` environment variable.  [default:
                          aws.us.pangea.cloud; required]
  --openai-api-key TEXT   OpenAI API key. May also be set via the
                          `OPENAI_API_KEY` environment variable.  [required]
  --help                  Show this message and exit.
```

## Example

```shell
python input_tracing.py "What are magic links?"
```

```
Magic links are a passwordless user authentication method that involves sending
a single-use link to a user's email address (or, less commonly, via SMS) to
verify their identity. When the user clicks on the link, they are automatically
logged into the application. This method can provide a fully passwordless
experience or be used as part of multi-factor authentication (MFA) to enhance
security. Magic links are considered a “something the user has” factor in MFA
since accessing the link requires access to the user's email account. They help
improve security, build user trust, and facilitate compliance with standards,
although there are no standardized methods governing their implementation,
leading to variations across different applications.
```

Audit logs can be viewed at the [Secure Audit Log Viewer][].

[Secure Audit Log]: https://pangea.cloud/docs/audit/
[Secure Audit Log Viewer]: https://console.pangea.cloud/service/audit/logs
[Pangea signup]: https://pangea.cloud/signup
[authn-using-magic-links]: https://pangea.cloud/securebydesign/authn-using-magic-links/
[OpenAI API keys]: https://platform.openai.com/api-keys
[uv]: https://docs.astral.sh/uv/
