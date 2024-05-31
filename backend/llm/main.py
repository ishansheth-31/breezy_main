from medical_chatbot import MedicalChatbot

def main():
    print("Hello, I'm your virtual nurse assistant. Let's start with some basic questions.")
    bot = MedicalChatbot()
    
    # Prompt user for initial questions and gather answers
    initial_questions_dict = {
        "What is your first and last name?": input("What is your first and last name? "),
        "What is your approximate height?": input("What is your approximate height? "),
        "What is your approximate weight?": input("What is your approximate weight? "),
        "Are you currently taking any medications?": input("Are you currently taking any medications? "),
        "Have you had any recent surgeries?": input("Have you had any recent surgeries? "),
        "Do you have any known drug allergies?": input("Do you have any known drug allergies? "),
        "Finally, could you tell me what your going into the office for?": input("Finally, could you tell me what your going into the office for? ")
    }

    last_initial_answer = bot.handle_initial_questions(initial_questions_dict)

    if last_initial_answer:
        response = bot.generate_response(last_initial_answer)
        print("Virtual Nurse:", response)

    while not bot.finished:
        user_input = input("You: ")
        response = bot.generate_response(user_input)
        print("Virtual Nurse:", response)
        bot.should_stop(response)

    if bot.finished:
        report_content = bot.create_report().choices[0].message.content
        print(report_content)
        file_path = bot.extract_and_save_report(report_content)
        print(f"Report saved to: {file_path}")

if __name__ == "__main__":
    main()