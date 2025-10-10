import streamlit as st
from api.agent import MyAgent, api
from pydash import find 
from datetime import date

from api.sse import sse_content

def side_bar_log():
    pass

def sidebar_main():
    agents=api.config()['agents']
    select_agent = st.selectbox("Select Agent", options=[x.get('name',x['id']) for x in agents])
    agent_id=find(agents, lambda x: x.get('name',x['id']) == select_agent)['id']
    if agent_id:
        st.write(f"You have selected: ",agent_id)

    agent=MyAgent(agent_id)
    def clear():
        st.session_state.messages = []
        st.session_state.events = []
    if "messages" not in st.session_state:
        clear()

    def parse_sse(sse):
        st.session_state.events.append(sse)
        if sse['event']=='RunContent':
            return sse.get('data',{}).get('content')
        return ''
        
    if st.button('Clear'):
        clear()

    container= st.container(height=300)
    with container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Say something"):
        
        # messages.chat_message("user").write(prompt)
        with container:    
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # resp=agent.send(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                # Simulate streaming content
                for chunk in agent.send(prompt):
                    txt=parse_sse(chunk)
                    # st.write(chunk)
                    full_response += txt
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})


