from flask import Flask, request, jsonify
from flask_cors import CORS
from medical_chatbot import MedicalChatbot

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
bot = MedicalChatbot()

@app.route('/start', methods=['POST'])
def start_chat():
    # Example response to start the chat
    return jsonify({'response': 'Hello, I am your virtual nurse assistant. How can I help you today?'})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    response = bot.generate_response(message)
    bot.should_stop(response)
    return jsonify({'response': response})

@app.route('/report', methods=['GET'])
def generate_report():
    if bot.finished:
        report_content = bot.create_report().choices[0].message.content  # Assuming create_report returns a response object
        file_path = bot.extract_and_save_report(report_content)
        return jsonify({'report_path': file_path})
    return jsonify({'error': 'Conversation not finished yet'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
