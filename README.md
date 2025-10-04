Batcave-backend (DroneWatch) - Django backend

Quick start

1. Create a venv and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```

4. POST recordings to `/api/recordings/` (see API docs below)

API (minimal)
- POST /api/recordings/ - multipart/form-data with `audio_file` (file) and optional `device_id` (string) and `timestamp` (ISO8601). Returns JSON with saved record id.
# batcave-backend
