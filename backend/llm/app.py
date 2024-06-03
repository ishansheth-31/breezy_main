from flask import Flask, request, jsonify
from flask_cors import CORS
from medical_chatbot import MedicalChatbot

app = Flask(__name__)
CORS(app)

chatbot = MedicalChatbot()

@app.route('/start', methods=['POST'])
def start_conversation():    
    initial_questions_dict = request.json
    
    if not initial_questions_dict:
        return jsonify({"error": "Invalid input data"}), 400

    last_initial_answer = chatbot.handle_initial_questions(initial_questions_dict)
    response = ""
    if last_initial_answer:
        response = chatbot.generate_response(last_initial_answer)
    
    return jsonify({"initial_response": response})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    response = chatbot.generate_response(user_message)
    chatbot.should_stop(response)
    return jsonify({"response": response, "finished": chatbot.finished})

@app.route('/report', methods=['GET'])
def report():
    if chatbot.finished:
        report_content = chatbot.create_report().choices[0].message.content
        report_data = chatbot.extract_and_save_report(report_content)
        return jsonify(report_data)
    else:
        return jsonify({"error": "Chat not finished"}), 400

if __name__ == "__main__":
    app.run(debug=True)