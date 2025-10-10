from pydash import pick
from rich.pretty import pprint
import json

def sse_content(sse):
    content=''
    event_txt=f"\n:red[{sse['event']}]" if not sse['event']=='RunContent' else ""
    if sse['event'] in 'RunContent TeamToolCallStarted RunPaused'.split():
        content= event_txt+sse.get('data',{}).get('content','')
    return content,fmt_evt_log(sse)

def fmt_evt_log(evt):
    data=evt['data']
    evt_type=data.get("event",'-')
    tool=pick(data['tool'],["tool_name","tool_args"]) if 'tool' in data else ''
    if evt_type=='RunPaused': return evt_type+json.dumps(tool)
    return ", ".join([evt_type]
                     )+json.dumps(tool)
def is_paused(evt):
    evt_type=evt['data'].get("event",'-')
    if evt_type=='RunPaused':
        return evt['data'].get("tools",'-')
    

# {"created_at": 1759869536, "event": "RunPaused", "agent_id": "estimation2-agent", "agent_name": "Estimation2 Agent", 
# "run_id": "c45cc2be-ccc2-4366-b6f0-cc439cb2d4a9", "session_id": "default", 
# "content": "I have tools to execute, but I need user input.", 
# "tools": [{"tool_call_id": "37e1aaf7-072b-46e5-bcf6-ea86d46fc31a", 
# "tool_name": "get_user_input", "tool_args": {"user_input_fields": 
# [{"field_name": "number_of_years", "field_type": "int", "field_description": "Please provide the number of years for the AMS estimation. (Default is 3 years)"}]}, 
# "tool_call_error": null, "result": null, "metrics": null, "child_run_id": null, "stop_after_tool_call": false, 
# "created_at": 1759869510, "requires_confirmation": null, "confirmed": null, "confirmation_note": null, "requires_user_input": true, 
# "user_input_schema": [{"name": "number_of_years", "field_type": "int", 
# "description": "Please provide the number of years for the AMS estimation. (Default is 3 years)", "value": null}], 
# "answered": null, "external_execution_required": null}]}