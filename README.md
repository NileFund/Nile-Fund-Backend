# Nile Fund Backend

> **Made by ITI Students** 🎓

A Django REST Framework-based backend API for a crowdfunding/donation platform. Users can create fundraising projects, donate to projects, leave comments, and rate projects.

## Features

- 👥 **User Management**: Registration, authentication, profile management, and password reset
- 💰 **Project Management**: Create, update, and manage fundraising projects with various statuses
- 🎯 **Categories**: Organize projects by categories
- 💳 **Donations**: Process donations and track donor contributions
- 💬 **Comments**: Users can comment on projects
- ⭐ **Ratings**: Rate and review projects
- 📊 **Reports**: Report inappropriate projects or comments
- 🔐 **Security**: JWT-based authentication with token refresh and blacklist support
- 📁 **Media Storage**: Cloud-based media storage using Cloudinary
- 🌍 **CORS**: Cross-Origin Resource Sharing enabled for frontend integration

## Tech Stack

- **Backend Framework**: Django 5.2.13
- **REST API**: Django REST Framework 3.17.1
- **Authentication**: Django REST Framework SimpleJWT 5.5.1
- **Database**: PostgreSQL (with psycopg2)
- **File Storage**: Cloudinary
- **Server**: ASGI with async support
- **Validation**: Django Filter, custom validators

## Project Structure

```
Nile-Fund-Backend/
├── apps/
│   ├── accounts/          # User authentication and profile management
│   ├── categories/        # Project categories
│   ├── comments/          # Project comments
│   ├── donations/         # Donation handling and tracking
│   ├── projects/          # Project creation and management
│   ├── ratings/           # Project ratings and reviews
│   ├── reports/           # Report inappropriate content
│   └── common/            # Shared models, exceptions, permissions, pagination
├── config/                # Project configuration
│   ├── settings/          # Django settings (base, dev, prod)
│   ├── urls.py            # URL routing configuration
│   ├── asgi.py            # ASGI configuration
│   └── wsgi.py            # WSGI configuration
├── media/                 # Media files storage
├── bruno/                 # API request collection (Bruno)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Nile-Fund-Backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment configuration**
   Create a `.env` file in the project root with the following variables:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/nile_fund

   # Django
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=127.0.0.1,localhost

   # JWT
   JWT_SECRET_KEY=your-jwt-secret-key

   # Cloudinary (for media storage)
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret

   # Email (for password reset)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password

   # CORS
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Project

### Development Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`

### Admin Panel
Navigate to `http://127.0.0.1:8000/admin/` and log in with superuser credentials.

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `POST /api/accounts/token/refresh/` - Refresh JWT token
- `POST /api/password_reset/` - Request password reset
- `POST /api/password_reset/confirm/` - Confirm password reset

### User Profile
- `GET /api/accounts/profile/` - Get current user profile
- `PUT /api/accounts/profile/` - Update user profile
- `DELETE /api/accounts/delete/` - Delete user account

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

### Categories
- `GET /api/categories/` - List all categories

### Donations
- `GET /api/donations/` - List user's donations
- `POST /api/donations/` - Create a donation
- `GET /api/donations/my-donations/` - Get current user's donations

### Comments
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create a comment
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

### Ratings
- `POST /api/ratings/` - Create/update a rating
- `PUT /api/ratings/{id}/` - Update rating

### Reports
- `POST /api/reports/` - Report inappropriate content

## Database Models

### User
- Email-based authentication
- Profile picture, birthdate, phone number validation
- Phone number validation (Egyptian format)
- Email verification support

### Project
- Belongs to a user (creator)
- Has a category and tags
- Status tracking (pending, running, completed, cancelled)
- Time-based validation (start and end dates)
- Target fundraising amount
- Related projects, donations, comments, and ratings

### Donation
- Links users to projects
- Tracks donation amount and timestamp
- Supports filtering by project and donor

### Comment
- Allows users to comment on projects
- Hierarchical support (optional parent comment for nested comments)

### Rating
- Allows users to rate projects (1-5 stars)
- Tracks reviewer feedback

## Authentication

The API uses JWT (JSON Web Token) authentication:

1. **Login**: Send credentials to `/api/accounts/login/` to receive access and refresh tokens
2. **Access Token**: Include in Authorization header: `Authorization: Bearer <access-token>`
3. **Refresh Token**: When access token expires, use refresh token at `/api/accounts/token/refresh/`

## Testing

API requests are documented in the `bruno/` folder using Bruno API client format. Import the collection into Bruno to test all endpoints.

## Configuration

### Development vs Production
- **Development**: Configure in `config/settings/dev.py`
- **Production**: Configure in `config/settings/prod.py`

Switch environments by setting `DJANGO_SETTINGS_MODULE`:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod  # For production
python manage.py runserver
```

## Contributors

This project is developed by the ITI team:

- **Team Members**: [Alaa Abdallah , Menna Mohamed, kariem Ibrahim , Hashiem Abdelaziz, John Fayz , ]
- **Organization**: Information Technology Institute (ITI)

## Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License

This project is proprietary and confidential.

## Support

For issues or questions, please contact the development team.

---

**Last Updated**: April 2026
