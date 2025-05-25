# backend/app/routers/agent.py
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage

from kiwi.react_agent import graph # Import the compiled graph
from kiwi.fastapi.models import ChatRequest, StreamedChatMessage # Import Pydantic models

router = APIRouter(
    prefix="/api", # Sets a prefix for all routes in this router
    tags=["Agent"] # For OpenAPI documentation
)

async def event_stream_generator(initial_graph_input: dict):
    # stream_mode="values" makes event_chunk the direct output of a node
    # stream_mode="updates" (default) gives dict like {"node_name": output}
    # Let's use "updates" as it's more common to check node names
    async for event_chunk_update in graph.astream(initial_graph_input): # Default stream_mode="updates"
        # event_chunk_update will be like {"node_name": output_value}
        for node_name, output_value in event_chunk_update.items():
            if node_name == "call_model" and isinstance(output_value, dict) and "messages" in output_value:
                last_message = output_value["messages"][-1]
                if isinstance(last_message, AIMessage): # Check if it's an AIMessage
                    # Use Pydantic model for consistent serialization if desired
                    # streamed_msg = StreamedChatMessage(**last_message.dict())
                    # yield f"data: {streamed_msg.model_dump_json()}\n\n"
                    # Or simpler, direct dump if AIMessage has model_dump_json
                     if hasattr(last_message, 'model_dump_json'):
                        yield f"data: {last_message.model_dump_json()}\n\n"
                     else: # Fallback if model_dump_json isn't present or for simpler dicts
                        simple_dict = {"role": getattr(last_message, "role", "assistant"), "content": getattr(last_message, "content", "")}
                        yield f"data: {json.dumps(simple_dict)}\n\n"

            # You can add handling for other nodes like "tools" if needed
            # elif node_name == "tools":
            #     # output_value here would be the list of ToolMessage objects
            #     # You could stream these too if the frontend needs to know about tool calls/results
            #     if isinstance(output_value, list):
            #         for tool_message in output_value:
            #             if isinstance(tool_message, ToolMessage):
            #                 tool_data = {"role": "tool", "tool_call_id": tool_message.tool_call_id, "content": tool_message.content}
            #                 yield f"data: {json.dumps(tool_data)}\n\n"
            # Pass, ignore other updates, or handle them as needed
            pass


@router.post("/astream")
async def astream_agent_endpoint(payload: ChatRequest):
    """
    Endpoint to stream the agent's responses using Server-Sent Events.
    Expects JSON: {"messages": [{"role": "user", "content": "Your query"}]}
    """
    try:
        # Convert Pydantic model messages to LangChain HumanMessage objects
        # Note: graph input schema (InputState) is Dict[str, Any], expecting a 'messages' key
        # with a list of BaseMessage-compatible objects.
        input_messages: List[BaseMessage] = []
        for msg_item in payload.messages:
            if msg_item.role.lower() == "user":
                input_messages.append(HumanMessage(content=msg_item.content))
            # Add elif for "ai", "system", "tool" if your graph expects them in initial input
            else:
                # Fallback or raise error for unsupported roles in initial input
                print(f"Unsupported role in initial message: {msg_item.role}")


        if not input_messages:
            raise HTTPException(status_code=400, detail="No valid user messages provided")

        initial_graph_input = {"messages": input_messages}
        
        return StreamingResponse(event_stream_generator(initial_graph_input), media_type="text/event-stream")

    except HTTPException as http_exc: # Re-raise HTTPException
        raise http_exc
    except Exception as e:
        import traceback
        print(f"Error in /api/astream: {e}\n{traceback.format_exc()}")
        # Return a structured error, or re-raise as HTTPException
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# You can add an invoke_agent endpoint similarly if needed:
@router.post("/invoke")
async def invoke_agent_endpoint(payload: ChatRequest):
    try:
        input_messages: List[BaseMessage] = []
        for msg_item in payload.messages:
            if msg_item.role.lower() == "user":
                input_messages.append(HumanMessage(content=msg_item.content))
        
        if not input_messages:
            raise HTTPException(status_code=400, detail="No valid user messages provided")

        initial_graph_input = {"messages": input_messages}
        final_state = await graph.ainvoke(initial_graph_input)

        response_messages = []
        if final_state and "messages" in final_state:
            for msg in final_state["messages"]:
                # Convert LangChain messages to Pydantic model or simple dict for response
                if isinstance(msg, BaseMessage): # AIMessage, HumanMessage, etc.
                    response_messages.append(StreamedChatMessage(
                        id=getattr(msg, 'id', None),
                        role=getattr(msg, 'type', 'assistant'), # .type is common for LC messages
                        content=getattr(msg, 'content', ''),
                        name=getattr(msg, 'name', None),
                        tool_calls=getattr(msg, 'tool_calls', None)
                    ).model_dump(exclude_none=True))
        return {"response": response_messages}
    except Exception as e:
        import traceback
        print(f"Error in /api/invoke: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")