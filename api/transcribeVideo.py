import json
import httpClient
import time

assemblyAiApi = "api.assemblyai.com"

assemblyAiUploadRoute = "/v2/upload"

assemblyAiTranscriptRoute = "/v2/transcript"

assemblyAiApiKey = "3c759f10117c48d7ac03bd84f149fdac"

uploadUrlKey = "upload_url"

audioUrlKey = "audio_url"

idKey = "id"

textKey = "text"

statusKey = "status"

assemblyAiApiHeader = httpClient.makeHeaderWithoutContentType(assemblyAiApiKey)

pollTime = 5

def makePayload(audioUrl : str) -> dict:
    try:
        payload = {}
        payload[audioUrlKey] = audioUrl
        return payload
    except Exception as e:
        return {}

def uploadVideo(name : str) -> str:
    try:
        with open(name , "rb") as fileObj:
            uploadVideoResponse = httpClient.httpRequestPost(assemblyAiApi, assemblyAiUploadRoute, assemblyAiApiHeader, fileObj)
            if uploadUrlKey in uploadVideoResponse:
                return uploadVideoResponse[uploadUrlKey] 
            else:
                return None
    except Exception as e:
        return None
    
def startToTranscriptVideo(payload : dict) -> str:
    try:
        transcriptVideoResponse = httpClient.httpRequestPost(assemblyAiApi, assemblyAiTranscriptRoute, assemblyAiApiHeader, json.dumps(payload))
        if idKey in transcriptVideoResponse:
            return transcriptVideoResponse[idKey] 
        else:
            return None
    except Exception as e:
        return None

def pollTranscriptionVideo(transcriptId : str) -> str:
    try:
        pollingEndpoint = assemblyAiTranscriptRoute + "/{}".format(transcriptId)
        while True:
            transcribedResponse = httpClient.httpRequestGet(assemblyAiApi, pollingEndpoint, assemblyAiApiHeader)
            if transcribedResponse[statusKey] == 'completed':
                if textKey in transcribedResponse:
                    return transcribedResponse[textKey]
            elif transcribedResponse[statusKey] == 'error':
                return None
            else:
                time.sleep(pollTime)
    except Exception as e:
        return None