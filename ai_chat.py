'''
    AI chat Integration using Groq API
    Demonstrates: API calls, error handling, conversation managment.
'''

import requests
from config import GROQ_API_KEY, GROQ_API_URL, AI_MODEL, AI_MODEL_FALLBACK, SYSTEM_PROMPT

def get_ai_response(user_message, conversation_history=None):
    '''
       Send a message to the AI and get a response.
       
       Parameters:
       - user_message: what the user just typed.
       - conversation_history: List of previous messages for context.
       
       why pass history? AI has no memory. We must send the whole conversation
       each time so it knows what was discussed.
    '''
    # Build the messages list for the API
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add conversation history if we have it.

    if conversation_history:
        for sender, content in conversation_history:
            role = 'user' if sender == 'user' else 'assistant'
            messages.append({'role': role, 'content': content})

    # Add the current user message
    messages.append({'role': 'user', 'content': user_message})

    # Try primary model, then fall back
    models_to_try = [AI_MODEL, AI_MODEL_FALLBACK]

    for model in models_to_try:
        try:
            response = call_groq_api(messages, model)
            if response:
                return response
        except Exception as e:
            print(f'Model {model} failed: {e}')
            continue

    # if all models fail, return a fallback message
    return "Sorry, I'm having trouble responding right now. please try again."

def call_groq_api(messages, model):
    '''
       make the actual API call to Groq.
       
       This is similar to how youd call any REST API:
       1. Set up headers(authentication)
       2. Set up the request body (data)
       3. Make the POST request.
       4. Parse the response
    '''

    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': 500,
        'temperature': 0.7
    }

    response = requests.post (
        GROQ_API_URL,
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f'API error: {response.status_code}')
    