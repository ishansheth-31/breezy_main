import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    DeepgramClientOptions
)
from medical_chatbot import MedicalChatbot

load_dotenv()

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://breezy-frontend-1ffc4ccedf6b.herokuapp.com"]}})
#socketio = SocketIO(app, cors_allowed_origins=['https://breezy-frontend-1ffc4ccedf6b.herokuapp.com'])
CORS(app)
socketio = SocketIO(app)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Set up Deepgram client configuration
config = DeepgramClientOptions(
    verbose=logging.WARN,  # Change to logging.INFO or logging.DEBUG for more verbose output
    options={"keepalive": "true"}
)

deepgram = DeepgramClient(DEEPGRAM_API_KEY, config)

chatbot = MedicalChatbot()
dg_connection = None

def initialize_deepgram_connection():
    global dg_connection
    # Initialize Deepgram client and connection
    dg_connection = deepgram.listen.live.v("1")

    def on_open(self, open, **kwargs):
        print(f"\n\n{open}\n\n")

    def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if len(transcript) > 0:
            print(result.channel.alternatives[0].transcript)
            socketio.emit('transcription_update', {'transcription': transcript})

    def on_close(self, close, **kwargs):
        print(f"\n\n{close}\n\n")

    def on_error(self, error, **kwargs):
        print(f"\n\n{error}\n\n")

    dg_connection.on(LiveTranscriptionEvents.Open, on_open)
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    # Define the options for the live transcription
    options = LiveOptions(model="nova-2", language="en-US")

    if dg_connection.start(options) is False: # THIS CAUSES ERROR
        print("Failed to start connection")
        exit()

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

@app.route('/chat/<patient_id>', methods=['POST'])
def chat(patient_id):
    data = request.json
    user_message = data.get("message", "")
    response = chatbot.generate_response(user_message)
    chatbot.should_stop(response)
    return jsonify({"response": response, "finished": chatbot.finished})

@socketio.on('audio_stream')
def handle_audio_stream(data):
    if dg_connection:
        dg_connection.send(data)

@socketio.on('toggle_transcription')
def handle_toggle_transcription(data):
    print("toggle_transcription", data)
    action = data.get("action")
    if action == "start":
        print("Starting Deepgram connection")
        initialize_deepgram_connection()

@socketio.on('connect')
def server_connect():
    print('Client connected')

@socketio.on('restart_deepgram')
def restart_deepgram():
    print('Restarting Deepgram connection')
    initialize_deepgram_connection()

if __name__ == '__main__':
    logging.info("Starting Flask and SocketIO server.")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5001)
