import requests
import time
from api import apiKey 

apiURL = 'https://api.gladia.io/v2/upload'
transcriptionURL = 'https://api.gladia.io/v2/transcription'

audioFilePath = './recording.wav'

headers = {
    'x-gladia-key': apiKey,
}

files = {
    'audio': ('recording.wav', open(audioFilePath, 'rb'), 'audio/wav')
}

uploadResponse = requests.post(apiURL, headers=headers, files=files)

if uploadResponse.status_code == 200:
    uploadResult = uploadResponse.json()
    audioUrl = uploadResult.get('audio_url')
    
    if audioUrl:
        print('AudioUrl: ', audioUrl)
        
        transcriptionHeaders = {
            'Content-Type': 'application/json',
            'x-gladia-key': apiKey,
        }
        
        transcriptionData = {
            'audio_url': audioUrl,
        }
        
        transcriptionResponse = requests.post(
            transcriptionURL,
            headers=transcriptionHeaders,
            json=transcriptionData
        )
        
        if transcriptionResponse.status_code == 201:
            transcriptionResult = transcriptionResponse.json()
            
            resultUrl = transcriptionResult['result_url']
            
            if resultUrl:
                print("resultUrl: ", resultUrl)
                
                while True:
                    resultResponse = requests.get(resultUrl, headers={'x-gladia-key': apiKey})
                    
                    if resultResponse.status_code == 200:
                        finalResult = resultResponse.json()
                        
                        if finalResult.get('status') == 'done':
                            transcription = finalResult['result']['transcription']['full_transcript']
                            print("\nTranscription: ", transcription)
                            break
                            
                        else:
                            print("Result being processed")
                            time.sleep(5)
                        
                    else:
                        print("Error fetching transcription: ", resultResponse.status_code, resultResponse.text)
                        break
        
        else:
             print("Transcription Error:", transcriptionResponse.status_code, transcriptionResponse.text)
        
    else:
        print("url not found")
    
else: 
    print("error: ", uploadResponse.status_code, uploadResponse.text)
