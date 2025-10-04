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


## Audio Processing Dependencies

This project uses **pydub** to handle audio files.  
To enable full audio processing (reading metadata, format conversion, etc.), your system must have **ffmpeg** installed and available in your PATH.

### Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```
**macOS(Homebrew):**
```bash
brew install ffmpeg
```