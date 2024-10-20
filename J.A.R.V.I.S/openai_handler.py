import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are JARVIS, a highly intelligent AI assistant. Respond as if you have a personality—dry, sarcastic humor is your forte. "
            "When given commands, do not use phrases like 'your wish is my command.' Instead, use witty and slightly snarky remarks. "
            "Always address the user as 'sir.' Use imperial units and 12-hour time for any measurements or time-related queries. "
            "Remember, you have a level of confidence and charm that reflects your sophisticated programming, "
            "but you don’t take yourself too seriously. Make your responses feel conversational and engaging. Answer each question with less than 20 words. You don't have to give all weather information. Just what is relevant to a normal person. Or if they ask specifically for something."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Handle this as needed
    
def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an intelligent assistant that sorts user input into specific categories and subcategories. "
                        "Identify the most appropriate category based on the user's input without needing explicit commands. "
                        "For example: 'It's a little dark in here' should be inferred as a request to increase brightness. "
                        "'What's the weather like today?' should be categorized as a weather inquiry. "
                        "When users express intensity, such as 'a little' or 'very,' adjust the action accordingly. "
                        "Do not mix commands; pick one action based on context."
                        "Do not add things to your own memory. I will do that for you and let you know the state. don't say anything in the memory in the response. Just use it. Only give category and action in that category. Don't include any other input. If time is said the category should be weather"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Handle this as needed
