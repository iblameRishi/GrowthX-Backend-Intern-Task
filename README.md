# GrowthX Backend Intern Task

This project is developed using FastAPI + MongoDB and designed to manage user and admin-specific operations as according to the requirements.

## Security

The application uses JWT for authentication and authorization. Password is hashed and saved using the bcrypt scheme.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose

### Running the Project

1. **Clone the Repository**

   Clone this repository to your local machine using:

   ```bash
   git clone https://github.com/iblameRishi/GrowthX-Backend-Intern-Task.git
   
   cd GrowthX-Backend-Intern-Task
   ```

2. **Environment Variables**

   Env variables are already in the docker-compose but if they dont work, create a `.env` file in the root directory of the project and add the following environment variables:

   ```plaintext
   SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   You can keep the secret key and hashing algorithm I've used or use your own.
   &nbsp;

3. **Build and Run with Docker Compose**

   Use Docker Compose to build and run the application:

   ```bash
   docker-compose up
   ```

   This command will build the Docker images and start the services defined in the `docker-compose.yml` file.
   &nbsp;

4. **Access the API**

   Once the services are up and running, you can access the API at `http://localhost:8000`.

   You can also view the API documentation at `http://localhost:8000/docs`.

## Project Structure

- **app/main.py**: Main file for the FastAPI application. It initializes the database and includes routers for user and admin endpoints.
&nbsp;

- **app/database/**: Contains database connection logic and Pydantic schemas for data validation.
  - `database.py`: Manages MongoDB connection and initialization.
  - `schemas.py`: Defines data models for users, admins, assignments, and tokens.
&nbsp;

- **app/routers/**: Contains the API routes for users and admins.
  - `users.py`: Handles user registration, login, assignment uploads and get all admins.
  - `admins.py`: Manages admin registration, login, and assignment management (accept/reject).
&nbsp;

- **app/oauth2.py**: Manages JWT token creation and validation for secure access to protected routes.
&nbsp;

- **app/utils.py**: Provides utility functions for password hashing and verification.

## API Endpoints

### User Endpoints

- **POST /user/register**: Register a new user.
   - Send data in this format: `raw` (in postman)
     ```
     {
        "username": "testusername",
        "password": "testpassword"
     }
     ```
- **POST /user/login**: User login to obtain a JWT token.
   - Send data in this format: `form-data` (in postman)
     ```
     {
        "username": "testusername",
        "password": "testpassword"
     }
     ```
- **POST /user/upload**: Upload an assignment (protected route - requires valid JWT).
   - Send data in this format: `raw` (in postman)
     ```
     {
        "task": "test task",
        "admin": "[admin id]",
     }
     ```
- **GET /user/admins**: Fetch all admins (protected route - requires valid JWT).

### Admin Endpoints

- **POST /admin/register**: Register a new admin.
   - Send data in this format: `raw` (in postman)
     ```
     {
        "username": "testusername",
        "password": "testpassword"
     }
     ```
- **POST /admin/login**: Admin login to obtain a JWT token.
   - Send data in this format: `form-data` (in postman)
     ```
     {
        "username": "testusername",
        "password": "testpassword"
     }
     ```
- **GET /admin/assignments**: View assignments tagged to the admin (protected route - requires valid JWT).
- **POST /admin/assignments/{id}/accept**: Accept an assignment (protected route - requires valid JWT).
- **POST /admin/assignments/{id}/reject**: Reject an assignment (protected route - requires valid JWT).

