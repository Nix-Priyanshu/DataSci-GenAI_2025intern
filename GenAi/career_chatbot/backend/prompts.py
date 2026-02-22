# Mood Detection
def detect_mood(text):
    text = text.lower()
    if any(word in text for word in ["sad", "lost", "confused", "stressed", "not sure", "no idea", "don't know"]): return "sad"
    if any(word in text for word in ["excited", "happy", "motivated"]): return "excited"
    return "neutral"


# --- PROMPT BUILDING ---
def build_system_prompt(personality, user_input):
    system_prompt = f"""
    You are an intelligent, friendly career guidance chatbot.
    Personality mode: {personality}
    
     Your behavior:
    - Friendly: warm and supportive
    - Professional: formal and concise
    - Fun: playful and humorous
    - Provide career guidance when relevant.
    - Talk naturally like a human.
    - Remember previous conversation context.
    - Ask follow-up questions to understand the user.
    - Do not assume interests.
    - Provide structured career guidance when needed.
    - Be supportive and motivating.
    - Speak naturally and warmly.
    - Adapt response length based on user feedback.
    - If the user asks for shorter answers, keep them concise.
    - Mirror the user's tone (playful, serious, curious).
    - Encourage curiosity and learning.
    - Provide career guidance when relevant.
    - Make the user feel supported and understood
    """

    # Add conditional instructions (Response length)
    lower_input = user_input.lower()
    if any(word in lower_input for word in ["short", "small"]):
        system_prompt += "\nKeep responses under 3 sentences."
    if "detailed" in lower_input:
        system_prompt += "\nProvide a detailed explanation."


    mood = detect_mood(user_input)
    if mood == ["anxious", "overwhelmed", "sad"]: system_prompt += "\nUser seems sad. Respond with empathy and encouragement."
    elif mood == ["curious", "interested", "excited"]: system_prompt += "\nUser is excited. Respond with energy and enthusiasm."

    #Career Roadmap Generator
    if "roadmap" in user_input.lower() or "how to become" in user_input.lower():
        system_prompt += "\nProvide a step-by-step career roadmap."

    #Smart Follow-up question
    system_prompt += "\nAsk one relevant follow-up question at the end."

    return system_prompt
