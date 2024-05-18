from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import logging

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# Initialize the OpenAI client

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Function to read the knowledge.txt file
def read_knowledge_file():
    try:
        with open('knowledge.txt', 'r') as file:
            knowledge = file.read()
        return knowledge
    except Exception as e:
        logging.error(f"Error reading knowledge file: {e}")
        return "Default system message: No knowledge available."

# Generate the initial system message based on knowledge.txt
def generate_initial_system_message():
    knowledge_content = read_knowledge_file()
    return {
        "role": "system",
        "content": knowledge_content
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Build the message history
    messages = [generate_initial_system_message()]

    # User's message
    messages.append({"role": "user", "content": user_message})

    # Log the messages for debugging
    logging.debug(f"Messages: {messages}")

    try:
        # Call OpenAI API
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150)

        response_message = response.choices[0].message.content

        return jsonify({'message': response_message})
    except Exception as e:
        logging.error(f"Error during OpenAI API call: {e}")
        return jsonify({'message': "An error occurred. Please try again later."})

if __name__ == '__main__':
    app.run()
