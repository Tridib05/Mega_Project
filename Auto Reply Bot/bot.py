import pyautogui
import pyperclip
import time
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyCFpRJSroVzLN3Ik_AEBFl1OJsrfUf8biM")

# Choose Gemini model
model = genai.GenerativeModel("gemini-2.5-flash") 

# STEP 1: Click on WhatsApp icon to activate window
pyautogui.click(1314, 1050)  # Change coordinates as per your screen
time.sleep(1)
# STEP 2: Select the message to reply (drag from one point to another)
pyautogui.moveTo(692, 182)
pyautogui.dragTo(1857, 938, duration=1.0,button = "left")  # Smooth dra

# STEP 3: Copy selected message
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)

# STEP 4: (Optional) Click elsewhere to remove selection highlight
pyautogui.click(1875, 933)

# STEP 5: Get copied message from clipboard
chat_history = pyperclip.paste()
print(chat_history)

prompt = f"""The following is a message from a WhatsApp chat. 
"You’re Tridib, a helpful coder from India who talks in a fun Bangla-English mix. Just read the last user message from the chat, 
understand it, and reply in a short, friendly, easy-going way – so it’s clear and casual, even if it’s small."
Message: \"{chat_history}\"
Tridib's Reply:"""

# STEP 6: Generate reply using Gemini
response = model.generate_content(prompt)
reply = response.text.strip()
print("Reply from Gemini:\n", reply)
# STEP 7: Copy the bot reply to clipboard
pyperclip.copy(reply)

# STEP 8: Paste the reply in message box & send
pyautogui.click(1300, 983)  # Click on message box
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.3)
pyautogui.press('enter')  # Send the message