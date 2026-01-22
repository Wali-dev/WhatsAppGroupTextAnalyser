# WhatsApp Text Analyzer

## About the Project

Most developers would typically choose React for a project like this, but I deliberately selected Angular for the frontend to explore a different architectural approach and demonstrate versatility, even though I am proficient in React, Next.js, and React Native.

This project is a WhatsApp group text analyzer platform that allows users to upload exported .txt chat files and generate various insights from the data. The backend is built using FastAPI with MongoDB, providing a high-performance and scalable API layer. For data visualization, Chart.js integrated via ng2-charts is used to render interactive and responsive charts. All dependencies, setup instructions, and execution steps required to run the project are clearly documented in the internal README files.

## Project Structure

```
whatsApp_Text_Analyzer/
├── backend/           # FastAPI backend with MongoDB
├── frontend-angular/  # Angular frontend with Chart.js integration
└── readme.md          # This file
```

## Technologies Used

### Backend
- **Python**: Programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for storing chat analysis data
- **Motor**: Async Python driver for MongoDB
- **PyJWT**: JSON Web Token implementation for authentication
- **Uvicorn**: ASGI server for running FastAPI applications

### Frontend
- **Angular**: Frontend framework
- **Chart.js**: Interactive charting library
- **ng2-charts**: Angular wrapper for Chart.js
- **TypeScript**: Typed superset of JavaScript

## Features

- Upload exported WhatsApp .txt chat files
- Parse and analyze chat data
- Generate insights about conversation patterns
- Visualize data with interactive charts
- User authentication and session management
- Responsive design for cross-device compatibility

## Setup Instructions

Detailed setup instructions for both backend and frontend can be found in their respective README files:

- [Backend README](./backend/README.md)
- [Frontend README](./frontend-angular/README.md)

## How to Run

1. Set up the backend server (see backend README)
2. Set up the frontend application (see frontend README)
3. Start both servers
4. Access the application through your browser

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.