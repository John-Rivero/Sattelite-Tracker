# Satellite Tracker

Satellite Tracker is an orbital intelligence and satellite tracking desktop application built with PyQt6, OpenAI Agents SDK, and PostgreSQL. The system uses a centralized Supervisor and Verification architecture that coordinates live orbital tracking, SatNOGS ground station health analysis, persistent telemetry logging to an Amazon RDS PostgreSQL database, and automated email reporting.

---

## Architecture Overview

![Architecture](<images/screenshots/architecture.png>)

The application coordinates multiple specialized agents under a strict verification pipeline:
1. **Supervisor Agent:** Orchestrates user intent, assigns tasks to sub-agents, and performs a secondary sanity check on research queries.
2. **ChatGPT Researcher Agent:** Queries orbital databases and general space history to resolve numeric NORAD IDs and mission facts.
3. **N2YO Tracking Agent:** Fetches real-time sub-satellite coordinates (latitude, longitude, altitude) and observation timestamps.
4. **Satellite Status Agent:** Queries SatNOGS DB for spacecraft operational status (alive, dead, re-entered) and ground receiver detection data.
5. **Verification Agent:** Serves as a mandatory gatekeeper, auditing all payloads before database logging, email dispatch, or UI display.
6. **PostgreSQL DB Agent:** Persists verified 11-field telemetry records to PostgreSQL.
7. **Email Dispatch Agent:** Formats observation passes into styled HTML reports and dispatches them via SendGrid/Twilio.

---

## Core Application Interfaces

The desktop application integrates three main UI components:

1. **AI Chatbot Interface:** A PyQt6 QWebEngine-powered mission console running the multi-agent pipeline for natural language tracking, research queries, and manual task triggers.
2. **Database Connection UI:** A live PostgreSQL management interface (`self.tableView`) displaying persisted telemetry records including sub-satellite coordinates, NORAD IDs, operational health flags, receiving station IDs, observer handles, and detection timestamps.
3. **Gmail / Email Dispatch Interface:** An outbound notification UI integrated with SendGrid/Twilio for generating and dispatching structured HTML telemetry reports.

---

## Screenshots

### Application Main Window
![Application Main UI](<images/screenshots/Screenshot 2026-10-30 131802.png>)

### Live Query & Verified Output Results
![Query Result1](<images/screenshots/database.png>)
![Query Result1](<images/screenshots/email.jpg>)

---

## Complete Step-by-Step Instructions

Follow these numbered steps in sequence to set up, configure, and operate the entire system:

### Steps:

1. **Download or export the project archive to your local workstation.**
   Extract the archive files and open your terminal in the root directory of the project.

2. **Install all required packages.**
   Ensure your Python environment is active and install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtain necessary API keys:**
   - **N2YO API Key:** Retrieve from your [N2YO account](https://www.n2yo.com/api/).
   - **OpenAI API Key:** Retrieve from the [OpenAI Platform](https://platform.openai.com/api-keys).
   - **Twilio / SendGrid Key:** Retrieve from your [Twilio SendGrid console](https://app.sendgrid.com/).

4. **Obtain PostgreSQL credentials:**
   Gather your database name, user, password, host endpoint, and port from your database administrator or cloud provider (e.g., AWS RDS).

5. **Create a `.env` file and make sure to include these variables:**
   Create a file named `.env` in the root directory and paste the following template, filling in your actual values:

```env
# APIs
N2YO_API=your_n2yo_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
TWILIO_KEY=your_twilio_sendgrid_key_here

# Email Sender Address
DEFAULT_SENDER=your_verified_sender@example.com

# Database Credentials
DB_NAME=sattelite_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=database-1.your-rds-endpoint.amazonaws.com
DB_PORT=5432
DB_CONNECT_TIMEOUT=10
DB_SSLMODE=require
```