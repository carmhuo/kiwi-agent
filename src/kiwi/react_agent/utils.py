"""Utility & helper functions."""
import os

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    # provider, model = fully_specified_name.split("/", maxsplit=1)
    # llm = ChatOpenAI(
    #     model=os.getenv("MODELSCOPE_MODEL"),
    #     base_url=os.getenv("MODELSCOPE_API_BASE"),
    #     api_key=os.getenv("MODELSCOPE_API_KEY"),  # ModelScope Token
    #     temperature=0
    # )
    model = "Qwen/Qwen2.5-32B-Instruct"
    if fully_specified_name:
        model = fully_specified_name
    provide = "openai"
    base_url = os.getenv("MODELSCOPE_API_BASE")
    llm = init_chat_model(model=model, model_provider=provide, 
                        base_url=base_url, temperature=0.7)
    return llm
