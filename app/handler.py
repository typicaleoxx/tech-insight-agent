import time
from app.utils import logger
from app.utils.config import MAX_EXECUTION_TIME

# Lambda calls this function — event comes from EventBridge, context is AWS metadata
def lambda_handler(event, context):
    start = time.time()
    logger.info("handler", "pipeline started")

    try:
        # --- stage 1: ingest raw topics from external sources ---
        # placeholder until Sprint 2 wires up the real ingestion layer
        raw_topics = _ingest()

        # bail early if nothing came back — no point running the rest
        if not raw_topics:
            logger.warn("handler", "no topics ingested, exiting early")
            return _response(200, "no topics found")

        # --- stage 2: filter and rank to pick the single best topic ---
        top_topic = _filter_and_rank(raw_topics)

        # --- stage 3: send topic to the LLM and get back structured insight ---
        insight = _extract_insight(top_topic)

        # --- stage 4: turn insight into linkedin post + portfolio article ---
        content = _generate_content(insight)

        # --- stage 5: validate quality before we bother saving anything ---
        if not _validate(content):
            logger.error("handler", "content failed validation, skipping storage")
            return _response(422, "content did not pass quality check")

        # --- stage 6: write outputs to S3 ---
        _store(content)

        elapsed = round(time.time() - start, 2)
        logger.info("handler", "pipeline finished", {"elapsed_seconds": elapsed})

        # warn if we're cutting it close to the 8-second soft limit
        if elapsed > MAX_EXECUTION_TIME:
            logger.warn("handler", "execution exceeded soft time limit", {"elapsed": elapsed})

        return _response(200, "ok")

    except Exception as e:
        # catch-all so Lambda always returns a clean response, never a raw traceback
        logger.error("handler", f"unhandled exception: {str(e)}")
        return _response(500, "internal error")


# --- pipeline stage stubs — each will be filled in across future sprints ---

def _ingest():
    # Sprint 2 will replace this with real Hacker News / GitHub / RSS calls
    return []

def _filter_and_rank(topics):
    # Sprint 3 will add keyword filtering + scoring logic here
    return topics[0] if topics else None

def _extract_insight(topic):
    # Sprint 4 will call the Gemini API here with a strict prompt template
    return {}

def _generate_content(insight):
    # Sprint 4 will produce a linkedin string and a portfolio markdown string
    return {"linkedin": "", "portfolio": ""}

def _validate(content):
    # Sprint 5 will check length, quality, and reject empty outputs
    return bool(content.get("linkedin") and content.get("portfolio"))

def _store(content):
    # Sprint 5 will write linkedin/latest.txt and portfolio/latest.md to S3
    pass


# keep the response shape consistent so API Gateway never chokes on it
def _response(status_code: int, message: str) -> dict:
    return {"statusCode": status_code, "body": message}
