from config.settings import client


def answer_question(question, vector_db):

    chunk_count = vector_db._collection.count()

    if chunk_count < 100:
        k = 4
    elif chunk_count < 500:
        k = 8
    elif chunk_count < 1000:
        k = 12
    else:
        k = 16

    docs = vector_db.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=k * 3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a PDF assistant.

Answer ONLY using the provided context.

If the answer is not present,
say:

'I could not find that information in the uploaded PDF.'

Context:

{context}
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content
    

    sources = []

    for doc in docs:

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        source = f"📄 Page {page}"

        if source not in sources:

            sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }