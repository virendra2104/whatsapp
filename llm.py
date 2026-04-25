import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from tools import get_current_datetime, get_current_weather, get_weather

load_dotenv()

# LLM
llm = ChatMistralAI(
    model="mistral-medium",
    temperature=0.7,
    streaming=True
)

# Bind tools
tools = [get_current_datetime, get_current_weather, get_weather]
llm = llm.bind_tools(tools)

# Tool map
tool_map = {tool.name: tool for tool in tools}


def ask_question(question):
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content=question)
    ]

    final_answer = ""   # <-- ADD THIS

    while True:
        tool_calls = None
        full_response = None

        for chunk in llm.stream(messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                final_answer += chunk.content   # <-- COLLECT TEXT

            if chunk.tool_calls:
                tool_calls = chunk.tool_calls
                full_response = chunk

        print()

        if not tool_calls:
            break

        messages.append(full_response)

        for tool_call in tool_calls:
            tool = tool_map[tool_call["name"]]
            result = tool.invoke(tool_call["args"])

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return final_answer   # <-- VERY IMPORTANT