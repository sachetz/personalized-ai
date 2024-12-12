import json
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

import streamlit as st
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from app.utils.navigation import make_sidebar

load_dotenv()
make_sidebar()

st.title("Personalized AI Assistant")

class State(TypedDict):
    messages: Annotated[list, add_messages]
graph_builder = StateGraph(State)

searchTool = TavilySearchResults(max_results=2)
tools = [searchTool]

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
llm = llm.bind_tools(tools)
memory = MemorySaver()

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

tool_node = ToolNode(tools=[searchTool])
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str):
    config = {"configurable": {"thread_id": st.session_state.user_id}}
    messages = []
    if "message_history" in st.session_state:
        for hist in st.session_state.message_history:
            if hist["role"] in ("user", "ai"):
                messages.append(("user" if hist["role"] == "user" else "ai", hist["content"]))
    messages.append(("user", user_input))
    events = graph.stream({"messages": messages}, config)

    tool_details = []
    final_response = ""

    for event in events:
        for key, value in event.items():
            if key == "chatbot":
                message = value["messages"][0]
                if message.content:
                    final_response = message.content
                elif 'tool_calls' in message.additional_kwargs and message.additional_kwargs['tool_calls']:
                    for tool_call in message.additional_kwargs['tool_calls']:
                        tool_name = tool_call['function']['name']
                        tool_args = json.loads(tool_call['function']['arguments'])
                        content = f"Calling {tool_name} with args {tool_args}"
                        tool_details.append(content)
                        st.write(content)
            elif key == "tools":
                tool_message = value["messages"][0]
                tool_response_content = tool_message.content
                try:
                    tool_response = json.loads(tool_response_content)
                except json.JSONDecodeError:
                    tool_response = tool_response_content  # Fallback if not JSON
                content = f"Tool Response: {tool_response}"
                tool_details.append(content)
                st.write(content)
    
    history = st.session_state.get("message_history", []) + \
        [{"role": "tool", "content": tool_details}]
    st.session_state.message_history = history
    return final_response


user_input = st.chat_input("User: ")
if user_input:
    for message in st.session_state.get("message_history", []):
        if message["role"] in ("user", "ai"):
            with st.chat_message(message["role"]):
                st.write(message["content"])
        else:
            with st.expander("Tool usage"):
                for msg in message["content"]:
                    st.write(msg)
    with st.chat_message("user"):
        history = st.session_state.get("message_history", []) + [{"role": "user", "content": user_input}]
        st.session_state.message_history = history
        st.write(user_input)
    with st.expander("Tool usage"):
        response = stream_graph_updates(user_input)
    history = st.session_state.get("message_history", []) + [{"role": "ai", "content": response}]
    st.session_state.message_history = history
    with st.chat_message("ai"):
        st.markdown(response)
