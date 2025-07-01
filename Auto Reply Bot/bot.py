import pyautogui        # For automating mouse and keyboard actions
import pyperclip        # For clipboard operations (copy/paste)
import time             # For adding delays
# For using Google Gemini API
import google.generativeai as genai     
# Configure your Gemini API key
genai.configure(api_key="Your Api Key")          

# Choose Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")               

def is_last_message_from_sender(chat_history, your_name="Tridib"):              
    """
    Returns True if the last message is NOT from you (i.e., from sender), else False.
    Adjust 'your_name' to match your WhatsApp display name.
    """
    # Split chat by newlines, get last non-empty line
    lines = [line.strip() for line in chat_history.strip().split('\n') if line.strip()]                     
    if not lines:
        return False
    last_line = lines[-1]                  # Get the last line of the chat history
    # If your name is NOT in last line, assume it's from sender
    return your_name not in last_line               

try:
    while True:
        # STEP 1: Click on WhatsApp icon to activate window
        pyautogui.click(1314, 1050)         # Change coordinates as per your screen
        time.sleep(1)                       # Wait for WhatsApp to come to the foreground
        # STEP 2: Select the message to reply (drag from one point to another)
        pyautogui.moveTo(692, 182)          # Move to the starting point of the message
        pyautogui.dragTo(1857, 938, duration=1.0,button = "left")          # Smooth drag

        # STEP 3: Copy selected message to clipboard
        pyautogui.hotkey('ctrl', 'c')       # Copy the selected text
        time.sleep(0.5)                     # Wait for clipboard to update

        # STEP 4: (Optional) Click elsewhere to remove selection highlight
        pyautogui.click(1875, 933)          # Click outside the selection area to remove highlight

        # STEP 5: Get copied message from clipboard
        chat_history = pyperclip.paste()    # Get the text from clipboard
        print(chat_history)                 # Print the copied message for debugging    

        if is_last_message_from_sender(chat_history, your_name="Tridib"):  # Change to your WhatsApp name
            prompt = f"""The following is a message from a WhatsApp chat. \n
            "You’re Tridib, a helpful coder from India who talks in a fun Bangla-English mix. Just read the last user message from the chat,\n
            understand it, and reply in a short, friendly, easy-going way – so it’s clear and casual, even if it’s small."\n
            Message: \"{chat_history}\"\nTridib's Reply:"""

            # STEP 6: Generate reply using Gemini
            response = model.generate_content(prompt)   # Generate the reply        
            reply = response.text.strip()               # Get the reply text
            print("Reply from Gemini:\n", reply)        # Print the reply for debugging
            # STEP 7: Copy the bot reply to clipboard
            pyperclip.copy(reply)              # Copy the reply to clipboard

            # STEP 8: Paste the reply in message box & send
            pyautogui.click(1300, 983)         # Click on message box
            time.sleep(0.3)                    # Wait for the message box to be ready
            pyautogui.hotkey('ctrl', 'v')      # Paste the reply from clipboard
            time.sleep(0.3)                    # Wait for paste to complete
            pyautogui.press('enter')           # Send the message
            print("Reply sent!")
        else:
            print("No new sender message. Waiting...")

        print("Waiting for next message... (Press Ctrl+C to stop)")
        time.sleep(5)  # Wait before next iteration
except KeyboardInterrupt:
    print("Bot stopped by user.")
