from __future__ import annotations

import sys

import click
from dotenv import load_dotenv
from openai import OpenAI
from pangea import PangeaConfig
from pangea.services import Audit
from pangea.services.audit.util import canonicalize_json

load_dotenv(override=True)


SYSTEM_PROMPT = """
You are a kind and humble chatbot who sticks to facts received from the
following context:
Context: {context}
"""

# Sample context from <https://pangea.cloud/securebydesign/authn-using-magic-links/>.
CONTEXT = """
Magic link authentication is a passwordless user authentication method that
sends a single-use link to the user's email address (or, less commonly, via SMS)
to verify their identity. When the user clicks on the link, they are
automatically (“magically”) logged in to the application (or there may be
additional login steps that follow).

It can be used by itself for a potentially fully passwordless experience, for
cases in which it provides an adequate level of security. More commonly though,
it is used for multi-factor authentication (MFA), for example on top of
password-based authentication, providing an additional layer of security. In
terms of MFA, magic links are considered a “something the user has” factor since
it proves the user has access to their email account - the presumption being
that they are the only ones with access.

As a form of authentication, magic link authentication provides gatekeeping,
enhanced data security, and reduced abuse to your app. Having robust
authentication bolsters the security of your application, builds trust with
users by demonstrating a commitment to protecting their data, helps to safeguard
your reputation, and can facilitate adherence to compliance standards. Magic
links can provide strong authentication and do so in a way that is convenient
for users. No standards govern magic link authentication. Each application can
implement it in its own unique way, resulting in various variations and
approaches and a lack of interoperability.
"""


@click.command()
@click.option("--model", default="gpt-4o-mini", show_default=True, required=True, help="OpenAI model.")
@click.option(
    "--audit-token",
    envvar="PANGEA_AUDIT_TOKEN",
    required=True,
    help="Pangea Secure Audit Log API token. May also be set via the `PANGEA_AUDIT_TOKEN` environment variable.",
)
@click.option(
    "--audit-config-id",
    envvar="PANGEA_AUDIT_CONFIG_ID",
    required=False,
    help="Pangea Secure Audit Log configuration ID. May also be set via the `PANGEA_AUDIT_CONFIG_ID` environment variable.",
)
@click.option(
    "--pangea-domain",
    envvar="PANGEA_DOMAIN",
    default="aws.us.pangea.cloud",
    show_default=True,
    required=True,
    help="Pangea API domain. May also be set via the `PANGEA_DOMAIN` environment variable.",
)
@click.option(
    "--openai-api-key",
    envvar="OPENAI_API_KEY",
    required=True,
    help="OpenAI API key. May also be set via the `OPENAI_API_KEY` environment variable.",
)
@click.argument("prompt")
def main(
    *,
    prompt: str,
    model: str,
    audit_token: str,
    audit_config_id: str | None = None,
    pangea_domain: str,
    openai_api_key: str,
) -> None:
    config = PangeaConfig(domain=pangea_domain)
    audit = Audit(token=audit_token, config=config, config_id=audit_config_id)

    # Log context and prompt.
    audit.log_bulk(
        [
            {
                "event_type": "inference:user_prompt",
                "event_tools": OpenAI.__name__,
                "event_input": canonicalize_json({"context": CONTEXT, "prompt": prompt}).decode("utf-8"),
            }
        ]
    )

    # Generate chat completions.
    stream = OpenAI(api_key=openai_api_key).chat.completions.create(
        messages=(
            {"role": "system", "content": SYSTEM_PROMPT.format(context=CONTEXT)},
            {"role": "user", "content": prompt},
        ),
        model=model,
        stream=True,
    )
    for chunk in stream:
        for choice in chunk.choices:
            sys.stdout.write(choice.delta.content or "")
            sys.stdout.flush()

        sys.stdout.flush()

    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
