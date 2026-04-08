import boto3
import sys

# --- CONFIGURATION ---
REGION = "ap-south-1"
KNOWLEDGE_BASE_ID = "EMHBRAIUUF"

# Initialize KB Client
try:
    kb_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
except Exception as e:
    print(f"Error initializing KB client: {e}")
    sys.exit(1)

def get_kb_context(query):
    """Retrieves document chunks from the Bedrock Knowledge Base."""
    try:
        response = kb_runtime.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={'text': query}
        )
        results = response.get('retrievalResults', [])
        contexts = []
        sources = []

        for r in results:
            text = r['content']['text']
            contexts.append(text)

                # Dummy source (you can customize later)
            sources.append("HR Policy Document")

        return {
            "context": "\n".join(contexts),
            "sources": list(set(sources))
        }
    except Exception as e:
        return f"Retrieval Error: {e}"
