import requests
import gradio as gr

# Set your API key
api_key = "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"

# Define the API endpoint
api_endpoint = "https://api.groq.com/openai/v1/chat/completions"

# Initialize conversation history
conversation_history = []

# Define the chatbot function with conversation history
def chatbot_response(user_input):
    global conversation_history

    # Append user message to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": conversation_history,
        "model": "mixtral-8x7b-32768",  # Replace with the correct model ID
        "max_tokens": 150
    }
    
    response = requests.post(api_endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        bot_response = response.json().get("choices")[0]["message"]["content"]
        
        # Append bot response to conversation history
        conversation_history.append({"role": "assistant", "content": bot_response})
        
        return bot_response
    else:
        return f"Error: {response.status_code} - {response.text}"

# Create the Gradio interface without theme and layout arguments
iface = gr.Interface(
    fn=chatbot_response, 
    inputs=gr.Textbox(label="Your Message"), 
    outputs=gr.Textbox(label="Bot Response"),
    title="Advanced Groq Chatbot",
    description="An advanced chatbot interface using Groq's LLM with conversation history."
)

# Launch the interface
iface.launch()
