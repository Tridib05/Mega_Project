import google.generativeai as genai

genai.configure(
    api_key="Your api key"
)
model = genai.GenerativeModel("gemini-1.5-flash") 
chat_log=''''''

response = model.generate_content(f"You are a person named Tridib who speaks Bengali as well as English. " \
            "You are from India and you are a coder. You analyze chat history and respond like Tridib." \
            "Output should be the next chat response as Tridib")
chat_history:{chat_log}
print(response.text)
