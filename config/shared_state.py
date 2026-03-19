from typing import Annotated,Optional
from typing_extensions import TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage
from typing import List

class Shared_State(TypedDict):

    messages:Annotated[List[AnyMessage], add_messages]
    user_input:Optional[str]
    story:Optional[str]
    img_url:Optional[str]
    error:Optional[str]
