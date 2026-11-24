# API Data Synchronization & Validation System

A Python-based automation project that retrieves GitHub events from a REST API, validates incoming data, stores records in SQLite, processes pending events, and exports results to CSV.

The project demonstrates reliable API integration, structured data validation, database operations, error handling, logging, automated testing, and idempotent data synchronization.

## Key Features

- **API Integration:** Fetches event data from the GitHub Events API using Requests.
- **Retry Mechanism:** Uses Tenacity to retry requests after connection errors and timeouts.
- **Data Validation:** Validates incoming API records using Pydantic models.
- **SQLite Storage:** Stores validated events in a local SQLite database.
- **Duplicate Prevention:** Uses database constraints and `INSERT OR IGNORE` to prevent duplicate records.
- **Event Processing:** Processes pending events according to their event types.
- **Processing Status:** Tracks event statuses, including Pending and Completed.
- **Logging:** Records application activities and errors.
- **CSV Export:** Exports stored event records into a CSV file.
- **Automated Testing:** Includes unit and integration tests using Pytest.

## Project Architecture

```text
api_data_sync/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── api_client.py
│   ├── models.py
│   ├── validator.py
│   ├── storage.py
│   ├── processor.py
│   ├── reporter.py
│   └── csv_exporter.py
│
├── tests/
│   ├── conftest.py
│   ├── test_api_client.py
│   ├── test_models.py
│   ├── test_validator.py
│   ├── test_storage.py
│   ├── test_processor.py
│   ├── test_csv_exporter.py
│   └── test_main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Application Workflow

The application follows an organized data synchronization pipeline:

1. Initialize the SQLite database.
2. Fetch events from the GitHub REST API.
3. Validate incoming records using Pydantic.
4. Store valid events in SQLite.
5. Ignore duplicate records.
6. Retrieve pending events.
7. Process supported event types and update their statuses.
8. Generate a synchronization report.
9. Export stored events to CSV.

## Technologies Used

| Technology | Purpose                                   |
| ---------- | ----------------------------------------- |
| Python     | Core programming language                 |
| Requests   | REST API integration                      |
| Pydantic   | Data validation                           |
| SQLite     | Persistent data storage                   |
| Tenacity   | Retry mechanism                           |
| Logging    | Application monitoring and error tracking |
| CSV        | Data export                               |
| Pytest     | Automated testing                         |

## Installation & Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd api_data_sync
```

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
py -m pip install -r requirements.txt
```

## Running the Application

From the project root directory:

```bash
py -m src.main
```

The application will initialize the database, retrieve and validate events, store new records, process pending events, generate a report, and export the results.

**Important:** The processing step retrieves all records currently marked as Pending in the database, including records from previous runs. Run the application against a test database first if you do not want to modify existing processing statuses.

## Running Tests

Execute the complete test suite:

```bash
py -m pytest -v
```

The project currently includes **24 automated tests** covering:

- API requests and error handling.
- Retry behavior.
- Pydantic model validation.
- Data validation.
- SQLite database operations.
- Duplicate prevention and idempotency.
- Event processing and failure handling.
- CSV export.
- Main application workflow.

## Reliability Considerations

- API requests use a maximum of three attempts for connection errors and timeouts.
- Exponential backoff is used between retry attempts.
- HTTP errors are raised and handled, but are not included in the configured retry conditions.
- Duplicate records are prevented using database-level insertion rules.
- Completed events are excluded from subsequent pending-event queries.
- Processing failures are logged, and unsuccessful events remain Pending.

## Current Limitations

- Event processing is currently a simulation: supported event types are classified and logged or printed; no actual GitHub actions are performed.
- Retry handling currently applies to connection errors and timeouts, not all HTTP status errors.
- Exactly-once processing is not guaranteed if processing succeeds but the database status update fails.
- The application currently uses SQLite for local storage.

## Future Improvements

- Add configurable API endpoints and settings.
- Implement more advanced API rate-limit handling.
- Add configurable retry policies for selected HTTP errors.
- Improve processing recovery and transaction handling.
- Integrate real downstream automation actions.
- Add monitoring and structured reporting.

## Test Status

**24 tests passing**

This project was developed as a practical exercise in building reliable Python automation systems with API integration, data validation, persistence, processing, and automated testing.
