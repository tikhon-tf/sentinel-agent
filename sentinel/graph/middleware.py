"""Middleware for short-circuiting tool calls with missing required args.

Some model variants (notably Nemotron Ultra) periodically emit tool calls with
empty `{}` arguments for tools that declare required fields. The default
behavior — letting pydantic raise a ValidationError, which becomes an opaque
error ToolMessage — causes the model to retry the same empty-arg call several
times in a row, burning a full prompt round-trip per retry. This middleware
intercepts the call before validation, returns a structured correction signal,
and escalates after repeated consecutive failures so the loop can't run away.
"""
from __future__ import annotations

from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

EMPTY_ARG_GUARDED_TOOLS = {
    "create_jira_tickets": (
        "findings_json",
        'a JSON array string of finding objects, e.g. \'[{"sop_id":"SOP-ISEC-008",'
        '"clause_id":"HIPAA-164.312(a)","clause_title":"Access Control",'
        '"regulation":"HIPAA","severity":"high","gap_description":"Missing MFA"}]\'',
    ),
    "create_jira_ticket": (
        "sop_id",
        "the SOP identifier plus clause_id, clause_title, regulation, severity, and gap_description",
    ),
    "record_finding": (
        "sop_id",
        "the SOP identifier plus the finding fields (clause_id, regulation, severity, gap_description)",
    ),
}

_CORRECTION_MARKER = "[empty-args-guard]"
_ESCALATION_THRESHOLD = 2


def _required_fields(tool) -> list[str]:
    schema = getattr(tool, "args_schema", None)
    if schema is None:
        return []
    try:
        return list(schema.model_json_schema().get("required", []))
    except Exception:
        return []


def _missing_required(args: dict, required: list[str]) -> list[str]:
    if not isinstance(args, dict):
        return list(required)
    return [f for f in required if f not in args or args[f] in (None, "", [], {})]


def _consecutive_corrections(state, tool_name: str) -> int:
    messages = []
    if isinstance(state, dict):
        messages = state.get("messages", []) or []
    else:
        messages = getattr(state, "messages", []) or []
    count = 0
    for msg in reversed(messages):
        if not isinstance(msg, ToolMessage):
            continue
        content = msg.content if isinstance(msg.content, str) else ""
        if _CORRECTION_MARKER in content and getattr(msg, "name", None) == tool_name:
            count += 1
        else:
            break
    return count


@wrap_tool_call
def empty_args_guard(request, handler):
    """Short-circuit empty-args calls to tools with required fields."""
    tool_call = request.tool_call
    name = tool_call.get("name", "")
    if name not in EMPTY_ARG_GUARDED_TOOLS or request.tool is None:
        return handler(request)

    args = tool_call.get("args") or {}
    required = _required_fields(request.tool)
    if not required:
        return handler(request)
    missing = _missing_required(args, required)
    if not missing:
        return handler(request)

    field_hint, example = EMPTY_ARG_GUARDED_TOOLS[name]
    primary = missing[0] if missing else field_hint
    prior = _consecutive_corrections(request.state, name)
    if prior + 1 >= _ESCALATION_THRESHOLD:
        text = (
            f"{_CORRECTION_MARKER} Tool call '{name}' was again invoked with missing "
            f"required argument '{primary}'. Stop retrying this tool with empty args. "
            "Explain to the user what compliance findings you would have filed and ask "
            "them to confirm the inputs before retrying."
        )
    else:
        text = (
            f"{_CORRECTION_MARKER} Tool call '{name}' was missing required argument "
            f"'{primary}'. Re-emit the call with '{primary}' set to {example}. "
            "Do not retry with empty args."
        )
    return ToolMessage(content=text, tool_call_id=tool_call.get("id", ""), name=name)
