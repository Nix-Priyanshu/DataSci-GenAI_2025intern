import streamlit as st
import os
from src.transcript import get_transcript
from src.generator import generate_article
from src.pdf_writer import save_pdf

st.set_page_config(page_title="YT to Article", layout="centered")

st.title("🎥 YouTube → Article Generator")
st.write("Convert any YouTube video into a structured article + PDF")

url = st.text_input("Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

if st.button("Generate Article", use_container_width=True):
    if not url:
        st.warning("Please enter a YouTube URL first.")
    else:
        try:
            video_id = extract_video_id(url)
            if not video_id:
                st.error("Invalid YouTube URL format.")
                st.stop()

            # Create a status container for a cleaner UI
            status = st.status("Processing your request...")
            
            status.write("🔍 Fetching transcript...")
            transcript = get_transcript(video_id)

            if not transcript:
                status.update(label="Failed to fetch transcript", state="error")
                st.error("❌ This video has no transcript. Try another video.")
                st.stop()

            status.write("🤖 Generating article with AI...")
            article = generate_article(transcript)

            status.write("📄 Creating PDF document...")
            # Ensure output directory exists
            os.makedirs("output", exist_ok=True)
            pdf_path = "output/output.pdf"
            save_pdf(article, filename=pdf_path)

            status.update(label="✅ Article Generated Successfully!", state="complete")

            # Display Content
            st.divider()
            st.subheader("Generated Article")
            st.markdown(article) # Using markdown is better for structured text

            # Download Button
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download PDF",
                        data=f,
                        file_name="insightful_article.pdf",
                        mime="application/pdf"
                    )

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
