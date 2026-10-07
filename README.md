# IR Flows

A responsive AI agency website built with Python and Flask. Includes a service-led homepage, team and blog pages, and a validated inquiry form backed by SQLite.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

The server uses port 8000 by default; set `PORT` to override it. Run checks with `.venv/bin/python -m unittest discover -s tests -v`.

## Content and branding

- Edit `templates/index.html` for homepage copy and `templates/content.html` for team and blog content. These pages currently use explicit coming-soon states until real profiles and articles are supplied.
- `static/style.css` contains the responsive palette and typography. Both supplied reference URLs were inaccessible from the build environment, so their exact layouts and font choices have not been verified. Typography uses local Arial and Georgia without external font requests.
- `static/logo.svg` is a vector recreation based on the supplied logo image. Replace it with the original uploaded asset for exact fidelity.
- Contact submissions are stored in `instance/inquiries.sqlite3`, which is excluded from Git. Override the path with `IRFLOWS_DATABASE`. No email notification or booking provider is connected. The database has no public read endpoint. Set retention and backup policies before accepting real customer inquiries.

## Deployment

Use a production WSGI server rather than Flask's development server (for example, Gunicorn with `app:app`). Configure HTTPS, durable storage for inquiries, and abuse protection before public deployment. Live development processes must be restarted in new environments.
