# IP Tools Suite

## Overview

IP Tools Suite is a Flask-based web application that provides professional network calculation and analysis tools. The application focuses on IP subnet calculations and CIDR block operations, featuring a modern web interface with Bootstrap styling and Font Awesome icons.

## System Architecture

The application follows a simple MVC pattern with Flask as the backend framework:

- **Frontend**: HTML templates with Bootstrap 5 UI framework and custom CSS
- **Backend**: Python Flask web server
- **Deployment**: Gunicorn WSGI server for production deployment
- **Development**: Replit environment with Python 3.11

## Key Components

### Backend Components
- **Flask Application** (`app.py`): Main application entry point with routing and business logic
- **IP Calculation Engine**: Built-in Python `ipaddress` module for network calculations
- **Route Handlers**: RESTful endpoints for subnet calculations and network analysis

### Frontend Components
- **Base Template** (`templates/index.html`): Main HTML structure with tab-based navigation
- **Custom Styling** (`static/css/styles.css`): Professional UI with gradient backgrounds and modern design
- **Interactive UI**: Bootstrap components with Font Awesome icons for enhanced user experience

### Core Features
1. **IP Calculator**: Subnet calculation with CIDR notation support
2. **Network Analysis**: Complementary range calculations for multiple CIDR blocks
3. **Professional UI**: Modern, responsive design with tab-based navigation

## Data Flow

1. **User Input**: CIDR notation entered through web interface
2. **Request Processing**: Flask routes handle HTTP requests
3. **Network Calculation**: Python ipaddress module processes subnet calculations
4. **Response Generation**: JSON responses sent back to frontend
5. **UI Update**: JavaScript updates the interface with calculated results

## External Dependencies

### Core Dependencies
- **Flask 3.1.1**: Web framework for HTTP handling and templating
- **Gunicorn 23.0.0**: Production WSGI server
- **psycopg2-binary 2.9.10**: PostgreSQL database adapter (prepared for future database integration)
- **email-validator 2.2.0**: Email validation utilities
- **flask-sqlalchemy 3.1.1**: ORM for database operations (prepared for future use)

### Frontend Dependencies (CDN)
- **Bootstrap 5.1.3**: UI framework and responsive grid system
- **Font Awesome 6.0.0**: Icon library for enhanced UI
- **Google Fonts (Inter)**: Professional typography

## Deployment Strategy

### Production Deployment
- **Platform**: Replit autoscale deployment
- **Server**: Gunicorn WSGI server
- **Configuration**: Bind to 0.0.0.0:5000 with port reuse and auto-reload
- **Environment**: Python 3.11 with stable Nix packages

### Development Workflow
- **Local Development**: Flask development server with auto-reload
- **Package Management**: UV lock file for dependency management
- **Environment**: Replit with integrated workflow automation

### Infrastructure Requirements
- **Runtime**: Python 3.11
- **System Packages**: OpenSSL, PostgreSQL (prepared for future database integration)
- **Port Configuration**: Application serves on port 5000

## Changelog
- June 24, 2025: Implemented dark/light theme toggle with comprehensive CSS variables and localStorage persistence
- June 24, 2025: Enhanced visual design with modern Bootstrap UI, gradient backgrounds, and professional styling
- June 24, 2025: Updated header with link to gergovadasz.hu blog and simplified subtitle
- June 23, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.