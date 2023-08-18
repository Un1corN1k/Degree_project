# MyCinema

MyCinema is a web application for managing movie sessions and cinema halls.

## Features

- View a list of available cinema halls.
- View detailed information about a specific cinema hall.
- Create, update, and delete movie sessions.
- Reserve tickets for movie sessions.
- User authentication and authorization.
- Responsive design for optimal viewing on various devices.

## Installation

1. Clone the repository:

git clone https://github.com/Un1corN1k/Degree_project.git

2. Navigate to the project directory:

cd cinema

3. Create a virtual environment:

python -m venv venv

4. Activate the virtual environment:

On Windows:

venv\Scripts\activate

On macOS and Linux:

source venv/bin/activate

5. Install the required dependencies:

pip install -r requirements.txt

6. Run the development server:

python manage.py runserver


7. Access the application in your web browser at `http://127.0.0.1:8000`.

## Usage

- Visit the homepage to see a list of available movies.
- Click on tickets if you want to book a ticket for a movie screening.
- If you're a superuser, you can log in and access the admin panel at `/admin` to manage movie sessions and cinema halls.
