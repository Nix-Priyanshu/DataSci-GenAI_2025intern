from utils.kb_utils import get_kb_context
from utils.model_utils import generate_answer

# Custom QA Chain (simple + stable)
def qa_chain(query: str):
    data = get_kb_context(query)

    context = data["context"]
    sources = data["sources"]

    answer = generate_answer(query, context)

    return {
        "answer": answer,
        "sources": sources
    }

def log_interaction(query, response):
    with open("logs/rag_log.txt", "a") as f:
        f.write(f"User: {query}\n")
        f.write(f"Bot: {response}\n")
        f.write("-" * 40 + "\n")

