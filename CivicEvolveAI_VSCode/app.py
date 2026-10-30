from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
import json
import uuid

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_FILE = BASE_DIR / "reports.json"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
CORS(app)  # Allows the HTML frontend to call this local API.
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024  # 12 MB maximum upload


def read_reports():
    """Read reports from JSON storage; return an empty list if not created yet."""
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def write_reports(reports):
    """Persist reports to the local JSON file."""
    DATA_FILE.write_text(json.dumps(reports, indent=2), encoding="utf-8")


@app.get("/")
def home():
    """Serve the project frontend from Flask so it can be opened at localhost."""
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/reports")
def get_reports():
    return jsonify(read_reports())


@app.post("/api/reports")
def create_report():
    form = request.form
    emergency_type = (form.get("emergency_type") or form.get("issue_type") or "Civic issue").strip()
    is_non_emergency = emergency_type.lower().startswith("non-emergency:")

    image_url = ""
    image = request.files.get("image") or request.files.get("photo")
    if image and image.filename:
        safe_name = secure_filename(image.filename)
        extension = Path(safe_name).suffix[:12]
        filename = f"{uuid.uuid4().hex}{extension}"
        image.save(UPLOAD_DIR / filename)
        image_url = f"/uploads/{filename}"

    report = {
        "id": uuid.uuid4().hex,
        "name": form.get("name", "").strip(),
        "email": form.get("email", "").strip(),
        "emergency_type": emergency_type,
        "report_type": "non-emergency" if is_non_emergency else "emergency",
        "location": form.get("location", "").strip(),
        "description": form.get("description", "").strip(),
        "latitude": form.get("latitude") or form.get("photo_latitude"),
        "longitude": form.get("longitude") or form.get("photo_longitude"),
        "photo_taken_at": form.get("photo_taken_at", ""),
        "image_url": image_url,
        "status": "Report Received",
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    reports = read_reports()
    reports.insert(0, report)
    write_reports(reports)
    return jsonify({"message": "Report submitted successfully", "report": report}), 201


@app.put("/api/reports/<report_id>")
def update_report(report_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    allowed_statuses = {"Report Received", "Under Review", "Action Taken", "Resolved"}
    if new_status not in allowed_statuses:
        return jsonify({"error": "Invalid status"}), 400

    reports = read_reports()
    for report in reports:
        if report.get("id") == report_id:
            report["status"] = new_status
            write_reports(reports)
            return jsonify({"message": "Status updated", "report": report})
    return jsonify({"error": "Report not found"}), 404


@app.get("/uploads/<path:filename>")
def uploaded_image(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Image is too large. Maximum upload size is 12 MB."}), 413


if __name__ == "__main__":
    print("CivicEvolveAI is running at http://127.0.0.1:5000")
    print("Keep this terminal open while testing the website.")
    app.run(host="127.0.0.1", port=5000, debug=True)
