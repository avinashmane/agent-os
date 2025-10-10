import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os

st.title("AGNO Chat UI")

st.write("Welcome to the AGNO Chat Interface!")


st.markdown("""
## URLs
- Chat URL
http://localhost:8501/
- AgentOS URL
http://localhost:7777/docs            
- IBM on AI
https://www.ibm.com/thought-leadership/institute-business-value/en-us/report/ceo-generative-ai            
## Agents            
""")

from api.agent import api


config= api.config()
for x in config['agents']:
    # st.write(x)
    st.write(f"- **{x.get('name','🤖')}** __{x['id']}__:\n\n"+
             x.get('description',"No description."))
    
st.markdown("## Status" )    
st.write(api.health().get('status','--'))