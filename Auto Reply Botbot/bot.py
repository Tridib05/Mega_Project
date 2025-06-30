import pyautogui
import pyperclip
import time
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="Your Api key")

# Choose Gemini model
model = genai.GenerativeModel("gemini-2.5-flash") 
'''
def is_last_message_from_sender(chat_log,sender_name=""):
    # Split the chat log into individual messages
    message = chat_log.strip().split("/2025]")[-1]
    if sender_name in message:
        return True
    return False
    '''
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
Respond like Tridib, who is a bit frustrated but always technical, logical, and reacts smartly.
The reply should sound human and casual.
Message: "{chat_history}"
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
