import requests
import sys

 #upload
 #filename = "placeholder" : for later*
API_KEY_ASSEMBLYAI = "1ef7498e041047099cd9a17ca70b548e"
uploadEndpoint = "https://api.assemblyai.com/v2/upload"
transcriptEndpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization' : API_KEY_ASSEMBLYAI}

def upload(filename):
    def readFile(filename,chunkSize= 5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunkSize)
                if not data:
                    break
                yield data
    #HEADERS IS API KEY


    upload_response = requests.post(uploadEndpoint,
                            headers = headers,
                            data = readFile(filename))
    

    #didn't actually get upload_url
    audio_url = upload_response.json()['upload_url']
    return audio_url

 #transcribe
def transcribe(audio_url): 
    transcript_request = {"audio_url" : audio_url}
    transcript_response = requests.post(transcriptEndpoint, json = transcript_request, headers=headers)
    job_id = transcript_response.json()['id']
    return job_id


 #poll
def poll(transcript_id):
    pollingEndpoint = transcriptEndpoint + '/' + transcript_id
    pollingResponse = requests.get(pollingEndpoint, headers = headers)
    return pollingResponse.json()

def getTranscriptionResultURL(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        





 #save transcript 
def saveTranscript(audio_url, filename):
    data, error = getTranscriptionResultURL(audio_url)
    return data['text']

    if data: 
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data['text'])
    elif error:
        print("Error >:(", error)

