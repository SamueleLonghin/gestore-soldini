# Gestore Soldini

Gestore Soldini is a personal expense management application built with Flask and SQLAlchemy ORM.

## Overview

This is a complete solution for managing personal finances, including tracking income (ingressi), expenses (spese), recurring expenses (ricorrenti), and providing an overview of financial status. The application uses SQLite as the database backend and Bootstrap 5 for styling.

## Features

- Income management
- Expense tracking with one-time and recurring options
- Dashboard view with financial summary
- Responsive design using Bootstrap components
- User authentication system
- Multiple expense categories (ricorrenti, ingressi, spese normali)

## Prerequisites

Before running the application:

1. Python 3.7 or higher installed
2. Basic knowledge of Flask and SQLAlchemy ORM
3. SQLite database support on your system

## Installation

    ```bash
    # Clone the repository
    git clone https://github.com/samuelelonghin/gestore_soldini.git

    # Create a virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate    # Windows

    # Install dependencies
    pip install flask sqlalchemy flask-login bootstrap-icons
    ```

## Configuration

1. Copy the config.py file to your instance directory:
```bash
mkdir -p instance/
cp config.template.py instance/config.py
```

2. Edit the configuration file with your database credentials and other settings.

## Running the Application

To run the development server:

```bash
export FLASK_APP=app.py
flask run --debug
```

For production deployment, consider using a WSGI server like Gunicorn:

```bash
gunicorn -w 4 app:app
```

## Database Setup

The application uses SQLite by default. The database file is stored in the instance directory.

To initialize the database:
```bash
flask db init
```

## User Authentication

- Login system using session management
- Logout functionality available in navigation menu
- Protected routes require authentication

## Available Features

### Dashboard
- Financial overview with summary of recent transactions and balances

### Income Management
- View, modify, and add income entries

### Expense Tracking
- One-time expenses (spese)
- Recurring expenses (ricorrenti)

### Expense Categories
The application supports multiple expense categories including:
- Spese Ricorrenti: Recurring expenses
- Ingressi: Income sources
- Gestione Spese: General expenses management

## Directory Structure

```
gestore_soldini/
├── app.py
├── config.py
├── models.py (not shown in attachments, but should be present)
└── templates/
    ├── base.html
    ├── large.html
    ├── macros.html
    └── ... other template files
```

## Deployment

For production deployment:

1. Use a proper WSGI server like Gunicorn or uWSGI
2. Set up environment variables for configuration
3. Consider using a reverse proxy setup with Nginx or Apache

## License

This project is licensed under MIT license.

## Contributing

Contributions are welcome! Please open an issue to report bugs or feature requests.
