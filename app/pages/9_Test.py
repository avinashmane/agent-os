import streamlit as st

st.title("Test Chatbot")

# Initialize chat history
def clear_msgs(): st.session_state.messages_tst = []
if "messages_tst" not in st.session_state:
    clear_msgs()

st.button('Clear history', on_click=clear_msgs)

# Display chat messages from history on app rerun
for message in st.session_state.messages_tst:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

from time import sleep

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages_tst.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate streaming content
        for chunk in ["Hello", ", ", "you ", "asked: ", *prompt.split()]:
            full_response += chunk
            sleep(1)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages_tst.append({"role": "assistant", "content": full_response})
