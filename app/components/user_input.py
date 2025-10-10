import streamlit as st
import yaml

def get_input(tool_call):
    print(tool_call)
    return yaml.dump(tool_call)