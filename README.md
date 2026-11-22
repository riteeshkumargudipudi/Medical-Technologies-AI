Modular Python Backend Services and Automation Suite

A production-style modular Python backend application featuring a Flask REST API notification engine, prioritized message queuing, vehicle fleet maintenance scheduling, and centralized logging middleware.

ARCHITECTURAL OVERVIEW

This repository contains a suite of modular Python backend services designed for asynchronous operations, resource scheduling, and resilient API management:

notification_app_be/ - Core Flask REST API backend with SQLite persistence app.py - API routes and business logic test_app.py - Unit tests for notification endpoints priority_inbox/ - Message priority sorting and classification queue vehicle_scheduling/ - Automated vehicle maintenance scheduling algorithms logging_middleware/ - Centralized structured logging with rotation and sanitization logger.py - Reusable logging utility test_logger.py - Unit tests for logging formats verify_live.py - Live in-process endpoint verification test suite notification_system_design.md - System architecture and API schema documentation

KEY MICRO-MODULES

Campus Notification REST API (notification_app_be)
Lightweight, production-grade Flask web service backed by SQLite.
Implements student identity validation via custom header authentication (X-Student-ID).
Supports creating, querying, filtering, and marking read/unread notifications.
Priority Inbox Engine (priority_inbox)
Intelligent queuing and sorting mechanism that ranks incoming messages based on urgency, category, and sender weight.
Segregates critical alerts from broadcast notifications.
Vehicle Maintenance Scheduler (vehicle_scheduling)
Algorithmic scheduler that allocates fleet maintenance slots based on mileage, time intervals, and workshop capacity.
Eliminates operational bottlenecks through dynamic conflict resolution.
Centralized Logging Middleware (logging_middleware)
Standardized logging module generating structured logs in ./logs/ directory.
Independent log separation for the web server (app.log), queue (priority_inbox.log), and scheduler (vehicle_scheduler.log).

AUTOMATED TESTING

The repository contains built-in test suites covering unit logic and live endpoint behavior:

verify_live.py: Spins up an in-process test client using an isolated temporary SQLite database and exercises every API route against edge cases.
Pytest Suites: Structured unit testing across the API and logging middleware.

INSTALLATION AND USAGE

Clone the repository git clone https://github.com/riteeshkumargudipudi/Medical-Technologies-AI.git cd Medical-Technologies-AI

Set up virtual environment python -m venv venv venv\Scripts\activate pip install -r requirements.txt pip install flask pytest requests

Run Live In-Process Endpoint Verification python verify_live.py

Run Pytest Suite pytest

Start the Notification API Server python notification_app_be/app.py

AUTHOR

Gudipudi Riteesh Kumar


GitHub: https://github.com/riteeshkumargudipudi


LinkedIn: https://linkedin.com/in/riteesh-kumar-gudipudi-76a330290/
