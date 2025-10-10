import streamlit as st
from api.agent import AgentAPI
state=st.session_state

def init_state(x,default):
    # print (f"init_state({x},{default})")
    if not x in state:
        state[x]=default
    return state[x]


init_state('config',AgentAPI().config())
