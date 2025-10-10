import streamlit as st

def sidebar_tab2():    
    
    events= st.session_state.events

    for evt in events:
        evt_type=evt.get('event')
        if evt_type not in ['RunContent']:
            try: 
                dt=evt.get('data',{}).get('create_at')
                dt=date(dt) if dt else '--'
            except: 
                dt='--'
                print(">>>",evt)
            
            st.write(dt,
                    evt_type,
                    )
            
