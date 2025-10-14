# Portfolio AI

**Status**: In progress \
**Expected Release**: 31/10/2025

Will be available by end of october (hopefully) on https://l145.be/ so that you can ask questions to the AI version of me!

## Features

- **AI-Powered Q&A:** Ask questions in plain language and get answers based directly on my skills, projects, experience, and more.
- **Custom RAG Pipeline:** A custom-built pipeline ensures that the answers are highly relevant and drawn from optimized data chunks.
- **Fact-Checked Responses:** The AI is instructed to only use the provided context from my portfolio, preventing it from making things up.
- **Fast & Efficient:** Uses the Groq API for real-time, low-latency responses.
- **Portfolio Integration (todo)**: Direct integration into personal portfolio site https://l145.be/.

## How It Works (The Pipeline)

1.  **Ingestion:** My portfolio data is manually chunked into focused pieces for optimal embedding quality.
2.  **Embedding:** Each chunk is converted into a vector using the `all-MiniLM-L6-v2` model.
3.  **Storage:** These vectors are stored in a ChromaDB vector database.
4.  **Retrieval:** When you ask a question, it's converted into a vector to find the most similar (relevant) data chunks from the database.
5.  **Generation:** Your original question and the retrieved data are sent to the Groq LLM, which generates a coherent, context-aware answer.

## Tech Stack

- **LLM:** Groq (using `openai/gpt-oss-20b`)
- **Vector DB:** ChromaDB (Local for dev, Chroma Cloud for prod)
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Llama-index (LEGACY):** Various library features, scrapped due to bad accuracy and chromadb sync issues, would be better accuracy if there was more data, which is not not applicable to a simple Portfolio RAG

## Development Setup

1.  **Clone the repository.**
2.  **Start the local ChromaDB server:**

    ```powershell
    # Using PowerShell
    pwsh ./chroma-start.ps1
    ```

    or

    ```bash
    # Using bash/terminal
    chroma run --host localhost --port 8000
    ```
4.  Go through ```pure_chroma.ipynb``` if you want to try it yourself.

## Roadmap & Status

- [x] Hyper-optimize and manually chunk all portfolio data.
- [x] Build and test the dense RAG pipeline locally.
- [ ] **Chroma Cloud:** Resolve the "permission denied" error to connect to the cloud instance.
- [ ] **Backend Integration:** Finalize the architecture for the backend API.
- [ ] **Frontend Integration:** Design and build the AI chat section for my portfolio at [l145.be](https://l145.be/).

## Contact

- **Author:** Aryan Shah
- **Email:** [aryan.shah@l145.be](mailto:aryan.shah@l145.be)
- **GitHub:** [l145dev](https://github.com/l145dev/)
- **LinkedIn:** [Aryan Shah](https://www.linkedin.com/in/aryan-shah-l145/)
