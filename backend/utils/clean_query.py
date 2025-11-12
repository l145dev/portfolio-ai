def clean_query(groq_client, query: str) -> str:
    cleaned_query = ""

    # to only have 1 space between words at most
    prev_space = False

    for c in query:
        # only account for alphabet char, digit or space
        if c == " ":
            if not prev_space:
                prev_space = True
                cleaned_query += c
                

        elif c.isalpha() or c.isdigit():
            prev_space = False
            cleaned_query += c

    # intent clarification and query optimization
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Rephrase the user query minimally, preserving meaning, to maximize semantic match accuracy for vector database retrieval. Only return the rephrased query."
            },
            {
                "role": "user",
                "content": f"User query to rephrase minimally: {cleaned_query}",
            }
        ],
    )

    cleaned_query = completion.choices[0].message.content

    return str(cleaned_query)