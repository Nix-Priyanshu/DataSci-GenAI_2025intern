# 🤖 HR Assistant Bot (RAG-based)

## 📌 Overview
This project is an AI-powered HR Assistant chatbot that answers employee queries using company policy documents. It uses Retrieval-Augmented Generation (RAG) to ensure responses are accurate and grounded in data.

---

## 🚀 Features
- 💬 Conversational Chat Interface (Streamlit)
- 📚 Knowledge Base Retrieval (AWS Bedrock)
- 🧠 Context-Aware Responses (Memory)
- 📄 Source Citation for transparency
- 📝 Interaction Logging
- ❌ Handles unknown queries gracefully

---

## 🛠️ Tech Stack
- Python
- Streamlit
- AWS Bedrock (Knowledge Base + Nova LLM)
- LangChain (PromptTemplate)
- Boto3

---

## 📂 Project Structure

MajorProject/
│
├── app.py
├── retriever_chain.py
├── utils/
│ ├── kb_utils.py
│ └── model_utils.py
├── web/
│ └── web_app.py
├── data/
├── logs/
└── README.md


---

## ⚙️ How It Works
1. User enters a query in the UI
2. Query is sent to the Knowledge Base
3. Relevant context is retrieved
4. LLM generates answer using context
5. Response + source displayed to user
6. Interaction is logged

---

## ▶️ Run the Project

```bash
streamlit run web/web_app.py
🎯 Example Queries
What is the leave policy?
Can unused leave be carried forward?
What is the remote work policy?
📌 Future Improvements
Voice input
Role-based access (HR/Admin)
Multi-document support
Better source attribution