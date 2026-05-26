# Web-saku Petugas SE2026 — SEROJA

Member login portal for field officers of **Sensus Ekonomi 2026 (SE2026)** at BPS Kabupaten Sukoharjo, nicknamed **SEROJA** (Sensus Ekonomi Sukoharjo Juara).

## Project Overview

A lightweight static web app with no external package dependencies. It uses:
- **Vanilla HTML5, CSS3, JavaScript** for the frontend
- **Python `http.server`** (`server.py`) to serve files on port 5000
- **GitHub API** (in the admin panel) to persist schedule data to a GitHub repository
- **sessionStorage** for login session management

## How to Run

The app starts automatically via the `Start application` workflow which runs:
```
python3 server.py
```
This serves all files on `http://0.0.0.0:5000`.

## Pages

- `index.html` — Main login page and member dashboard
- `organik.html` — Dashboard for "Organik" users (BPS staff)
- `admin.html` — Admin panel to manage event schedules (syncs to GitHub)
- `jadwal.html` — Embedded BPS Sukoharjo Google Calendar

## Login Credentials

Defined in `script.js`:
| Username     | Password     | Redirects to     |
|--------------|--------------|------------------|
| admin        | password123  | Member dashboard |
| ORGANIK3311  | SE26-Org     | Member dashboard |
| MITRA3311    | SE26-ptg     | organik.html     |

Admin panel password: `ADMIN3311` (requires a GitHub Classic Token to sync data)

## User Preferences

- Keep the orange/blue gradient theme consistent across all pages
- Indonesian language UI (Bahasa Indonesia)
- Mobile-first responsive design
