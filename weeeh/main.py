import os
import re

import chromadb
import fitz
from dotenv import load_dotenv
from google import genai


load_dotenv()


def load_and_chunk_document(document_path):
    doc = fitz.open(document_path)

    full_text = ""

    for page in doc:
        full_text += page.get_text("text") + "\n"

    doc.close()

    heading_pattern = re.compile(
        r"(?m)^(\d+)\.\s+([^\n]+)"
    )

    matches = list(heading_pattern.finditer(full_text))

    if not matches:
        return []

    chunks = []

    for i, match in enumerate(matches):
        section = f"{match.group(1)}. {match.group(2).strip()}"

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(full_text)

        body = full_text[start:end]

        # Collapse line breaks into spaces
        body = re.sub(r"\s+", " ", body).strip()

        # 500-character windows
        # 420-character step
        for position in range(0, len(body), 420):
            text = body[position:position + 500].strip()

            if len(text) >= 60:
                chunks.append({
                    "section": section,
                    "text": text
                })

            if position + 500 >= len(body):
                break

    return chunks


def retrieve_sections(question, embedding_model, collection):
    """
    ChromaDB handles the embedding internally.
    embedding_model is retained in the signature because
    the assignment requires this function signature.
    """

    results = collection.query(
        query_texts=[question],
        n_results=4,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        similarity = round(1 - distance, 2)

        retrieved_chunks.append({
            "chunk": document,
            "section": metadata["section"],
            "similarity": similarity
        })

    retrieved_chunks.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return retrieved_chunks


def augment_prompt(question, retrieved_chunks):
    context = []

    for i, item in enumerate(retrieved_chunks, 1):
        context.append(
            f"""Context {i}
Section: {item["section"]}
Excerpt: {item["chunk"]}"""
        )

    context_text = "\n\n".join(context)

    prompt = f"""
You are an employee policy assistant for Halcyon Logistics Pvt Ltd.

Answer the employee's question ONLY using the supplied policy excerpts.

Do not use outside knowledge.
Do not make assumptions.

Name the supporting policy section in your answer.

If the supplied excerpts do not contain the answer, state that
the matter is not covered in the provided policy excerpts.

Policy excerpts:

{context_text}

Employee question:
{question}

Answer only from the supplied excerpts and mention the
supporting section title.
""".strip()

    return prompt


def generate_answer(prompt, client):
    model_name = os.getenv("GEMINI_MODEL")

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text.strip()


def policy_qa_pipeline(question, document_path):

    # --------------------------------------------------
    # 1. Load and chunk document
    # --------------------------------------------------
    chunks = load_and_chunk_document(document_path)

    # --------------------------------------------------
    # 2. Create ChromaDB client
    # --------------------------------------------------
    chroma_client = chromadb.Client()

    collection_name = "employee_policy"

    # Delete previous collection if it exists
    try:
        chroma_client.delete_collection(
            collection_name
        )
    except Exception:
        pass

    # ChromaDB default embedding function
    collection = chroma_client.create_collection(
        name=collection_name,
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

    # --------------------------------------------------
    # 3. Prepare data
    # --------------------------------------------------
    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "section": chunk["section"]
        }
        for chunk in chunks
    ]

    # --------------------------------------------------
    # 4. Add documents
    # ChromaDB generates embeddings automatically
    # --------------------------------------------------
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    # --------------------------------------------------
    # 5. Retrieve relevant sections
    # --------------------------------------------------
    retrieved_chunks = retrieve_sections(
        question,
        None,
        collection
    )

    # --------------------------------------------------
    # 6. Augment prompt
    # --------------------------------------------------
    prompt = augment_prompt(
        question,
        retrieved_chunks
    )

    # --------------------------------------------------
    # 7. Gemini client for generation only
    # --------------------------------------------------
    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(
        api_key=api_key
    )

    # --------------------------------------------------
    # 8. Generate answer
    # --------------------------------------------------
    answer = generate_answer(
        prompt,
        client
    )

    # --------------------------------------------------
    # 9. Build unique source list
    # --------------------------------------------------
    sources = []

    for item in retrieved_chunks:
        if item["section"] not in sources:
            sources.append(item["section"])

    return {
        "question": question,
        "retrieved_chunks": retrieved_chunks,
        "sources": sources,
        "answer": answer
    }


if __name__ == "__main__":

    question = input("Enter your question: ").strip()

    if not question:
        print("Question cannot be empty.")
    else:
        result = policy_qa_pipeline(
            question,
            "data/employee_policy_handbook.pdf"
        )

        print(
            f"\nQuestion: {result['question']}"
        )

        print("\nRetrieved Sections:")

        for i, item in enumerate(
            result["retrieved_chunks"],
            1
        ):
            print(
                f"{i}. {item['section']} "
                f"(similarity: {item['similarity']:.2f})"
            )

        print(
            f"\nSources: {', '.join(result['sources'])}"
        )

        print("\nAnswer:")
        print(result["answer"])