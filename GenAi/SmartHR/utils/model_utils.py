from langchain_core.prompts import PromptTemplate
import boto3
import json
import sys

# --- CONFIGURATION ---
REGION = "ap-south-1"
MODEL_ID = "apac.amazon.nova-lite-v1:0"

# Initialize Model client
try:
    br_runtime = boto3.client("bedrock-runtime", region_name=REGION)
except Exception as e:
    print(f"Error initializing Model client: {e}")
    sys.exit(1)

# Improved Prompt Template (clean formatting)
prompt_template = PromptTemplate.from_template("""
You are a professional HR Assistant.

Answer strictly using the provided context.
If the answer is not in the context, say:
"I do not have that information."

Give clear, well-formatted answers with proper spacing and bullet points if needed.

Context:
{context}

Question:
{question}
""")

def generate_answer(query, context):
    """Generates a grounded answer using Amazon Nova."""

    if not context or not context.strip() or "Error" in context:
        return "I couldn't find any information in the knowledge base to answer that."

    # Format prompt
    formatted_prompt = prompt_template.format(
        context=context.strip(),
        question=query.strip()
    )

    native_request = {
        "system": [
            {"text": "You are a professional HR Assistant."}
        ],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": formatted_prompt}
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 1000,
            "temperature": 0.0,
            "topP": 0.9
        }
    }

    try:
        response = br_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(native_request)
        )
        response_body = json.loads(response['body'].read())

        # Clean output formatting
        answer = response_body['output']['message']['content'][0]['text']

        return answer.strip()

    except Exception as e:
        return f"Model Error: {e}"
