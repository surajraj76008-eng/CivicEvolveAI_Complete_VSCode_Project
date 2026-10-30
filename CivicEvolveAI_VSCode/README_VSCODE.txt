CIVICEVOLVEAI - VS CODE PROJECT

FILES
- index.html: frontend (login, Emergency/Non-Emergency forms, government dashboard columns)
- app.py: Flask backend/API
- requirements.txt: Python dependencies
- run_windows.bat: quick start on Windows
- uploads/: saved uploaded images (created/used by app)
- reports.json: report records (created after the first report)

RUN IN VS CODE (WINDOWS)
1. Extract this ZIP folder.
2. Open VS Code > File > Open Folder > select CivicEvolveAI_VSCode.
3. Open Terminal > New Terminal.
4. Run: python -m pip install -r requirements.txt
5. Run: python app.py
6. Keep the terminal open.
7. In Edge, open: http://127.0.0.1:5000
8. Submit a test report. API check: http://127.0.0.1:5000/api/reports

If `python` is not recognized, try `py -m pip install -r requirements.txt` and `py app.py`.

NOTE
This local demo saves reports to reports.json on this computer. It is not a deployed/public backend. For an EdgeOne Pages public website, deploy app.py to an online backend host and update API_URL in index.html to that backend's HTTPS endpoint. Login in this HTML is demo UI only, not secure production authentication.


DEMO SAMPLE DATA
----------------
This project includes six fictional sample reports in reports.json (3 emergency and 3 non-emergency) so the dashboard is populated for demonstration. These are mock records, not real public reports. Delete reports.json and restart the app if you want to start with an empty report list; the backend will recreate storage after the next submission.
