import psycopg2, os
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QMessageBox
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def btn_connect_db_button_clicked(self, ui):
    """Queries sattelite_db from PostgreSQL and populates self.tableView."""
    db_config = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", 5432)),
        "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", 10)),
        "sslmode": os.getenv("DB_SSLMODE", "require"),
    }
    
    conn = None
    try:
        #Postgres Connection
        conn = psycopg2.connect(**db_config)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, latitude, longitude, altitude, norad_id, timestamp, name, norad_cat_id, status, station_id, observer, detected_timestamp, queried_date
                FROM satellite_db
                ORDER BY id DESC;
            """)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

        #QT Table Model Buildout
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([col.replace("_", " ").title() for col in columns])


        for row in rows:
            row_items = []
            for item in row:
                cell = QStandardItem(str(item) if item is not None else "")
                cell.setEditable(False)  # Make table cells read-only
                row_items.append(cell)
            model.appendRow(row_items)

        #Attach the model to the tableview
        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()

    except Exception as error:
        QMessageBox.critical(
            self,
            "Database Error",
            f"Failed to query database:\n{str(error)}"
        )
    finally:
        if conn and not conn.closed:
            conn.close()