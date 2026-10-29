#!/usr/bin/env python3
"""
BrownieCam Mobile Web Viewer & Gallery

Provides a responsive mobile web UI to view, download, and manage photos taken
with the BrownieCam, accessible over the Pi's local Wi-Fi or hotspot.
"""

from flask import Flask, render_template_string, send_from_directory, abort, jsonify
from pathlib import Path
from datetime import datetime
import config

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BrownieCam Gallery</title>
  <style>
    :root {
      --bg: #1c1815;
      --card-bg: #2b2520;
      --accent: #d4a373;
      --text: #faedcd;
      --muted: #a99b8d;
    }
    body {
      margin: 0;
      padding: 16px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, serif;
    }
    header {
      text-align: center;
      padding: 12px 0 24px 0;
      border-bottom: 1px solid #3d352e;
    }
    h1 {
      margin: 0;
      font-size: 1.8rem;
      letter-spacing: 2px;
      color: var(--accent);
      text-transform: uppercase;
    }
    .subtitle {
      font-size: 0.85rem;
      color: var(--muted);
      margin-top: 4px;
    }
    .gallery {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }
    .card {
      background: var(--card-bg);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      border: 1px solid #3d352e;
      display: flex;
      flex-direction: column;
    }
    .card img {
      width: 100%;
      height: 240px;
      object-fit: cover;
      background: #111;
      display: block;
      cursor: pointer;
    }
    .card-info {
      padding: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      color: var(--muted);
    }
    .btn-download {
      background: var(--accent);
      color: var(--bg);
      text-decoration: none;
      padding: 6px 12px;
      border-radius: 4px;
      font-weight: 600;
      font-size: 0.8rem;
    }
    .empty {
      text-align: center;
      color: var(--muted);
      margin-top: 60px;
      font-style: italic;
    }
  </style>
</head>
<body>
  <header>
    <h1>Premo Junior 1A</h1>
    <div class="subtitle">BrownieCam Digital Relay Gallery</div>
  </header>

  <main>
    {% if photos %}
    <div class="gallery">
      {% for photo in photos %}
      <div class="card">
        <a href="/photos/{{ photo.name }}" target="_blank">
          <img src="/photos/{{ photo.name }}" alt="{{ photo.name }}" loading="lazy">
        </a>
        <div class="card-info">
          <span>{{ photo.date }}</span>
          <a class="btn-download" href="/photos/{{ photo.name }}" download>Save</a>
        </div>
      </div>
      {% endfor %}
    </div>
    {% else %}
    <div class="empty">
      No exposures captured yet.<br>Click the Premo's shutter lever to take your first shot!
    </div>
    {% endif %}
  </main>
</body>
</html>
"""

@app.route("/")
def index():
    photo_files = sorted(
        config.PHOTO_DIR.glob("*.jpg"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    photos = [
        {
            "name": p.name,
            "date": datetime.fromtimestamp(p.stat().st_mtime).strftime("%b %d, %Y %I:%M %p")
        }
        for p in photo_files
    ]
    return render_template_string(HTML_TEMPLATE, photos=photos)

@app.route("/photos/<filename>")
def get_photo(filename):
    safe_path = Path(filename).name
    if not (config.PHOTO_DIR / safe_path).exists():
        abort(404)
    return send_from_directory(config.PHOTO_DIR, safe_path)

@app.route("/api/status")
def status():
    count = len(list(config.PHOTO_DIR.glob("*.jpg")))
    return jsonify({"status": "ready", "photo_count": count})

if __name__ == "__main__":
    app.run(host=config.WEB_HOST, port=config.WEB_PORT, debug=False)
