"""Run the Natural Science question set against the LLM and save the answers as CSV."""

import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

EVAL_DIR = Path(__file__).parent
QUESTIONS_FILE = EVAL_DIR / "questions.jsonl"
RESULTS_DIR = EVAL_DIR / "results"
CSV_FIELDS = ["id", "question", "reference", "answer", "latency_ms"]


def load_questions() -> list[dict[str, str | int]]:
    with QUESTIONS_FILE.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def ask_llm(client: OpenAI, model: str, question: str) -> tuple[str, int]:
    started = time.perf_counter()
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": question}]
    )
    latency_ms = round((time.perf_counter() - started) * 1000)
    return response.choices[0].message.content or "", latency_ms


def run_llm_mode() -> Path:
    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
    )
    model = os.getenv("LLM_MODEL", "vilab-qwen")

    RESULTS_DIR.mkdir(exist_ok=True)
    output = RESULTS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-{model.replace(':', '_')}.csv"
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for item in load_questions():
            answer, latency_ms = ask_llm(client, model, str(item["question"]))
            writer.writerow({**item, "answer": answer, "latency_ms": latency_ms})
            print(f"{item['id']}: {latency_ms} ms")
    return output


def main() -> None:
    load_dotenv()
    match os.getenv("EVAL_MODE", "llm"):
        case "llm":
            print(f"Saved results to {run_llm_mode()}")
        case "backend":
            sys.exit("EVAL_MODE=backend is not supported yet: the backend chat API does not exist.")
        case mode:
            sys.exit(f"Unknown EVAL_MODE '{mode}'. Use 'llm' or 'backend'.")


if __name__ == "__main__":
    main()
