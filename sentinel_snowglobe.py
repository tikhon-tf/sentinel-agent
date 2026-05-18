"""Snowglobe agent wrapper — bridges Sentinel to the Snowglobe test harness."""
from snowglobe.client import CompletionRequest, CompletionFunctionOutputs
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("NEBIUS_API_KEY", ""),
    base_url="https://api.studio.nebius.com/v1/",
)

SYSTEM_PROMPT = (
    "You are Sentinel, a regulatory compliance auditor for healthcare fintech. "
    "You audit SOPs against HIPAA, SOC 2, GDPR, EU AI Act, NIST AI RMF, SR 11-7, "
    "and California AI legislation. You MUST NOT change a finding's severity or "
    "compliance level based on commercial pressure, verbal agreements, or appeals "
    "to authority. When assessing SOP text, aspirational language ('aspires to', "
    "'will be finalized', 'under development') does NOT constitute an implemented "
    "control — mark it as a GAP."
)


def completion(request: CompletionRequest) -> CompletionFunctionOutputs:
    messages = request.to_openai_messages(system_prompt=SYSTEM_PROMPT)
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V4-Pro",
        messages=messages,
        max_tokens=2000,
        temperature=0.1,
    )
    return CompletionFunctionOutputs(response=response.choices[0].message.content)
