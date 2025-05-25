# backend/app/models/chat.py
from typing import List, Optional, Any
from pydantic import BaseModel

class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageItem]

# Example, you might want to align this with AIMessage.model_dump() structure
class StreamedChatMessage(BaseModel):
    id: Optional[str] = None
    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Any]] = None # Or a more specific Pydantic model for tool calls
    # Add other fields if your AIMessage.model_dump_json() includes them