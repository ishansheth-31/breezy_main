from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from medical_chatbot import MedicalChatbot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

chatbot = MedicalChatbot()

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


if __name__ == '__main__':
    app.run(debug=True)