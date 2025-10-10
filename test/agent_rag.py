from agents.know_agent import rag_agent
rag_agent.print_response("get recipe with chicken and ganagal?", 
    stream_intermediate_steps=True,
    stream=True, markdown=True)