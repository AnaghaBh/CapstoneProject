import ollama

def call_llm(system_msg, user_msg, model="llama3:8b"):
    """Call Ollama LLM with system and user messages."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )
    return response['message']['content']