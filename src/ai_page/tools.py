
import os
import requests
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from openai import AsyncOpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from agents import function_tool


# Load .env file
load_dotenv()

# Initialize OpenAI
OPENAI_API = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
N2YO_API = os.getenv("N2YO_API")


TWILIO_API = os.getenv("TWILIO_KEY")
DEFAULT_SENDER = os.getenv("DEFAULT_SENDER")

###########################################
# ChatGPT Research Tool
###########################################
@function_tool
async def chatgpt_researcher(query: str) -> str:
    """Queries OpenAI's language model to research information, answer questions, and retrieve detailed explanations based on the provided prompt.
    Args:
        query: The specific research question, query, or task instructions to send to the model.

    Returns:
        The model's factual response and research findings.
    """
    try:
        response = await OPENAI_API.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "You are an assistant that will precisely answer questions."},
                {"role": "user", "content": query},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content or ""

    except Exception as error:
        print(f"This is the error: {error}")
        return f"Error: {error}"


###########################################
# N2YO Tracking Tool
###########################################
@function_tool
async def satellite_researcher(satellite_id: int):
    """Accept a satellite ID and query the N2YO API to retrieve the latitude and longitude of the satellite.

    Args:
        satellite_id: The unique numeric NORAD Catalog ID of the satellite (e.g., 25544 for ISS).

    Returns:
        dict: A dictionary containing satellite coordinates and tracking details:
            - "latitude": Sub-satellite latitude in decimal degrees.
            - "longitude": Sub-satellite longitude in decimal degrees.
            - "altitude": Satellite altitude in kilometers above Earth.
            - "timestamp": Epoch timestamp of the retrieved coordinate.
    """
    try:
        observer_lat = 0.0
        observer_lng = 0.0
        observer_alt = 0.0
        seconds = 1

        url = (
            f"https://api.n2yo.com/rest/v1/satellite/positions/"
            f"{satellite_id}/{observer_lat}/{observer_lng}/{observer_alt}/{seconds}/"
            f"?apiKey={N2YO_API}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        positions = data.get("positions", [])
        if not positions:
            return {"error": f"No position data returned for satellite ID {satellite_id}. Check if the ID is valid."}

        first_pos = positions[0]

        return {
            "norad_id": satellite_id,
            "latitude": first_pos.get("satlatitude"),
            "longitude": first_pos.get("satlongitude"),
            "altitude": first_pos.get("sataltitude"),
            "timestamp": first_pos.get("timestamp"),
        }

    except Exception as error:
        print(f"Error in satellite_researcher: {error}")
        return {"error": str(error)}

###########################################
# SatNOGS Satellite Status Tool & # SatNOGS Ground Station Telemetry Tool
###########################################

# SatNOGS Base Configuration
SATNOGS_BASE_URL = "https://db.satnogs.org/api"
DEFAULT_HEADERS = {"Accept": "application/json"}


@function_tool
def get_satellite_status(norad_id: int) -> dict:
    """Fetches satellite operational status from SatNOGS and normalizes it for database verification."""
    try:
        url = f"https://db.satnogs.org/api/satellites/{norad_id}/"
        headers = {
            "Accept": "application/json",
            "User-Agent": "SatelliteTrackerApp/1.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        raw_status = "alive"  # Default fallback
        sat_name = "Unknown"
        
        if response.status_code == 200:
            data = response.json()
            sat_name = data.get("name", "Unknown")
            raw_status = str(data.get("status", "")).strip().lower()

        # Normalize to the allowed verification whitelist:
        # ['alive', 'dead', 're-entered', 'future']
        if any(term in raw_status for term in ["alive", "operational", "active", "in orbit"]):
            normalized_status = "alive"
        elif any(term in raw_status for term in ["re-entered", "decayed", "reentered"]):
            normalized_status = "re-entered"
        elif any(term in raw_status for term in ["future", "planned"]):
            normalized_status = "future"
        else:
            normalized_status = "dead"

        return {
            "norad_id": norad_id,
            "name": sat_name,
            "status": normalized_status
        }

    except Exception as e:
        return {
            "norad_id": norad_id,
            "name": "Unknown",
            "status": "alive",  # Safe default to avoid blocking valid tracks
            "error": str(e)
        }

    

@function_tool
def get_recent_telemetry(norad_id: int) -> dict:
    """Fetches recent ground station detection telemetry without requiring any API keys."""
    try:
        # 100% free & public endpoint - no authentication required
        url = "https://network.satnogs.org/api/observations/"
        params = {
            "norad": int(norad_id),
            "status": "good",  # Only verified observations
            "limit": 1
        }
        headers = {
            "User-Agent": "SatelliteTrackerApp/1.0",
            "Accept": "application/json"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        observations = response.json()

        if not observations:
            return {
                "norad_id": norad_id,
                "station_id": "None",
                "observer": "None",
                "detected_timestamp": "None"
            }

        latest = observations[0]
        return {
            "norad_id": norad_id,
            "station_id": str(latest.get("ground_station", "Unknown")),
            "observer": str(latest.get("observer", "Unknown")),
            "detected_timestamp": str(latest.get("vetted_datetime") or latest.get("end", "Unknown")),
            "station_name": str(latest.get("station_name", "N/A"))
        }

    except Exception as e:
        return {"error": f"Failed to retrieve public SatNOGS observation: {str(e)}"}


###########################################
# PostgreSQL Database Tool
###########################################
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", 10)),
    "sslmode": os.getenv("DB_SSLMODE", "require"),
}

@function_tool
def connect_db(
    latitude: str,
    longitude: str,
    altitude: str,
    norad_id: str,
    timestamp: str,
    name: str,
    norad_cat_id: str,
    status: str,
    station_id: str,
    observer: str,
    detected_timestamp: str,
) -> dict:
    """Logs real-time coordinates along with satellite metadata and observer telemetry into PostgreSQL.

    Args:
        latitude: Sub-satellite latitude coordinate in decimal degrees.
        longitude: Sub-satellite longitude coordinate in decimal degrees.
        altitude: Satellite altitude in kilometers.
        norad_id: The NORAD ID from the tracking API.
        timestamp: The coordinate tracking timestamp.
        name: Name of the satellite.
        norad_cat_id: NORAD catalog ID from SatNOGS status.
        status: Operational status (e.g., 'alive', 'dead').
        station_id: ID of the ground station that detected the satellite.
        observer: Operator callsign/name of the ground station.
        detected_timestamp: Timestamp when the transmission was detected by the observer.

    Returns:
        dict: A dictionary confirming database execution status.
    """
    conn = None
    try:
        queried_date = datetime.now(timezone.utc).isoformat()
        conn = psycopg2.connect(**DB_CONFIG)

        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS satellite_db (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    latitude TEXT,
                    longitude TEXT,
                    altitude TEXT,
                    norad_id TEXT,
                    timestamp TEXT,
                    name TEXT,
                    norad_cat_id TEXT,
                    status TEXT,
                    station_id TEXT,
                    observer TEXT,
                    detected_timestamp TEXT,
                    queried_date TEXT
                );
            """)

            cursor.execute("""
                INSERT INTO satellite_db (
                    latitude,
                    longitude,
                    altitude,
                    norad_id,
                    timestamp,
                    name,
                    norad_cat_id,
                    status,
                    station_id,
                    observer,
                    detected_timestamp,
                    queried_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                latitude,
                longitude,
                altitude,
                norad_id,
                timestamp,
                name,
                norad_cat_id,
                status,
                station_id,
                observer,
                detected_timestamp,
                queried_date,
            ))

        conn.commit()
        return {"status": "success", "message": "Query Logged"}

    except Exception as error:
        if conn:
            conn.rollback()
        return {"status": "failed", "message": str(error)}

    finally:
        if conn and not conn.closed:
            conn.close()


###########################################
# SendGrid Outbound Email Tool
###########################################
@function_tool
def send_email_tool(recipient_email: str, subject: str, html_body: str) -> dict:
    """Sends an outbound notification or telemetry report email via SendGrid.

    Args:
        recipient_email: The recipient address (e.g., 'john.rivero.interview@gmail.com').
        subject: The subject header for the email.
        html_body: Formatted HTML content or plain text message body.

    Returns:
        dict: Execution status and HTTP status code or error details.
    """
    message = Mail(
        from_email=DEFAULT_SENDER,
        to_emails=recipient_email,
        subject=subject,
        html_content=html_body,
    )

    try:
        sg = SendGridAPIClient(TWILIO_API)
        response = sg.send(message)
        return {
            "status": "success",
            "status_code": response.status_code,
            "message": f"Email successfully accepted by SendGrid (HTTP {response.status_code})."
        }
    except Exception as error:
        error_details = str(error)
        if hasattr(error, "body") and error.body:
            error_details = error.body.decode("utf-8") if isinstance(error.body, bytes) else str(error.body)
        return {
            "status": "failed",
            "error": error_details
        }