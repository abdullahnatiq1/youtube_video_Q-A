import openai
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY is missing from .env file!")

client = openai.OpenAI(
    api_key  = api_key,
    base_url = "https://api.groq.com/openai/v1",
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection    = chroma_client.get_or_create_collection(name="youtube_collection")