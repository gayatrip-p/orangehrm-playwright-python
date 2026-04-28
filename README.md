# OrangeHRM Playwright Python — Automation Portfolio Project

> End-to-end test automation framework for [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com)
> Built with **Playwright + Python + pytest + Allure**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.44-green)
![pytest](https://img.shields.io/badge/pytest-8.2-orange)

---

## 📁 Project Structure

```
orangehrm-playwright/
│
├── pages/                  # Page Object Model (POM) classes
│   ├── base_page.py        # Parent class — reusable methods
│   ├── login_page.py       # Login page locators + actions
│   └── dashboard_page.py  # Dashboard page locators + actions
│
├── tests/                  # Test files
│   └── test_login.py       # 10 login test cases
│
├── test-data/              # Test data separated from test logic
│   └── login_data.py       # Login credentials + expected messages
│
├── reports/                # Auto-generated HTML + Allure reports
├── conftest.py             # Shared pytest fixtures
├── pytest.ini              # pytest configuration
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (credentials, URL)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/orangehrm-playwright.git
cd orangehrm-playwright
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env if needed (default creds already set for demo site)
```

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run only smoke tests
pytest -m smoke

# Run only login tests
pytest -m login

# Run specific test file
pytest tests/test_login.py

# Run specific test case
pytest tests/test_login.py::TestLogin::test_valid_login

# Run headless (no browser window)
pytest --headed=false

# Run on Firefox
pytest --browser firefox

# Run on all 3 browsers
pytest --browser chromium --browser firefox --browser webkit
```

---

## 📊 Viewing Reports

### HTML Report (instant)
```bash
pytest
open reports/report.html
```

### Allure Report (detailed with steps + screenshots)
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 🧪 Test Cases Covered

| ID            | Test Case                               | Priority | Marker     |
|---------------|-----------------------------------------|----------|------------|
| TC_LOGIN_001  | Valid login → Dashboard redirect        | Critical | smoke      |
| TC_LOGIN_002  | Invalid password → Error message        | Critical | regression |
| TC_LOGIN_003  | Invalid username → Error message        | Critical | regression |
| TC_LOGIN_004  | Empty username → Required validation    | Normal   | regression |
| TC_LOGIN_005  | Empty password → Required validation    | Normal   | regression |
| TC_LOGIN_006  | Both empty → Two Required messages      | Normal   | regression |
| TC_LOGIN_007  | Login page UI elements visible          | Minor    | smoke      |
| TC_LOGIN_008  | Logout → Back to login page             | Critical | regression |
| TC_LOGIN_009  | Data-driven: 10 invalid combinations    | Normal   | regression |
| TC_LOGIN_010  | Page title is 'Login'                   | Minor    | smoke      |

---

## 🏗️ Design Patterns Used

- **Page Object Model (POM)** — locators and actions per page
- **BasePage inheritance** — shared methods, no code duplication
- **Fixtures (conftest.py)** — reusable setup, pre-login state
- **Data-driven testing** — `pytest.mark.parametrize` + external data file
- **Allure reporting** — step-by-step report with screenshots on failure

---

## 📌 Tech Stack

| Tool           | Purpose                        |
|----------------|--------------------------------|
| Python 3.11+   | Programming language           |
| Playwright     | Browser automation             |
| pytest         | Test runner                    |
| pytest-html    | HTML test report               |
| Allure         | Rich test reporting            |
| python-dotenv  | Environment variable management|
