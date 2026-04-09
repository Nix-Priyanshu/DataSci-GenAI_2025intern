import google.generativeai as genai

# ================================
# Configure Gemini API (no env)
# ================================
API_KEY = "Your Api Key"  # replace with your key or input via Streamlit
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# ================================
# Generate Article from Transcript
# ================================
def generate_article(transcript: str) -> str:
    """
    Converts YouTube transcript into a well-structured article in Markdown.
    Structure:
    - H1 Title
    - Introduction
    - H2/H3 Main Points
    - Key Takeaways (bullet points)
    - Conclusion
    """
    if not transcript:
        return "No transcript available to generate article."

    prompt = f"""
    You are a professional technical content writer. Convert the transcript below
    into a **high-quality, structured article in Markdown** format.

    REQUIREMENTS:
    1. **Title** (H1) – catchy and relevant
    2. **Introduction** – brief overview
    3. **Main Content** – H2/H3 headers for key points
    4. **Key Takeaways** – bulleted list
    5. **Conclusion** – final summary

    Tone: Clear, engaging, and informative.

    Transcript:
    {transcript}
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,  # some creativity, but factual
                top_p=0.9,
            )
        )

        if response and response.text:
            return response.text
        else:
            return "AI returned an empty response."
    except Exception as e:
        return f"Error generating article: {str(e)}"
