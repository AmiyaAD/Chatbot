import streamlit as st
from langgraph_database_backen import chatBot, retrive_all_threads
from langchain_core.messages import HumanMessage
import uuid

# *********************************** Utility Functions*********************

def generate_thread_id():

    thread_id = uuid.uuid4()

    return thread_id

def reset_chat():

    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['messages_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)   

def load_conversation(thread_id):

    return chatBot.get_state({'configurable': {'thread_id': thread_id}}).values['messages']         

# *********************************** Session State ************************

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all_threads()       


add_thread(st.session_state['thread_id'])

# ************************************* Thread id ***************************        

config = {'configurable': {'thread_id': st.session_state['thread_id']}}

# *********************************** Side Bar *****************************

st.sidebar.title("Langgraph Chatbot")

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = 'user'
            else:    
                role = 'assistant'
            temp_messages.append({'role': role, 'content': message.content})    

        st.session_state['messages_history'] = temp_messages

        

# ********************************** Main UI ********************************

for message in st.session_state['messages_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
user_message = st.chat_input('Type here')

if user_message:

    st.session_state['messages_history'].append({'role':'user', 'content': user_message})
    with st.chat_message('user'):
        st.text(user_message)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadeta in chatBot.stream(
                {'messages': [HumanMessage(content=user_message)]},
                config=config,
                stream_mode='messages'

            )
        )    

    st.session_state['messages_history'].append({'role': 'assistant', 'content': ai_message})    