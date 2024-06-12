from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from flask_socketio import SocketIO
from medical_chatbot import MedicalChatbot
import os
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions
)

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

chatbot = MedicalChatbot()

API_KEY = os.getenv("DEEPGRAM_TOKEN")
config = DeepgramClientOptions(verbose=logging.WARN, options={"keepalive": "true"})
deepgram = DeepgramClient(API_KEY, config)
dg_connection = None
transcription_active = False

def initialize_deepgram_connection():
    print('testing1')
    global dg_connection
    # Initialize Deepgram client and connection
    dg_connection = deepgram.listen.live.v("1")

    def on_open(self, open, **kwargs):
        print(f"\n\n{open}\n\n")
    print('testing2')

    def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if len(transcript) > 0:
            print(result.channel.alternatives[0].transcript)
            socketio.emit('transcription_update', {'transcription': transcript})
    print('testing3')

    def on_close(self, close, **kwargs):
        print(f"\n\n{close}\n\n")

    def on_error(self, error, **kwargs):
        print(f"\n\n{error}\n\n")
    print('testing4')

    dg_connection.on(LiveTranscriptionEvents.Open, on_open)
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)
    print('testing5')

    # Define the options for the live transcription
    options = LiveOptions(model="nova-2", language="en-US")

    if dg_connection.start(options) is False: # THIS CAUSES ERROR
        print("Failed to start connection")
    else:
        print("Deepgram connection established.")
        exit()

def stop_transcription():
    global dg_connection, transcription_active
    if not transcription_active:
        print("Transcription not active")
        return
    if dg_connection:
        dg_connection.finish()
        dg_connection = None
    transcription_active = False

@app.route('/toggle_transcription', methods=['POST'])
def toggle_transcription():
    print("Received toggle request")
    data = request.get_json()
    print(f"Data received: {data}")
    if data and data.get("action") == "start":
        print("Starting transcription")
        initialize_deepgram_connection()
        print("transcription over")
        return jsonify({"status": "transcription started"}), 200
    elif data and data.get("action") == "stop":
        print("Stopping transcription")
        stop_transcription()
        transcribed_text = data.get("transcription", "")
        response = chatbot.generate_response(transcribed_text)
        chatbot.should_stop(response)
        return jsonify({"response": response, "finished": chatbot.finished}), 200
    else:
        print("Invalid action received")
        return jsonify({"error": "Invalid action"}), 400

@socketio.on('audio_stream')
def handle_audio_stream(data):
    if dg_connection:
        dg_connection.send(data)

if __name__ == '__main__':
    socketio.run(app, debug=True)

@app.route('/start/<patient_id>', methods=['POST'])
def start_conversation(patient_id):    
    initial_questions_dict = request.json
    
    if not initial_questions_dict:
        return jsonify({"error": "Invalid input data"}), 400

    last_initial_answer = chatbot.handle_initial_questions(initial_questions_dict, patient_id)
    response = ""
    if last_initial_answer:
        response = chatbot.generate_response(last_initial_answer)
    
    return jsonify({"initial_response": response})

@app.route('/report/<patient_id>', methods=['GET'])
def report(patient_id):
    if chatbot.finished:
        report_content = chatbot.create_report().choices[0].message.content
        report_data = chatbot.extract_and_save_report(report_content, patient_id)

        if isinstance(report_data, dict):
            report_data['_id'] = str(report_data.get('_id'))

        return jsonify(report_data)
    else:
        return jsonify({"error": "Chat not finished"}), 400

if __name__ == '__main__':
    app.run(debug=True)