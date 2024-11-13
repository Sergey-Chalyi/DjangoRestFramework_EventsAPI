# Event Management API

---

## Project Description

This project is a Django-based REST API for managing events. It allows users to create, view, update, and delete events, as well as register for events.

### Key Features

- CRUD (Create, Read, Update, Delete) operations for the Event model
- Basic User Registration and Authentication
- Event Registration
- API documentation
- Docker support

## Prerequisites

Before running the project, ensure you have:

- Python 3.x
- Docker (optional)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Sergey-Chalyi/DjangoRestFramework_EventsAPI.git
   cd DjangoRestFramework_EventsAPI
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   Create a `.env` file in the project root with the following content:

   ```
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_oauth2_key
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_oauth2_secret
   TEST_IP_ADDRESS=your_test_ip_address
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

## Running the Project

### Using Django Development Server

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

2. Access the API at `http://localhost:8000/api/v1/events/`.

### Using Docker

1. Build the Docker image:

   ```bash
   docker build -t event-management-api .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8000:8000 -d --env-file .env event-management-api
   ```

3. Access the API at `http://localhost:8000/api/v1/events/`.

## API Documentation

### Authentication

All API endpoints require authentication. The project supports:
- Google OAuth2
- Session authentication for web interface

### Endpoints

#### Events API

| Method | Endpoint                | Description                     | Authentication Required |
|--------|--------------------------|---------------------------------|-------------------------|
| GET    | `/api/v1/events/`        | List all events                | Yes                     |
| POST   | `/api/v1/events/`        | Create a new event             | Yes                     |
| GET    | `/api/v1/events/{id}/`   | Get event details              | Yes                     |
| PUT    | `/api/v1/events/{id}/`   | Update an event                | Yes (Only event creator)|
| DELETE | `/api/v1/events/{id}/`   | Delete an event                | Yes (Only event creator)|


### List/Search/Filter Events

#### GET `/api/v1/events/`

Supports sorting, searching, and filtering events based on specific parameters:

| Parameter       | Type    | Description                                                                                |
|-----------------|---------|--------------------------------------------------------------------------------------------|
| `ordering`      | string  | Sort events by `date`, `time_created`, or `-date` and `-time_created` for descending order |
| `search`        | string  | Search events by title or location (case-insensitive)                                      |
| `date`          | date    | Filter events by assigned date                                                             |
| `time_created`  | date    | Filter events by creation date                                                             |
| `organizer_id`  | integer | Filter events by the user who created the event                                            |
| `invited_user_id` | integer | Filter events by invited user ID                                                           |


### Authentication Endpoints

| Endpoint                                   | Description                |
|--------------------------------------------|----------------------------|
| `/login/`                                  | Login page                 |
| `/logout/`                                 | Logout endpoint            |


## Development

For development and testing, please refer to the project requirements and setup instructions.

## Security Considerations

- The project uses environment variables for sensitive data.
- OAuth2 authentication is required for all API endpoints.

## Contact

For questions and support, please contact:

- Email: ch.sergey.rb@gmail.com
