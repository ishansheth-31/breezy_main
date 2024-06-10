from flask import Flask, request, jsonify
from flask_cors import CORS
import assemblyai as aai
import pyttsx3
from queue import Queue
from mainwithtts import MedicalChatbot
import os

app = Flask(__name__)
CORS(app)

transcript_queue = Queue()

chatbot = MedicalChatbot()

aai_api_key = os.getenv('AAI_KEY')
aai.settings.api_key = aai_api_key

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        transcript_queue.put(transcript.text + '')
        print("User:", transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

class AssemblyAIHandler:
  def __init__(self):
    self.transcriber = None

  def start_transcription(self):
    self.transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=44_100,
        end_utterance_silence_threshold=20000,
        disable_partial_transcripts=True
    )
    self.transcriber.connect()
    microphone_stream = aai.extras.MicrophoneStream()
    self.transcriber.stream(microphone_stream)

  def stop_transcription(self):
    if self.transcriber:
      self.transcriber.close()

handler = AssemblyAIHandler() 

@app.route('/start', methods=['POST'])
def start_conversation():
    initial_questions_dict = request.json

    if not initial_questions_dict:
        return jsonify({"error": "Invalid input data"}), 400

    last_initial_answer = chatbot.handle_initial_questions(initial_questions_dict)
    response = ""
    if last_initial_answer:
        response = chatbot.generate_response(last_initial_answer)
        speak(response)
    
    return jsonify({"initial_response": response})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        handler.start_transcription()
        transcript_result = transcript_queue.get()
        response = chatbot.generate_response(transcript_result)
        speak(response)
        chatbot.should_stop(response)
        return jsonify({"response": response, "finished": chatbot.finished}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/report', methods=['GET'])
def report():
    if chatbot.finished:
        try:
            report_content = chatbot.create_report().choices[0].message.content
            report_data = chatbot.extract_and_save_report(report_content)
            return jsonify(report_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Chat not finished"}), 400
    
@app.route('/terminate', methods=['POST'])
def terminate_session():
    try:
        data = request.get_json()
        if data and data.get('terminate_session', False):
            data['terminate_session'] = True 
            transcript_result = transcript_queue.get()
            response = chatbot.generate_response(transcript_result)
            speak(response)
            chatbot.should_stop(response)
            return jsonify({"response": response, "finished": chatbot.finished}), 200
        else:
            return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)