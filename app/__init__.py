from flask import Flask, render_template, request, jsonify, redirect, url_for
from transcribeTxt import upload,transcribe, poll,getTranscriptionResultURL,saveTranscript
import os

app = Flask(__name__)
qIndex = 0

questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "What are your weaknesses?",
    "How do you deal with stress?"
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
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    qIndex += 1

    audio_url = upload("uploads/recording.mp3")
    saveTranscript(audio_url, "transcription")
    
    text = ""
    with open('transcription.txt', 'r') as file:
        text = file.read().replace('\n', '')
    
    print(text)
    #when qIndex reaches all question, finish interview
    return jsonify({'success': 'File uploaded successfully', 'next_question_url': url_for('home')}), 200

#process mp3 file and get text, do processing stuff

app.run()