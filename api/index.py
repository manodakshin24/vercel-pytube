from http.server import BaseHTTPRequestHandler
from urllib import parse
import sys
import os
##from pytube import YouTube
from pytube.__main__ import YouTube
import json
##import httpClient
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



assemblyAiApiHeader = makeHeaderWithoutContentType(assemblyAiApiKey)

pollTime = 5

def uploadVideo(name : str) -> str:
    try:
        with open(name , "rb") as fileObj:
            uploadVideoResponse = httpRequestPost(assemblyAiApi, assemblyAiUploadRoute, assemblyAiApiHeader, fileObj)
            if uploadUrlKey in uploadVideoResponse:
                return uploadVideoResponse[uploadUrlKey] 
            else:
                return None
    except Exception as e:
                    print("Exception occurred while uploading video")
                    return None


##path = "/pytube/pytube/"
##sys.path.append("/vercel-pytube/pytube/pytube/__main__")
##here = os.path.abspath(os.path.dirname('__main__.py'))

##sys.path.append(os.path.abspath(__main__))

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")

CHUNK_SIZE = 5242880


def Downloader(link):
    yt =YouTube(link)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    #video = url.streams.first()
    try:
        #video.download()
        yt.download()
    except:
        print("An error has occurred")
    ##print("Download is completed successfully")

def Uploader(filename):
    def read_file(filename):
        with open(filename, 'rb') as _file:
              while True:
                data = _file.read(CHUNK_SIZE)
                if not data:
                      break
                yield data
##print("Upload completed successfully")

def makePayload(audioUrl : str) -> dict:
    try:
        payload = {}
        payload[audioUrlKey] = audioUrl
        return payload
    except Exception as e:
        return {}

def startToTranscriptVideo(payload : dict) -> str:
    try:
        transcriptVideoResponse = httpRequestPost(assemblyAiApi, assemblyAiTranscriptRoute, assemblyAiApiHeader, json.dumps(payload))
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
            transcribedResponse = httpRequestGet(assemblyAiApi, pollingEndpoint, assemblyAiApiHeader)
            if transcribedResponse[statusKey] == 'completed':
                if textKey in transcribedResponse:
                    return transcribedResponse[textKey]
            elif transcribedResponse[statusKey] == 'error':
                return None
            else:
                time.sleep(pollTime)
    except Exception as e:
        return None
'''
def main():
        Downloader("https://www.youtube.com/watch?v=oYZ--rdHL6I")
        uploadedURL = uploadVideo("Paneer Butter Masala  Paneer Makhani  Paneer Recipes  Gravy Curries  Home Cooking Show.mp4")
        if uploadedURL == None:
            print("Didn't receive uploaded url yet")
        else:
            print("Uploaded Url : {}".format(uploadedURL))
            payLoad = makePayload(uploadedURL)
            print("Payload: ", payLoad)
            id = startToTranscriptVideo(payLoad)
            if id == None:
                print("Didn't receive id")
            else:
                print("Transcription ID: ", id)
                transcribedText =  pollTranscriptionVideo(id)
                if transcribedText == None:
                    print("Error while polling")
                else:
                    print("Transcribed Text : {}".format(transcribedText))


if __name__ == "__main__":
    main()

'''
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        if "name" in dic:
            message = "Hello, " + dic["name"] + "!"
        else:
            message = "Hello, stranger!"
        #Downloader("https://www.youtube.com/watch?v=oYZ--rdHL6I","/tmp/")
        #Downloader("https://www.youtube.com/watch?v=XsUCNtU7mVM")
        #Downloader("https://youtu.be/XsUCNtU7mVM")
            uploadedUrl=uploadVideo("Paneer Butter Masala  Paneer Makhani  Paneer Recipes  Gravy Curries  Home Cooking Show.mp4")
            if uploadedUrl == None:
                print("Didn't receive uploaded url yet")
            else:
                message = "Uploaded Url : {}".format(uploadedUrl)
                
                self.wfile.write(message.encode())
                '''
                payload = makePayload(uploadedUrl)
                message = "Payload: {}".format(payload)
                #self.wfile.write(message.encode())
                id = startToTranscriptVideo(payload)
                if id == None:
                    message = "Didn't receive id"
                    #self.wfile.write(message.encode())
                else:
                    message = "Transcription ID: {}".format(id)
                    #self.wfile.write(message.encode())
                    
                    transcribedText = pollTranscriptionVideo(id)
                    if transcribedText == None:
                        message = "Error while polling"
                        #self.wfile.write(message.encode())
                    else:
                        message = ("Transcribed Text : {}".format(transcribedText))
                        print("Transcribed Text : {}".format(transcribedText))
                        self.wfile.write(message.encode())
            ##self.wfile.write(message.encode())
            '''
        ##message = "upload is complete!"
        #self.wfile.write(message.encode())
        ##self.wfile.write(message.encode())
        return