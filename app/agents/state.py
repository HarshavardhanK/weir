from typing import TypedDict, List, Annotated, Any


class State(TypedDict):
    input: Any
    output: Any
    messages: List[Any]
    # Additional fields as required
