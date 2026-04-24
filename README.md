# PitchIn — Django REST API Backend

Full backend for the PitchIn entrepreneurial networking platform.

---

## Tech Stack
- **Django 4.2** + **Django REST Framework 3.14**
- **JWT Auth** via `djangorestframework-simplejwt`
- **SQLite** (dev) / **PostgreSQL** (production)
- **Email notifications** via Django's mail backend

---

## Project Structure

```
pitchin/
├── config/              # Project settings & root URLs
├── users/               # Custom auth user model + JWT auth
├── profiles/            # Role-based profile models (5 roles)
├── connections/         # Follow requests + Interest email messages
├── feed/                # Posts, likes, comments
├── news/                # Curated news articles + weekly digests
├── notifications/       # In-app notification system
├── requirements.txt
├── .env.example
└── manage.py
```

---

## Quick Start

```bash
# 1. Clone & enter
git clone <repo> && cd pitchin

# 2. Create virtual environment
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your values

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (for Django Admin)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

Admin panel: http://localhost:8000/admin/

---

## API Reference

### Authentication  `POST /api/auth/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register/` | ❌ | Register new user (returns tokens) |
| POST | `/login/` | ❌ | Login (returns access + refresh token) |
| POST | `/logout/` | ✅ | Blacklist refresh token |
| POST | `/token/refresh/` | ❌ | Refresh access token |
| GET/PATCH | `/me/` | ✅ | Get or update own user info |
| POST | `/change-password/` | ✅ | Change password |

**Register body:**
```json
{
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "role": "startup",
  "password": "strongpass123",
  "password2": "strongpass123"
}
```
Roles: `innovator` | `startup` | `investor` | `consultant` | `ecosystem_partner`

**Login response includes:**
```json
{
  "access": "<jwt>",
  "refresh": "<jwt>",
  "user": { "id": 1, "email": "...", "role": "startup", ... }
}
```

---

### Profiles  `GET|PATCH /api/profiles/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PATCH | `/me/` | Own profile (role-specific fields) |
| GET | `/<user_id>/` | View another user's profile (privacy enforced) |
| GET | `/public/?role=investor` | List public-role profiles |

**Privacy rules:**
- `innovator` & `startup` → **private** — only visible to accepted followers
- `investor`, `consultant`, `ecosystem_partner` → **public** — anyone can view

**Profile fields by role:**

| Role | Key Fields |
|------|-----------|
| Innovator | skills, areas_of_interest, stage, looking_for |
| Startup | company_name, industry, stage, pitch_deck_url, funding_raised |
| Investor | firm_name, investment_thesis, sectors_of_interest, ticket_size_min/max |
| Consultant | expertise, services_offered, years_of_experience, hourly_rate |
| Ecosystem Partner | organization_name, organization_type, programs_offered, equity_taken |

---

### Connections  `POST /api/connections/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/follow/` | Send follow request |
| POST | `/follow/<id>/respond/` | Accept or reject a request |
| DELETE | `/unfollow/<user_id>/` | Unfollow a user |
| GET | `/requests/` | Pending requests you received |
| GET | `/followers/` | Your accepted followers |
| GET | `/following/` | Users you follow |

**Follow request body:**
```json
{ "receiver_id": 5, "message": "Hi, I'd love to connect!" }
```
**Respond body:**
```json
{ "action": "accept" }   // or "reject"
```

> **Note:** Public-role users (investor/consultant/ecosystem_partner) auto-accept follow requests.

---

### Interest Messages (Email)  `POST /api/connections/interest/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/interest/` | Send interest (triggers email to recipient) |
| GET | `/interest/sent/` | Your sent interest messages |
| GET | `/interest/received/` | Interest messages you received |

**Interest body:**
```json
{
  "receiver_id": 3,
  "tag": "investment",
  "subject": "Interested in your startup",
  "message": "I'd like to discuss a potential seed investment..."
}
```
Tags: `investment` | `collaboration` | `mentorship` | `partnership` | `hiring` | `advisory` | `general`

> The message is stored in the DB **and** sent to the recipient's registered email.

---

### Feed  `GET /api/feed/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main feed (followed users + public roles) |
| POST | `/create/` | Create a post |
| GET | `/my/` | Your own posts |
| GET/PATCH/DELETE | `/<id>/` | Post detail / edit / delete |
| POST | `/<id>/like/` | Toggle like |
| GET/POST | `/<id>/comments/` | List or add comments |

**Feed supports filtering:**
- `?post_type=program` — filter by type
- `?author__role=ecosystem_partner` — posts by role
- `?search=fundraising` — full-text search

**Post types:** `update` | `news` | `program` | `fundraise` | `milestone` | `hiring` | `other`

---

### News  `GET /api/news/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | All news (filterable) |
| GET | `/featured/` | Featured articles |
| GET | `/<id>/` | Article detail |
| GET | `/digest/` | Weekly digest list |
| GET | `/digest/<week_label>/` | Single digest (e.g., `2025-W17`) |
| POST | `/admin/create/` | Staff only: create article |
| GET/PATCH/DELETE | `/admin/<id>/` | Staff only: edit/delete |

**Filter options:**
- `?category=fundraising`
- `?is_featured=true`
- `?search=unicorn`

Categories: `startup` | `fundraising` | `ipo` | `venture` | `industry` | `national` | `local` | `policy` | `technology` | `other`

---

### Notifications  `GET /api/notifications/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | All your notifications |
| GET | `/unread-count/` | `{"unread_count": 3}` |
| POST | `/mark-all-read/` | Mark all as read |
| POST | `/<id>/read/` | Mark one as read |

**Notification types:** `follow_request` | `follow_accepted` | `interest_received` | `post_like` | `post_comment` | `new_post`

---

## Authentication Header

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong random `SECRET_KEY`
- [ ] Set `DATABASE_URL` to PostgreSQL
- [ ] Configure SMTP email in `.env`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Set `CORS_ALLOWED_ORIGINS` to your frontend domain
- [ ] Run `python manage.py collectstatic`
- [ ] Serve with Gunicorn + Nginx (or Railway / Render / Fly.io)

---

## Connecting to Your Lovable Frontend

1. Get the `access` token from `/api/auth/login/`
2. Store it in `localStorage` or a cookie
3. Add `Authorization: Bearer <token>` to all API requests
4. Use `/api/auth/token/refresh/` with the `refresh` token to renew access tokens before they expire (60 min)

