from __future__ import annotations

import yamale  # type: ignore
import yaml
from pydantic import BaseModel

_WAIT_FOR_AND_SEND_SPEC = """
include('wait-for-and-sends')
---
wait-for-and-sends:
    list(include('wait-for-and-send'))

wait-for-and-send:
    list(str(), min=2, max=2)

"""

_ONLY_SEND_SPEC = """
include('only-sends')
---
only-sends:
    list(include('only-send'))

only-send:
    str()
"""

WAIT_FOR_AND_SEND_SCHEMA = yamale.make_schema(content=_WAIT_FOR_AND_SEND_SPEC)
ONLY_SEND_SCHEMA = yamale.make_schema(content=_ONLY_SEND_SPEC)


class SendStr(BaseModel):
    send: str


class WaitForSendPair(BaseModel):
    wait_for: str
    send: str


# FUTURE: refactor and use single function
# FUTURE: Raise a better validation error, ideally return formatted block content
def scripted_cmd_interaction_parser(block_content: str) -> list[WaitForSendPair]:
    data = yaml.safe_load(block_content)
    yaml_validation = WAIT_FOR_AND_SEND_SCHEMA.validate(data, None, strict=True)
    if not yaml_validation.isValid():
        raise ValueError
    return [WaitForSendPair(wait_for=wait_for, send=send) for wait_for, send in data]


def timed_cmd_interaction_parser(block_content: str) -> list[SendStr]:
    data = yaml.safe_load(block_content)
    yaml_validation = ONLY_SEND_SCHEMA.validate(data, None, strict=True)
    if not yaml_validation.isValid():
        raise ValueError
    return [SendStr(send=send_str) for send_str in data]
