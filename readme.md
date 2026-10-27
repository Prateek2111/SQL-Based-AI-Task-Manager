# Taskflow AI

A conversational task manager built with Streamlit, LangChain, Groq, and SQLAlchemy.

Taskflow AI is a conversational task-management web app. Users can create, view, update, prioritize, complete, and delete tasks by chatting naturally with an AI assistant.

Built with Streamlit for the interface, LangChain and Groq for the AI agent, and SQLAlchemy with SQLite/PostgreSQL for task storage.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your_groq_api_key"
DATABASE_URL = "postgresql://USER:PASSWORD@HOST:5432/DATABASE"
```

Without `DATABASE_URL`, the app uses a local SQLite database (`todos.db`).

## Deploy

1. Create a PostgreSQL database with Supabase or Neon.
2. Push this project to GitHub. Do not commit secrets.
3. On [Streamlit Community Cloud](https://share.streamlit.io/), create an app with `app.py` as the entrypoint.
4. Add `GROQ_API_KEY` and `DATABASE_URL` in **Advanced settings → Secrets**.

> Use PostgreSQL for deployment. Local SQLite files are not reliably persistent on Streamlit Community Cloud.
