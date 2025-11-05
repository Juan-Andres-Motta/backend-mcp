import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastmcp import FastMCP
from datetime import datetime
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MCP Server configuration
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "stdio").lower()
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

mcp = FastMCP("Appointment Scheduler 🚀")

# Database connection configuration from environment variables
DB_CONNECTION_STRING = os.getenv(
    "DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname"
)

# SQLAlchemy setup
engine = create_engine(DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Define the appointments table
appointments_table = Table(
    "appointments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("identification_number", String(50), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("date", DateTime, nullable=False),
)


def run_migrations():
    """Run database migrations using Alembic."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


# Initialize database on startup by running migrations
run_migrations()


@mcp.tool
def schedule_appointment(
    name: str, identification_number: str, phone: str, date: str
) -> str:
    """
    Schedule a new appointment by inserting a record into the database.

    Args:
        name: Full name of the person scheduling the appointment
        identification_number: Identification number (e.g., ID card, passport)
        phone: Phone number
        date: Appointment date and time in ISO format (YYYY-MM-DDTHH:MM:SS)

    Returns:
        Success message with appointment details or error message
    """
    try:
        # Validate required fields
        if not all([name, identification_number, phone, date]):
            return "Error: All fields (name, identification_number, phone, date) are required."

        # Parse and validate date
        try:
            appointment_date = datetime.fromisoformat(date.replace("Z", "+00:00"))
        except ValueError:
            return "Error: Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)."

        # Insert record into database using SQLAlchemy
        db = SessionLocal()
        try:
            insert_stmt = (
                appointments_table.insert()
                .values(
                    name=name,
                    identification_number=identification_number,
                    phone=phone,
                    date=appointment_date,
                )
                .returning(appointments_table.c.id)
            )

            result = db.execute(insert_stmt)
            appointment_id = result.fetchone()[0]
            db.commit()

            return f"Success: Appointment scheduled for {name} on {appointment_date.strftime('%Y-%m-%d %H:%M:%S')} (ID: {appointment_id})"

        finally:
            db.close()

    except SQLAlchemyError as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    if MCP_TRANSPORT == "http":
        print(f"Starting MCP server in HTTP mode on {MCP_HOST}:{MCP_PORT}")
        mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT)
    else:
        print("Starting MCP server in stdio mode")
        mcp.run(transport="stdio")
