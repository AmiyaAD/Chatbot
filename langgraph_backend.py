from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

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

checkpointer = InMemorySaver()

chatBot = graph.compile(checkpointer=checkpointer)

config = {'configurable': {'thread_id':'thread-1'}}

# for message_chunk, metadata in chatBot.stream(
#     {'messages': [HumanMessage(content='WHat is the recipe to make pasta?')]},
#     config=config,
#     stream_mode='messages'
#     ):

#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)


