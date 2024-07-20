import os
import google.generativeai as genai

# Replace with your actual API key or use environment variables
api_key = "AIzaSyBraBcj2IpRJD6obNLAHQR-QisN7MAnRUU"
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="This is a company management system.",
)

# Initialize chat session
chat_session = model.start_chat(history=[])

print("hello  : ")

while True:
    user_input = input("you: ")

    # Send the user input to the model and get the response
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Print the response
    print(model_response)
    print()

    # Append to history
    history = [
        {"role": "user", "parts": [user_input]},
        {"role": "model", "parts": [model_response]}
    ]
