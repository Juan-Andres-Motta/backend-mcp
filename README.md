# Appointment Scheduler MCP Server

A Model Context Protocol (MCP) server that connects to a PostgreSQL database to manage appointment scheduling. Built with FastMCP, SQLAlchemy, and Alembic for database migrations.

## 🚀 Features

- **Database Integration**: PostgreSQL database with SQLAlchemy ORM
- **MCP Protocol**: Supports both stdio and HTTP transport modes
- **Database Migrations**: Alembic for schema management and migrations
- **Appointment Management**: Schedule appointments with validation
- **Docker Support**: Containerized deployment with Docker Compose
- **Environment Configuration**: Secure credential management with .env files

## 📋 Prerequisites

- Python 3.13+
- PostgreSQL database
- uv package manager (recommended) or pip

## 🛠️ Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/Juan-Andres-Motta/backend-mcp.git
cd backend-mcp

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/Juan-Andres-Motta/backend-mcp.git
cd backend-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password

# Database URL (constructed from above)
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# MCP Server Configuration
MCP_TRANSPORT=stdio  # Options: stdio, http
MCP_HOST=0.0.0.0    # Only used for HTTP transport
MCP_PORT=8000       # Only used for HTTP transport
```

### Database Setup

1. **Using Docker Compose** (Recommended):
   ```bash
   docker-compose up -d postgres
   ```

2. **Manual PostgreSQL Setup**:
   - Install PostgreSQL
   - Create a database
   - Update `.env` with your database credentials

### Database Migrations

Run database migrations to create the appointments table:

```bash
# Using uv
uv run alembic upgrade head

# Using pip
alembic upgrade head
```

## 🚀 Running the Server

### Development Mode (stdio)

```bash
# Using uv
uv run python main.py

# Using pip
python main.py
```

### HTTP Mode

Set `MCP_TRANSPORT=http` in your `.env` file:

```bash
# Using uv
uv run python main.py

# Using pip
python main.py
```

The server will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run only the MCP server (requires external PostgreSQL)
docker build -t appointment-mcp .
docker run --env-file .env appointment-mcp
```

## 📖 API Usage

### MCP Tool: `schedule_appointment`

Schedules a new appointment in the database.

**Parameters:**
- `name` (string): Full name of the person scheduling the appointment
- `identification_number` (string): Identification number (ID card, passport, etc.)
- `phone` (string): Phone number
- `date` (string): Appointment date and time in ISO format (YYYY-MM-DDTHH:MM:SS)

**Example:**
```json
{
  "name": "John Doe",
  "identification_number": "123456789",
  "phone": "+1234567890",
  "date": "2024-12-25T14:30:00"
}
```

**Response:**
```json
{
  "result": "Success: Appointment scheduled for John Doe on 2024-12-25 14:30:00 (ID: 1)"
}
```

## 🏗️ Project Structure

```
backend-mcp/
├── main.py                 # Main MCP server application
├── pyproject.toml          # Project dependencies and configuration
├── uv.lock                 # uv lock file
├── alembic/                # Database migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .env                    # Environment variables (create this)
├── .env.example           # Environment variables template
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore file
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🔧 Development

### Running Tests

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest
```

### Database Schema

The `appointments` table structure:

```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    identification_number VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    date TIMESTAMP NOT NULL
);
```

### Adding New Features

1. Define new MCP tools in `main.py`
2. Update database models if needed
3. Create Alembic migrations for schema changes
4. Update this README

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your `.env` file configuration
   - Ensure PostgreSQL is running
   - Verify database credentials

2. **Migration Errors**
   - Run `alembic current` to check migration status
   - Run `alembic upgrade head` to apply pending migrations

3. **MCP Transport Issues**
   - For stdio mode: Ensure the MCP client supports stdio transport
   - For HTTP mode: Check that the port is not in use

### Getting Help

- Check the [FastMCP documentation](https://fastmcp.com)
- Review [SQLAlchemy documentation](https://sqlalchemy.org)
- Check [Alembic documentation](https://alembic.sqlalchemy.org)

## 📊 Version History

- **v1.0.0**: Initial release with basic appointment scheduling functionality
- Database integration with PostgreSQL
- Docker containerization
- MCP protocol support (stdio and HTTP)