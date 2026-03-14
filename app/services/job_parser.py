import json
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


JOB_SCHEMA = {
    "name": "parsed_job",
    "schema": {
        "type": "object",
        "properties": {
            "client_name": {"type": ["string", "null"]},
            "phone": {"type": ["string", "null"]},
            "job_description": {"type": ["string", "null"]},
            "price": {"type": ["number", "null"]},
            "currency": {
                "type": ["string", "null"],
                "enum": ["RSD", "EUR", None],
            },
            "address": {"type": ["string", "null"]},
        },
        "required": [
            "client_name",
            "phone",
            "job_description",
            "price",
            "currency",
            "address",
        ],
        "additionalProperties": False,
    },
    "strict": True,
}


def parse_job_from_text(text: str) -> dict:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Extract job form fields from the user's dictated Serbian text. "
                    "Return only the structured data. "
                    "Always return Serbian Latin script (never Cyrillic)."
                    "If a field is unknown, return null. "
                    "Keep phone numbers exactly as spoken by the user. Do NOT add country codes or modify formatting."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": JOB_SCHEMA["name"],
                "schema": JOB_SCHEMA["schema"],
                "strict": True,
            }
        },
    )

    # Responses API returns text output in output_text for simple structured text responses
    return json.loads(response.output_text)