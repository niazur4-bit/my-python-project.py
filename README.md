# Munib and Co — Chartered Certified Accountant

A full-stack, responsive website for a Chartered Accountant firm, built with **Django 5**, **PostgreSQL**, **Bootstrap 5**, and vanilla JavaScript. Includes a client portal, online appointment booking, a blog, a downloadable tax-forms library, and a staff dashboard on top of the full Django admin.

## Features

- Professional homepage with hero banner, services, testimonials and blog preview
- About Us page with firm story, stats and team
- Services page (list + detail) covering all 8 core services
- Contact page with a working contact form (email notification) and an embedded Google Map
- Online appointment booking with automatic confirmation emails
- Client registration and login (custom user model)
- Client dashboard (view/track own appointments) and profile editing
- Staff dashboard with live statistics, plus the full Django admin for CRUD management
- Blog / News section with categories and pagination
- Testimonials carousel-style grid
- FAQ page (accordion)
- Download tax forms & documents, filterable by category
- Site-wide search across services and blog articles
- Mobile responsive design (Bootstrap 5)
- SEO: per-page meta tags, canonical URLs, Open Graph tags, `sitemap.xml`, `robots.txt`

## Tech Stack

- **Backend:** Python, Django 5
- **Database:** PostgreSQL (SQLite fallback for local development)
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript, Bootstrap Icons
- **Auth:** Django's built-in authentication with a custom `User` model
- **Email:** Django's SMTP email backend (console backend in development)
- **File uploads:** Django's media file handling (`Pillow` for images)

## Project Structure

```
ca_project/
├── accounts/          # Custom user model, registration, login, client dashboard, profile
├── core/               # Homepage, About, FAQ, Documents, Search, site-wide models
│                        #   (Testimonial, FAQ, Document, TeamMember), seed_demo_data command
├── services/           # Service catalogue (list + detail)
├── appointments/       # Appointment booking + client's "My Appointments"
├── blog/                # Blog / News
├── contact/             # Contact form + ContactMessage model
├── dashboard/           # Staff-only statistics dashboard
├── templates/           # All HTML templates (base.html + one folder per app)
├── static/              # css/style.css, js/main.js, img/
├── media/                # User-uploaded files (created at runtime)
├── requirements.txt
├── schema.sql            # PostgreSQL schema reference
├── .env.example
└── manage.py
```

## Design

The visual identity is built around the idea of an accounting ledger: thin ruled lines, a deep navy/ledger-green palette with a brass accent, monospace figures for numbers, and a wax-seal "certification" badge as the site's signature mark. Fonts: **Fraunces** (display), **Inter** (body), **IBM Plex Mono** (figures/data), loaded from Google Fonts.

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 14+ (optional for local dev — SQLite works out of the box)
- pip / virtualenv

### 2. Clone & create a virtual environment
```bash
cd ca_project
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and set at minimum `SECRET_KEY`. Leave `USE_POSTGRES=False` to use SQLite for a quick start, or see the PostgreSQL section below.

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create an admin (superuser) account
```bash
python manage.py createsuperuser
```

### 7. (Optional) Seed demo content
Populates services, FAQs, testimonials, team members and a sample blog post so the site isn't empty:
```bash
python manage.py seed_demo_data
```

### 8. Run the development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the Django admin. Logged-in staff users are also redirected to a custom stats dashboard at `/dashboard/` (linked from the navbar avatar menu once logged in).

## Using PostgreSQL

1. Create a database and user:
   ```sql
   CREATE DATABASE ca_firm_db;
   CREATE USER ca_firm_user WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE ca_firm_db TO ca_firm_user;
   ```
2. In `.env`, set:
   ```
   USE_POSTGRES=True
   DB_NAME=ca_firm_db
   DB_USER=ca_firm_user
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```
3. Run `python manage.py migrate` again — Django will create every table listed in `schema.sql` automatically.

## Email (SMTP) configuration

By default, `DEBUG=True` prints emails to the console instead of sending them, so you can test the contact form and appointment booking without an SMTP account. To send real emails:

1. In `.env`, set `FORCE_SMTP=True` (or set `DEBUG=False` for production).
2. Fill in `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`. For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your normal password.
3. Set `FIRM_NOTIFICATION_EMAIL` to the inbox that should receive contact/appointment notifications.

## Google Maps

The contact page embeds a Google Map via an iframe. To point it at your own office:
1. Open Google Maps → search your address → **Share** → **Embed a map**.
2. Copy the `src="..."` URL from the generated `<iframe>` code.
3. Paste it into `GOOGLE_MAPS_EMBED_SRC` in your `.env`.

## Admin / staff features

Everything under "Manage services / appointments / clients / blog posts / testimonials / contact messages" is handled by the customized Django admin at `/admin/` (list filters, search, inline editing of status/order fields are already configured per model). The custom dashboard at `/dashboard/` (staff-only) shows headline statistics — client count, appointment pipeline, unread messages, published content — with quick links into the relevant admin pages.

## Sample login (after seeding)

Create your own superuser with `createsuperuser` as shown above — no default credentials are shipped with this project for security reasons.

## Notes for deployment

- Set `DEBUG=False`, a strong random `SECRET_KEY`, and a real `ALLOWED_HOSTS` list in production.
- Run `python manage.py collectstatic` before deploying — static files are served via **WhiteNoise** in production.
- `gunicorn` is included in `requirements.txt` as a production WSGI server (`gunicorn ca_project.wsgi`).
- Use PostgreSQL, not SQLite, in production.
