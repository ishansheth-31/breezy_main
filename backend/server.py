from flask import Flask, request, jsonify
from backend.llm.app import MedicalChatbot

app = Flask(__name__)
chatbot = MedicalChatbot()

@app.route('/start_chat', methods=['POST'])
def start_chat():
    data = request.json
    last_initial_answer = chatbot.handle_initial_questions(data['questions'])
    if last_initial_answer:
        response = chatbot.generate_response(last_initial_answer)
        return jsonify({'response': response})
    return jsonify({'error': 'No initial answer received'})

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message']
    response = chatbot.generate_response(user_input)
    chatbot.should_stop(response)
    return jsonify({'response': response})

@app.route('/create_report', methods=['GET'])
def create_report():
    report_content = chatbot.create_report()
    file_path = chatbot.extract_and_save_report(report_content)
    return jsonify({'file_path': file_path})

if __name__ == '__main__':
    app.run(debug=True)
