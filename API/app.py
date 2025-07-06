from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os

load_dotenv()

OPENROUTER = os.getenv("OPENROUTER_API_KEY")
GROQ = os.getenv("GROQ_API_KEY")

# Ensure Groq sees its key
os.environ["GROQ_API_KEY"] = GROQ

app = FastAPI(
    title="Langchain server",
    version="1.0",
    description="A simple API server"
)

# OpenRouter model
model_openrouter = ChatOpenAI(
    api_key=OPENROUTER,
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-4o",
    model_kwargs={"max_tokens": 300}
)

# Groq model
llm_groq = ChatGroq(
    model_name="llama3-70b-8192",
    api_key=GROQ,
    temperature=0.0,
)

# Prompts
prompt1 = ChatPromptTemplate.from_template(
    "Write me an essay about {topic} with 100 words"
)
prompt2 = ChatPromptTemplate.from_template(
    "Write me a poem about {topic} with 100 words"
)

# Routes
add_routes(
    app,
    prompt1 | model_openrouter,
    path="/essay",
)

add_routes(
    app,
    prompt2 | llm_groq,
    path="/poem",
)

app.openapi = lambda: None

# __main__ guard
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
