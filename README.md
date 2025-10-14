# Portfolio AI

**Status**: In progress
**Expected Release**: 31/10/2025

Will be available by end of october (hopefully) on https://l145.be/ so that you can ask questions to the AI version of me!

## Features
- Hyper optimized portfolio data
- Custom Dense RAG pipeline
  -  Ingest data (array of objects with id, document/text, metadata) -> Chunked manually for optimal vectors
  -  Process data (ids, documents/texts, metadatas)
  -  Initialize chromadb locally on dev server - TERMINAL: ```pwsh ./chroma-start.ps1``` or ```chroma run --host localhost```
  -  Initialize chromadb locally on dev server - NOTEBOOK
  -  Embedding (all-MiniLM-L6-v2) + Add to collection in Vector DB locally (ChromaDB)
  -  Manual testing with chroma collection querying (n = 5)
  -  Push to Chroma Cloud when satisfied: ```chroma copy --to-cloud --all```
  -  Manual testing cloud client querying (in progress - permission to connect to my own cloud instance being denied by chroma 🥲)
- Backend integration (in progress - architecture not yet fixed): serves requests to get responses from Vector DB through chroma querying
- Frontend integration (todo): design and add section for AI in portfolio at https://l145.be/

## Contact

- **Author:** Aryan Shah
- **Email:** [aryan.shah@l145.be](mailto:aryan.shah@l145.be)
- **GitHub:** [l145dev](https://github.com/l145dev/)
- **LinkedIn:** [Aryan Shah](https://www.linkedin.com/in/aryan-shah-l145/)
