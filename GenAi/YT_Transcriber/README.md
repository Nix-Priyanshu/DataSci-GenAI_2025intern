# \# 🎥 YouTube → Article Generator

# 

# Convert any YouTube video into a structured article and downloadable PDF using AI.

# 

# \---

# 

# \## 🚀 Features

# 

# \- Extract YouTube video transcript automatically

# \- Generate a well-structured article using AI

# \- Save the generated article as a PDF

# \- Interactive Streamlit-based UI for easy usage

# 

# \---

# 

# \## 🛠️ Tech Stack

# 

# \- Python 3.10+

# \- Streamlit

# \- YouTube Transcript API

# \- Google Gemini AI (`google-generativeai`)

# \- FPDF (PDF generation)

# \- Optional: python-dotenv for API key management

# 

# \---

# 

# \## 📂 Project Structure

# 

# 

# yt\_article\_project/

# │

# ├── app.py # Main Streamlit application

# ├── src/

# │ ├── transcript.py # Fetches YouTube transcript

# │ ├── generator.py # Generates article using AI

# │ └── pdf\_writer.py # Saves article as PDF

# ├── output/ # Folder for PDF output

# └── requirements.txt

# 

# 

# \---

# 

# \## ⚡ How to Run

# 

# 1\. Clone the repository:

# 

# ```bash

# git clone <your\_repo\_link>

# cd yt\_article\_project

# Install dependencies:

# pip install -r requirements.txt

# Run the Streamlit app:

# streamlit run app.py

# Enter a YouTube URL and click Generate Article.

# Download the PDF after generation.

# 🔑 Notes

# Make sure your YouTube video has a transcript available

# Keep your API key secure. Use .env if necessary

# This project is fully local; no deployment required

