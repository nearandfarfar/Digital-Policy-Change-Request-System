
from pathlib import Path
from io import BytesIO

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from docx import Document
from crewai_cli.run_declarative_flow import load_declarative_flow

import os
import time
import requests

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

FLOW_PATH = (
    BASE_DIR
    / "src"
    / "digital_policy_change_request_system"
    / "flow.json"
)

# Limit HTTP request size to 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def execute_crewai_local(transcript):
    flow = load_declarative_flow(FLOW_PATH)
    result = flow.kickoff(
        inputs={"transcript": transcript}
    )
    return str(result)

def execute_crewai(transcript):
    mode = os.getenv("CREWAI_EXECUTION_MODE", "local").lower()

    if mode == "cloud":
        return execute_crewai_cloud(transcript)

    if mode == "local":
        return execute_crewai_local(transcript)

    raise ValueError(f"Unsupported execution mode: {mode}")


CREWAI_CLOUD_URL = (
    "https://digital-policy-change-request-system-v1-f57-e259db36.crewai.com"
)


def execute_crewai_cloud(transcript):
    """Execute the deployed CrewAI workflow through its API."""

    token = os.getenv("CREWAI_BEARER_TOKEN")

    if not token:
        raise RuntimeError("CREWAI_BEARER_TOKEN is missing")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 1: Start cloud execution
    response = requests.post(
        f"{CREWAI_CLOUD_URL}/kickoff",
        headers=headers,
        json={"inputs": {"transcript": transcript}},
        timeout=30
    )
    response.raise_for_status()

    kickoff_id = response.json()["kickoff_id"]

    print("CrewAI Cloud kickoff ID:", kickoff_id)

    # Step 2: Poll for completion
    deadline = time.monotonic() + 300

    while time.monotonic() < deadline:

        status_response = requests.get(
            f"{CREWAI_CLOUD_URL}/status/{kickoff_id}",
            headers=headers,
            timeout=30
        )
        status_response.raise_for_status()

        data = status_response.json()
        state = data.get("state")

        print("CrewAI Cloud state:", state)

        if state == "SUCCESS":
            result = data.get("result") or {}
            raw = result.get("raw")

            if not isinstance(raw, str):
                raise RuntimeError(
                    "Cloud execution completed without a text result"
                )

            return raw

        if state in ("FAILED", "FAILURE", "ERROR", "CANCELLED"):
            raise RuntimeError(
                f"CrewAI Cloud execution ended with state: {state}"
            )

        time.sleep(5)

    raise TimeoutError(
        f"Cloud execution did not finish within 300 seconds. "
        f"Kickoff ID: {kickoff_id}"
    )



def extract_docx_text(file_bytes):
    """Extract text from paragraphs and tables."""

    doc = Document(BytesIO(file_bytes))

    # Iterate through document blocks in their original order.
    parts = []

    for block in doc.iter_inner_content():
        if hasattr(block, "text") and not hasattr(block, "rows"):
            if block.text.strip():
                parts.append(block.text)

        elif hasattr(block, "rows"):
            for row in block.rows:
                cells = [cell.text.strip() for cell in row.cells]
                parts.append(" | ".join(cells))

    return "\n".join(parts)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/run")
def run_workflow():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON input"}), 400

    transcript = data.get("transcript")

    if not isinstance(transcript, str) or not transcript.strip():
        return jsonify({"error": "Transcript is required"}), 400

    try:
        result = execute_crewai(transcript)

        return jsonify({
            "status": "success",
            "result": result
        })

    except Exception:
        app.logger.exception("CrewAI execution failed")
        return jsonify({
            "status": "error",
            "message": "CrewAI execution failed"
        }), 500


@app.post("/upload")
def upload_document():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({"error": "No file selected"}), 400

    if not uploaded_file.filename.lower().endswith(".docx"):
        return jsonify({
            "error": "Only .docx files are supported"
        }), 400

    try:
        file_bytes = uploaded_file.read()
        transcript = extract_docx_text(file_bytes)

    except Exception:
        app.logger.exception("Document parsing failed")
        return jsonify({
            "error": "Could not read Word document"
        }), 400

    if not transcript.strip():
        return jsonify({
            "error": "Document contains no extractable text"
        }), 400

    try:
        result = execute_crewai(transcript)

        return jsonify({
            "status": "success",
            "filename": uploaded_file.filename,
            "transcript_length": len(transcript),
            "result": result
        })

    except Exception:
        app.logger.exception("CrewAI execution failed")
        return jsonify({
            "status": "error",
            "message": "CrewAI execution failed"
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
