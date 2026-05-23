# 🎭 Playwright Automation Framework

**Python-based UI test automation suite** for [SauceDemo](https://www.saucedemo.com) — a practice e-commerce site.  
Built to demonstrate SDET skills: test architecture, Page Object readiness, CI/CD integration, and HTML reporting.

---

## 🧪 Test Coverage

| Module | Tests | What It Covers |
|--------|-------|----------------|
| `test_login.py` | 7 | Valid login, invalid credentials, locked user, empty fields, logout |
| `test_inventory.py` | 9 | Product display, sorting (A-Z, price), add/remove from cart, product detail |
| `test_checkout.py` | 9 | Cart management, checkout form validation, full happy path E2E |

**Total: 25 tests across 3 modules**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `playwright` | Browser automation |
| `pytest` | Test runner & assertions |
| `pytest-html` | HTML test report generation |
| `GitHub Actions` | CI/CD pipeline |

---

## 🚀 Run Locally

### 1. Clone & install dependencies
```bash
git clone https://github.com/YOUR_USERNAME/playwright-sdet-portfolio.git
cd playwright-sdet-portfolio
pip install -r requirements.txt
playwright install chromium
```

### 2. Run all tests
```bash
pytest
```

### 3. Run a specific module
```bash
pytest tests/test_login.py -v
pytest tests/test_checkout.py -v
```

### 4. Run in headed mode (watch the browser)
```bash
pytest --headed
```

### 5. View HTML report
After running, open `reports/report.html` in your browser.

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

The pipeline triggers on:
- Every **push** to `main` or `develop`
- Every **pull request** to `main`
- **Daily at 8:00 AM UTC** (scheduled regression run)
- **Manual trigger** from the GitHub Actions UI

### Pipeline Steps
1. ✅ Checkout code
2. ✅ Set up Python 3.11
3. ✅ Install dependencies + Playwright browsers
4. ✅ Run full test suite
5. ✅ Upload HTML report as artifact (retained 30 days)
6. ✅ Write summary to GitHub job summary page
7. 🚨 On failure: auto-creates a GitHub Issue with run details

---

## 📁 Project Structure

```
playwright-sdet-portfolio/
├── .github/
│   └── workflows/
│       └── playwright.yml      # CI/CD pipeline
├── tests/
│   ├── conftest.py             # Shared fixtures (browser, page, logged_in_page)
│   ├── test_login.py           # Login / auth tests
│   ├── test_inventory.py       # Product listing tests
│   └── test_checkout.py        # Cart & checkout tests
├── reports/                    # Generated HTML reports (git-ignored)
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🔧 Key Design Decisions

- **Session-scoped browser** — browser launched once per test session for speed
- **Function-scoped pages** — each test gets a clean page with no shared state
- **`logged_in_page` fixture** — reusable login state without repeating login steps
- **`data-test` selectors** — resilient locators that survive UI redesigns
- **`continue-on-error`** in CI — ensures reports are always uploaded, even on failure

---

## 👤 Author

**Mehul Jethva** — QE Automation Engineer / SDET  
[LinkedIn](https://www.linkedin.com/in/mehuljethva29/) | Toronto, ON
