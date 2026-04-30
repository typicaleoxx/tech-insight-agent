import os

# hard limits from GUARDRAILS.md — never change these values
MAX_LLM_CALLS = 2
MAX_EXECUTION_TIME = 8
MAX_TOPIC_LENGTH = 300
MAX_OUTPUT_WORDS = 500
MAX_FILE_SIZE_KB = 50

# pull env vars early so everything downstream just reads from this module
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

# s3 paths match the structure defined in the PRD
S3_PATHS = {
    "linkedin": "linkedin/latest.txt",
    "portfolio": "portfolio/latest.md",
    "archive": "archive/",
}

# sources we pull from — easy to toggle without touching pipeline logic
INGESTION_SOURCES = {
    "hacker_news": True,
    "github_trending": True,
    "rss": True,
}

# cap retries low so we never loop forever on a bad API day
MAX_RETRIES = 2
RETRY_BACKOFF_BASE = 2
