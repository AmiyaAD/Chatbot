from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

llm = ChatOpenAI(
  model="nvidia/nemotron-3-super-120b-a12b",
  api_key="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", 
  base_url="https://integrate.api.nvidia.com/v1"
)

class ChatState(TypedDict):

    messages : Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):

    messages = state["messages"]

    response = llm.invoke(messages)

    return {'messages': [response]}    

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

chatBot = graph.compile(checkpointer=checkpointer)

config = {'configurable': {'thread_id':'thread-2'}}

# for message_chunk, metadata in chatBot.stream(
#     {'messages': [HumanMessage(content='WHat is the recipe to make pasta?')]},
#     config=config,
#     stream_mode='messages'
#     ):

#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)


# response = chatBot.invoke(
#     {'messages': [HumanMessage(content='What is the national frute of west bengal ')]},
#     config=config)

# print(response)

def retrive_all_threads():
    all_thread = set()

    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config['configurable']['thread_id'])

    return list(all_thread)