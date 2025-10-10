import requests
import os
from functools import lru_cache
import json
from rich.pretty import pprint

class AgentAPI:
    def __init__(self,api_url="http://localhost:7777"):
        self.api_url = api_url  

    def health(self):
        return self._get("/health")
    
    @lru_cache
    def config(self):
        return self._get("/config")

    def _get(self, endpoint):
        try:
            response = requests.get(self.api_url + endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                return f"GET {endpoint} failed with status code {response.status_code}"
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to API: {e}")
        
    def _post(self, endpoint, data, **kw):
        try:
            response = requests.post(self.api_url + endpoint, data=data, **kw)
            # pprint( response.__dict__)
            if response.status_code == 200:
                return response
            else:
                # print(response.json())
                return f"POST {endpoint} failed with status code {response.status_code}"
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to API: {e}")

api=AgentAPI(os.environ.get("AGENT_API_URL", "http://localhost:7777"))



class MyAgent:
    def __init__(self, agent_id ):
        self.api= api
        self.id = agent_id

    def send(self, message):
        data={
            "stream": True,
            "session_id": "default",
            "user_id": "user_1",
            "message": message
        }
        response=None
        try:
            response = api._post(f"/agents/{self.id}/runs", data, stream=True)
                    # response = requests.get("http://localhost:8000/stream", stream=True)
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    yield(self.sse_parse(chunk.decode('utf-8')))
        except requests.exceptions.ConnectionError:
            print("Could not connect to FastAPI SSE endpoint. Ensure it's running.",response)
        self.response=response
        print(f"/agents/{self.id}/runs", data, response.__dict__)
        # return self.response
    
    def sse_parse(self, msg):
        try:
            lines=[x for x in msg.strip().split('\n')]
            ret = {}
            event=lines[0].split(": ",1)
            data="\n".join(lines[1:]).split(": ",1)
            return {event[0]: event[1],
                    data[0]:json.loads(data[1])}
        except Exception as e:
            print(f"error parsing event {e!r}",msg)
            return {'event':event[1], 'data':data[1]}
    # def __repr__(self):
    #     return f"Agent(name={self.id}, description=self.description)"

class MyTeam:
    def __init__(self, agent_id ):
        self.api= api
        self.id = agent_id

    def send(self, message):
        data={
            "stream": True,
            "session_id": "default",
            "user_id": "user_1",
            "message": message
        }
        response=None
        try:
            response = api._post(f"/teams/{self.id}/runs", data, stream=True)
                    # response = requests.get("http://localhost:8000/stream", stream=True)
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    yield(self.sse_parse(chunk.decode('utf-8')))
        except requests.exceptions.ConnectionError:
            print("Could not connect to FastAPI SSE endpoint. Ensure it's running.",response)
        self.response=response
        print(f"/teams/{self.id}/runs", data, response.__dict__)
        # return self.response
    
    def sse_parse(self, msg):
        try:
            lines=[x for x in msg.strip().split('\n')]
            ret = {}
            event=lines[0].split(": ",1)
            data="\n".join(lines[1:]).split(": ",1)
            return {event[0]: event[1],
                    data[0]:json.loads(data[1])}
        except Exception as e:
            print(f"error parsing event {e!r}",msg)
            return {'event':event[1], 'data':data[1]}
    # def __repr__(self):
    #     return f"Agent(name={self.id}, description=self.description)"

