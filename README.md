# 📞 Automated UI Testing Framework (Phonebook App)

[![UI Tests CI](https://github.com/arfami096/QA3553_Phonebook/actions/workflows/ci.yml/badge.svg)](https://github.com/arfami096/QA3553_Phonebook/actions/workflows/ci.yml)

An automated UI testing framework for the "Phonebook" web application. The project covers a full spectrum of requirements: from positive scenarios and handling mandatory fields to negative validation (alerts, length and character constraints) and record uniqueness checks.

## 🛠 Tech Stack
* **Language:** Python
* **Test Runner:** Pytest
* **Automation Tool:** Selenium WebDriver
* **Architecture:** Page Object Model (POM)
* **CI/CD:** GitHub Actions (Headless Chrome)

## 📂 Project Structure
* `pages/` — Page Object classes for interacting with UI elements.
* `tests/` — Automated test suites (positive, negative scenarios, boundary values).
* `models/` — Data models and structures for test entities.
* `utils/` — Helper utilities (API client, data generator, logger, storage helpers).
* `.github/workflows/` — CI/CD configuration for automated test runs on GitHub.
* `pytest.ini` — Configuration file for Pytest settings and custom markers.

## 🚀 How to Run Tests Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/arfami096/QA3553_Phonebook.git](https://github.com/arfami096/QA3553_Phonebook.git)

Note on Configuration & Hidden Files:

Certain configuration files or environment variable files (such as files containing credentials) may not be stored in the public repository for security reasons.

Confidential files: If hidden configuration files are required for local test execution, you must request them separately from the project author.

Viewing hidden files: If you are working on macOS and cannot see files starting with a dot (e.g., .env, .gitignore), press Cmd + Shift + . (dot) in Finder or configure your code editor to show hidden files.
