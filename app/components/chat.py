import streamlit as st
from pages import init_state, state
from api.agent import MyTeam
from components.user_input import get_input
from api.sse import sse_content, is_paused
from rich.pretty import pprint

def chat_clear():
        state.messages = []
        state.events = []

def chat_panel(team):
    # st.write(state)
    init_state("team",MyTeam(team['id']))
    if "messages" not in state:
        chat_clear()
    with st.container(horizontal=True):
        st.header('Chat panel')
        
        if st.button('Clear'):
            chat_clear()

    container= st.container(height=400,width="stretch")
    with container:
        for message in state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Say something"):
        
        # messages.chat_message("user").write(prompt)
        with container:    
            st.chat_message("user").markdown(prompt)
            state.messages.append({"role": "user", 
                                   "content": prompt})

            with st.chat_message("assistant"):
                # Simulate streaming content     
                prompt_process( prompt,)

def prompt_process( prompt,):
    
    message_placeholder = st.empty()
    full_response = ""

    with st.spinner():
        for chunk in state.team.send(prompt):
            state.events.append(chunk)
            txt,trace= sse_content(chunk)
            with st.sidebar:
                st.write(trace)
            full_response += txt
            if tools:=is_paused(chunk):
                for t in tools:
                    ask_input=get_input(t)
                    pprint(ask_input)
                    full_response+=str(ask_input)
                
                break
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
                        # Add assistant response to chat history
        state.messages.append({"role": "assistant", "content": full_response})



