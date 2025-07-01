# ai-agent-trello

## Goal
Build a local-first AI assistant that reads meeting transcripts, extracts tasks
using an LLM, classifies them by project using FAISS, compares them to existing
Trello cards, and provides a Streamlit interface to review and sync updates.

## Key Features
1. **Upload Transcript**: Drag-and-drop transcripts in Streamlit.
2. **LLM Task Extraction**: Use OpenAI GPT to extract structured task data.
3. **Project Classification**: Match tasks to the correct Trello project using a
   local FAISS vector store.
4. **Trello Sync**: Compare extracted tasks to existing cards and create or update as needed.
5. **Confirmation Step**: Review proposed changes before syncing.

## Tech Stack
- Python 3.10+
- LangChain
- OpenAI API
- FAISS (local vectorstore)
- Trello API
- Streamlit
- Docker & dotenv

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.sample` to `.env` and fill in your API keys.
3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

You can also build and run with Docker:

```bash
docker build -t ai-trello-agent .
docker run --env-file .env -p 8501:8501 ai-trello-agent
```
