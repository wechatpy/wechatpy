from typing import Any, Optional

class ParsingInterrupted(Exception): ...

def parse(
    xml_input: Any,
    encoding: Optional[Any] = ...,
    expat: Any = ...,
    process_namespaces: bool = ...,
    namespace_separator: str = ...,
    disable_entities: bool = ...,
    process_comments: bool = ...,
    **kwargs: Any,
): ...
def unparse(
    input_dict: Any,
    output: Optional[Any] = ...,
    encoding: str = ...,
    full_document: bool = ...,
    short_empty_elements: bool = ...,
    **kwargs: Any,
): ...
