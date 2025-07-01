import google.generativeai as genai 
genai.configure(api_key="Your_API_Key_Here")  # Replace with your actual API key

model = genai.GenerativeModel("gemini-2.5-flash")       
response = model.generate_content("You are a virtual assistant named Jarvis.")      
print(response.text)        
