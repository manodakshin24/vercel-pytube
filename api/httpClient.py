import json
import http.client

def makeHeaderWithoutContentType(authorization : str) -> dict:
    try:
        header = {}
        header["authorization"] = authorization
        return header
    except Exception as e:
        return {}

def httpRequestPost(api : str, route : str, header : dict, data : str) -> dict:
    try:
        connect = http.client.HTTPSConnection(api)
        connect.request('POST',route,data,header)
        response = connect.getresponse()
        jsonResponse = json.loads(response.read().decode())
        return jsonResponse
    except Exception as e:
        return {}
    
def httpRequestGet(api : str, route : str, header : dict) -> dict:
    try:
        connect = http.client.HTTPSConnection(api)
        connect.request('GET',route,headers = header)
        response = connect.getresponse()
        jsonResponse = json.loads(response.read().decode())
        return jsonResponse
    except Exception as e:
        return {}