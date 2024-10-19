from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
@app.route("/home")
def welcome(): 
    return render_template('home.html')

if __name__ == '__main__':
    app.run()