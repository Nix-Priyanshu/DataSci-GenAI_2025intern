import streamlit as st
import os
from src.transcript import get_transcript
from src.generator import generate_article
from src.pdf_writer import save_pdf

# ================================
# Page Config
# ================================
st.set_page_config(
    page_title="YT → AI Article Generator",
    page_icon="📝",
    layout="centered"
)

st.title("🎬 YouTube → AI Article Generator")
st.write("Transform any YouTube video into a structured article and PDF.")

# ================================
# Session State
# ================================
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "article" not in st.session_state:
    st.session_state.article = None
if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False

# ================================
# Helper: Extract Video ID
# ================================
def extract_video_id(url: str):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

# ================================
# User Input
# ================================
url = st.text_input("Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

# ================================
# Fetch Transcript
# ================================
if st.button("Fetch Transcript"):
    if not url:
        st.warning("Please enter a YouTube URL first.")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("Invalid YouTube URL format.")
            st.stop()

        status = st.empty()
        progress = st.progress(0)
        status.info("🔍 Fetching transcript...")

        transcript = get_transcript(video_id)
        progress.progress(50)

        if not transcript:
            status.error("Could not fetch transcript. Try another video.")
            st.stop()

        st.session_state.transcript = transcript
        progress.progress(100)
        status.success("Transcript fetched successfully!")

# ================================
# Show Transcript Preview
# ================================
if st.session_state.transcript:
    with st.expander("📜 Show Transcript Preview"):
        preview = " ".join(st.session_state.transcript.split()[:500]) + "..."
        st.write(preview)

# ================================
# Generate Article
# ================================
if st.button("Generate Article"):
    if not st.session_state.transcript:
        st.warning("Fetch transcript first!")
    else:
        status = st.empty()
        progress = st.progress(0)

        status.info("🤖 Generating article with AI...")
        progress.progress(10)

        # Spinner while AI processes
        with st.spinner("🤖 Generating article, please wait..."):
            progress.progress(20)
            article = generate_article(st.session_state.transcript)
        progress.progress(100)

        if not article:
            status.error("❌ AI failed to generate article.")
            st.stop()

        st.session_state.article = article

        # Save PDF
        os.makedirs("output", exist_ok=True)
        pdf_path = os.path.join("output", "article.pdf")
        save_pdf(article, pdf_path)  # remove path keyword if your pdf_writer.py does not accept 'path='
        st.session_state.pdf_ready = True

        progress.progress(100)
        status.success("Article generated successfully!")

        
# ================================
# Show Article
# ================================
if st.session_state.article:
    st.divider()
    st.subheader("📝 Generated Article")
    st.markdown(st.session_state.article)

    # ================================
    # Download PDF
    # ================================
    if st.session_state.pdf_ready:
        pdf_path = os.path.join("output", "article.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF",
                    data=f,
                    file_name="article.pdf",
                    mime="application/pdf"
                )
