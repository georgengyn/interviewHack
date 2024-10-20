from flask import Flask, render_template, request, jsonify, redirect, url_for
from .transcribeTxt import upload,saveTranscript
from openai import OpenAI

import os

app = Flask(__name__)
qIndex = 0

OPENAI_API_KEY = "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"
client = OpenAI(api_key = OPENAI_API_KEY)

questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "What are your weaknesses?",
    "How do you deal with stress?",
    "Why should we hire you?",
    "What is your motivation?",
    "What are your goals?"
]

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/") #MAIN PAGE
def index(): 
    return redirect(url_for('home'))


@app.route("/home")
def home():
    return render_template('home.html', question=questions[qIndex])

@app.route('/upload', methods=['POST'])
def upload_file():
    global qIndex
    global questions
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    

    audio_url = upload("uploads/recording.mp3")
    text = saveTranscript(audio_url, "transcription")
    
    prompt = 'You are an assistant designed to critique answers to interview questions disregard unrealted inputs. You respond to users answers by providing constructive critiques for improvement. Give the user the question: ' + questions[qIndex]
    qIndex += 1
    
    if (qIndex >= questions.length):
        qIndex = 0;
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.8,
        max_tokens=200,
        frequency_penalty=.5,
        presence_penalty=.4
    )

    response_message = response.choices[0].message.content
    
    
    #you are an interviewer practicing with someone. Given the answer "text" to the question "tell me abtr urself", what feedback woudl you give
    
    
    

    #when qIndex reaches all question, finish interview
    return jsonify({'success': 'File uploaded successfully', 
                    'next_question_url': url_for('home'), 
                    'transcribedText': response_message, 
                    'question': questions[qIndex]
                    }), 200

#process mp3 file and get text, do processing stuff

app.run(debug=True)
