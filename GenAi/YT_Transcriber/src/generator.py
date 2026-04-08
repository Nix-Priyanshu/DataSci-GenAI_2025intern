import google.generativeai as genai
import os

# Best practice: Load your key from environment variables or Streamlit secrets
genai.configure(api_key=os.environ.get("Gemini-API-Key"))

model = genai.GenerativeModel("gemini-2.0-flash")
def generate_article(transcript):
    if not transcript:
        return "No transcript available."

    # Refining the prompt to force Markdown structure
    prompt = f"""
    You are a professional technical writer. Convert the following YouTube transcript into a 
    high-quality, insightful article formatted in Markdown.

    Structure requirements:
    1. **Catchy Title**: An engaging H1 header.
    2. **Introduction**: A brief overview of what the video covers.
    3. **Main Content**: Use H2 and H3 headers to break down the key points.
    4. **Key Takeaways**: A bulleted list of the most important lessons.
    5. **Conclusion**: A final summary.

    Tone: Informative, clear, and engaging.
    Transcript:
    {transcript}
    """

    try:
        # Generation configuration for better formatting
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7, # Adds a bit of creativity while staying factual
                top_p=0.95,
            )
        )
        
        if response and response.text:
            return response.text
        return "The AI returned an empty response."
        
    except Exception as e:
        return f"Error during generation: {str(e)}"
