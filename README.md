# JobMate Angular & FastAPI Project

## Overview
This project consists of a frontend built with Angular and a backend built with FastAPI. The application is designed to track resume match making with job description using ATS.

## Features

- User authentication with JWT
- Upload and manage resumes (PDF, DOCX, TXT)
- Track job applications and their status
- Match resumes with job descriptions using NLP
- Calculate and store match scores

## Project Structure
```
/project-root
  |-- frontend/        # Angular application
  |-- backend/         # FastAPI application
```

## Prerequisites
Before running this project, ensure you have the following installed:
- Node.js (>= 14.x)
- Angular CLI (>= 15.x)
- Python (>= 3.8)
- FastAPI
- npm or yarn

## Installation
Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd <project-folder>
```

### Setting Up the Frontend
```bash
cd frontend
npm install  # or yarn install
```

### Setting Up the Backend
```bash
cd backend
pip install -r requirements.txt
```

## Running the Application
### Start the Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload or python main.py
```
The backend will run at `http://127.0.0.1:8000/`.

### Start the Frontend (Angular)
```bash
cd frontend
ng serve
```
Then open your browser and navigate to `http://localhost:4200/`.

## Building the Project
### Build the Frontend
```bash
cd frontend
ng build --prod
```
The build files will be available in the `dist/` directory.

### Build the Backend
No build is required; just run the FastAPI server.

## Running Tests
### Frontend Tests
Run unit tests with:
```bash
cd frontend
ng test
```
Run end-to-end tests with:
```bash
ng e2e
```

### Backend Tests
Run FastAPI tests using pytest:
```bash
cd backend
pytest
```

## Linting
### Frontend Linting
To check for linting errors:
```bash
cd frontend
ng lint
```

### Backend Linting
To check for linting errors in Python:
```bash
cd backend
flake8 .
```

## Deployment
Deployment is done using Dockerfile and Kubernet

## Folder Structure
```
/project-root
  |-- frontend/               # Angular application
  |-- backend/                # FastAPI application
  |-- frontend/src/           # Angular source files
  |-- backend/app/            # FastAPI app files
  |-- assets/                 # Static assets (images, styles, etc.)
  |-- environments/           # Environment configuration files
  |-- main.ts                 # Main entry point for Angular
  |-- index.html              # Main HTML file
```