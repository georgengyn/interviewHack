let recorder;
let audioChunks = [];
let isRecording = false;

const recordButton = document.getElementById('recordButton');

recordButton.addEventListener('click', () => {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
});

function startRecording() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        
        navigator.mediaDevices.getUserMedia({audio:true},)

        .then(SetupStream)
        .catch(err => console.error(err));
        
    } 

}

function SetupStream(stream) {
    recorder = new MediaRecorder(stream);
    recorder.start();
    isRecording = true;
    recordButton.textContent = "Stop Recording";
    
    recorder.ondataavailable = e => {
        audioChunks.push(e.data);
    }
}
function stopRecording() {
            recorder.stop();
            recorder.onstop = e => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });

                const formData = new FormData();
                formData.append('audio', audioBlob, 'recording.mp3');

                // Send the recorded file to the backend
                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log('File uploaded successfully:', data);
                })
                .catch(error => {
                    console.error('Error uploading file:', error);
                });

                audioChunks = [];
                recordButton.textContent = "Start Recording";
                isRecording = false;
            };
        }