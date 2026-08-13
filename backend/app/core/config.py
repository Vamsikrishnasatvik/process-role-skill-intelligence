import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/intelligence_graph",
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)