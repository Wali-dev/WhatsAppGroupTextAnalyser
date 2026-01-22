# WhatsApp Text Analyzer Backend

A Python FastAPI backend for analyzing WhatsApp chat exports. This service parses WhatsApp text files and provides insights about conversations, including activity patterns and user engagement metrics.

## Prerequisites

- Python 3.8+
- pip package manager
- MongoDB database (local or cloud instance)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd whatsapp-text-analyzer/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
DATABASE_NAME=whatsapp_text_analyzer
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/database_name
```

> **Note**: Change the JWT secret key in production environments.

### 5. Run the Application

#### Option 1: Using Uvicorn with Config File
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

#### Option 2: Using Uvicorn Directly
```bash
uvicorn main:app --reload
```

#### Option 3: Using Python Module
```bash
python -m uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`.

## Project Structure

```
backend/
├── main.py                 # Main FastAPI application entry point
├── uvicorn.conf.py         # Uvicorn server configuration
├── .env                    # Environment variables (not committed)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── configs/                # Configuration files
│   └── database_config.py  # MongoDB configuration
├── controllers/            # Request handlers
├── middleware/             # Authentication and other middleware
├── models/                 # Data models
├── routes/                 # API route definitions
├── schemas/                # Pydantic schemas
├── utils/                  # Utility functions
├── validation/             # Input validation
└── README.md               # This file
```

## API Documentation

**Base URL**: `/api/v1`

### General Routes

#### 1. Health Check
- **Endpoint**: `GET /health`
- **Description**: Verify that the API is running.
- **Authentication**: None required
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

#### 2. Parse WhatsApp File
- **Endpoint**: `POST /parse-txt`
- **Description**: Parse an uploaded WhatsApp exported `.txt` file and save the analysis to the database.
- **Authentication**: Required (via Bearer Token in Authorization header)
- **Request Body** (`multipart/form-data`):
  - `file`: The `.txt` file to be analyzed.
- **Response**:
  ```json
  {
    "range": {
      "start": "2023-01-01",
      "end": "2023-01-07"
    },
    "day_wise_graph_data": [
      {
        "date": "2023-01-01",
        "new_users": 5,
        "active_users": 12
      }
    ],
    "active_4_days_users": ["Alice", "Bob"],
    "inserted_id": "60d5ec49f1a2c3a4b5c6d7e8"
  }
  ```

### User Routes
**Prefix**: `/user` (Full path: `/api/v1/user/...`)

#### 1. Login
- **Endpoint**: `POST /user/login`
- **Description**: Authenticate user and receive an access token.
- **Authentication**: None required
- **Request Body** (`application/json`):
  ```json
  {
    "userid": "user123",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJ0eXAi...",
    "token_type": "bearer"
  }
  ```

#### 2. Logout
- **Endpoint**: `POST /user/logout`
- **Description**: Log out the current user.
- **Authentication**: Required (via Bearer Token in Authorization header)
- **Request Body**: None
- **Response**:
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

#### 3. Get User Data
- **Endpoint**: `GET /user/data`
- **Description**: Retrieve all analysis history for the authenticated user.
- **Authentication**: Required (via Bearer Token in Authorization header)
- **Request Body**: None
- **Response**:
  ```json
  {
    "user_id": "user123",
    "analyses": [
      {
        "id": "60d5ec49f1a2c3a4b5c6d7e8",
        "filename": "WhatsApp Chat.txt",
        "upload_date": "2023-01-20T10:00:00.000Z",
        "range_start": "2023-01-01",
        "range_end": "2023-01-07",
        "day_wise_graph_data": [...],
        "active_4_days_users": [...],
        "user_id": "user123"
      }
    ]
  }
  ```

## Development

### Running with Auto-reload
For development, use the `--reload` flag to automatically restart the server when code changes:

```bash
uvicorn main:app --reload
```

### API Documentation
FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Database Connection
The application connects to MongoDB using Motor (async driver) and PyMongo (sync driver). Connection details are loaded from environment variables.

## Dependencies

This project uses the following key dependencies:
- [FastAPI](https://fastapi.tiangolo.com/): Modern, fast web framework for building APIs with Python
- [Uvicorn](https://www.uvicorn.org/): ASGI server for running FastAPI applications
- [Motor](https://motor.readthedocs.io/): Async Python driver for MongoDB
- [PyMongo](https://pymongo.readthedocs.io/): Python driver for MongoDB
- [PyJWT](https://pyjwt.readthedocs.io/): JSON Web Token implementation for authentication
- [python-multipart](https://andrew-d.github.io/python-multipart/): Multipart data parsing
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management

## Deployment

For production deployment:
1. Use a production-ready server like Gunicorn with Uvicorn workers
2. Configure proper environment variables
3. Set up SSL certificates
4. Use a reverse proxy like Nginx
5. Implement proper logging and monitoring

Example production command:
```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request