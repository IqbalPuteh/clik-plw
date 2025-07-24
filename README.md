# Credit-Bureau-Nusantara---Playwright

A robust automation service using Playwright and FastAPI to simulate user workflows on Credit Bureau Nusantara (CBN). This project integrates asynchronous RPA logic with secure endpoints, retry mechanisms, structured logging, and session management, enabling seamless backend orchestration for web automation.

---

## Features

- Headless browser automation via Playwright  
- Retry and fallback logic with `tenacity`  
- Modular task execution with parameterized inputs  
- Secure configuration via `.env` using `python-dotenv`  
- API-based trigger and status control using FastAPI  
- Webhook-compatible status updates and task reporting  
- Structured logging of failures and progress  
- Support for self-contained output in CSV and JSON formats  

---

## Prerequisites

- Python 3.10+  
- Playwright with Chromium installed  
- FastAPI  
- Uvicorn  
- Tenacity  
- python-dotenv  

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the root directory and define:

```env
CBN_USERNAME=your_cbn_username
CBN_PASSWORD=your_cbn_password
SESSION_TIMEOUT=300
MAX_RETRIES=3
RETRY_WAIT_SECONDS=5
WEBHOOK_URL=https://your-webhook-url.com/update
EXPORT_FORMAT=csv
```

---

## Usage

### Start the API service

```bash
uvicorn api_main:app --reload
```

### Available Endpoints

| Endpoint         | Method | Description                              |
|------------------|--------|------------------------------------------|
| `/start-session` | POST   | Begins a Playwright automation session   |
| `/status`        | GET    | Returns current session or task status   |
| `/logs`          | GET    | Retrieves logs of previous executions    |
| `/reset`         | POST   | Clears session and temporary files       |

### Automation Flow

1. `/start-session` triggers a browser instance  
2. Navigates to CBN login and performs sign-in  
3. Executes desired tasks (based on input parameters)  
4. Applies retry and fallback workflows if needed  
5. Stores result in local file (CSV/JSON)  
6. Sends webhook update with task status  

---

## Project Structure

```plaintext
Credit-Bureau-Nusantara---Playwright/
├─ .vscode/                     # Editor settings and launch configurations
├─ code_backup/                # Archived or legacy code for reference
├─ templates/                  # Template HTML files
│  └─ admin.html               # Web interface for admin or browser automation
├─ .gitignore                  # Git ignore rules
├─ README.md                   # Project documentation
├─ api-main.py                 # FastAPI entry point for automation
├─ config.py                   # Static configuration settings
├─ config_helper.py            # Helper functions for reading and applying config
├─ requirement.txt             # Python dependency list

---
```
## Logging

Logs include:
- Session start/end timestamps  
- Retry attempts and reason for fallback  
- Output file location and webhook response  
- Any browser or network errors encountered

Log format is compatible with `TextWriterTraceListener` style or JSON lines.


## Contributing

1. Fork the repository  
2. Create your feature branch:  
   ```bash
   git checkout -b feature/MyFeature
   ```  
3. Commit your changes  
4. Open a pull request  

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full terms.

---

### You can see a script in recorded action 

https://github.com/user-attachments/assets/91cab32c-8654-4303-bf8a-5fac24fed5bb

---

## Repository

[Credit-Bureau-Nusantara---Playwright](https://github.com/IqbalPuteh/Credit-Bureau-Nusantara---Playwright)

