import streamlit as st

st.title("Solution")
# from ag_ui.core import TextMessageContentEvent, EventType
# from ag_ui.encoder 
from box import Box
tab_cfg=Box.from_yaml("""
Overview:
    Deal overview
    
Estimation: |
    Offerings Included
    * Scope Boundaries
    * Method
    * Estimation Guidance
    * Efforts         
Resource Plan: |
    Resource plan (downloadable)
    * Roles per staffing guidance
    * Bandmix
    * Centermix
    * Target
                                   
    | Role  | Skill | Loc|Band |M1 | M2| M n |
    |---|---|---|---|---|---|---|
    |   |   |   |   |   |   |   |
    |   |   |   |   |   |   |   |
    |   |   |   |   |   |   |   |     
                               
Price: |
    Pricing with terms
Log:
    Audit log
""")

tabs=st.tabs(tab_cfg.keys(),  width="stretch")

for i,tab in enumerate(tab_cfg.keys()):
    tabs[i].header(tab)
    tabs[i].markdown(tab_cfg[tab])
# st.write(st.session_state['config']['agents'])

# st.write(agent)


with st.sidebar:
    from components.sidebar import sidebar_main
    st.title('SideBar')
    sidebar_main()
    

    # with st.chat_message('assistant'):
    #      st.write_stream(parse_sse(resp))

    # response = agent.send(prompt)
    # st.write( response)
    # msg_log( response['messages'] )
    # # messages.chat_message("assistant").write( response['messages'][-1]['text'] )

    # with st.sidebar:
    #         st.write(response['metrics'])



def msg_log(msgs):
    for msg in msgs:
        role=msg['role']
        text=msg['content']
        if role and text:
            messages.chat_message(role).write(text)

