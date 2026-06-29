# 📚 Enterprise UI Automation Framework — Books to Scrape

![Playwright Tests](https://github.com/Shahriar-Hasan123/books-automation/actions/workflows/playwright.yml/badge.svg)

A production-ready UI automation framework built with **Playwright** and **Pytest**
that validates website functionality, data consistency, UI elements, navigation
behavior, and quality assurance scenarios for
[Books to Scrape](https://books.toscrape.com/index.html).

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation Guide](#installation-guide)
- [Environment Setup](#environment-setup)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Test Case Coverage](#test-case-coverage)
- [Report Generation Guide](#report-generation-guide)
- [HTML Report Guide](#html-report-guide)
- [Allure Report Guide](#allure-report-guide)
- [GitHub Actions Setup](#github-actions-setup)
- [Design Decisions](#design-decisions)
- [Known Limitations](#known-limitations)

---

## 🎯 Project Overview

This framework automates end-to-end UI testing for the
[Books to Scrape](https://books.toscrape.com/index.html) website.
It is designed following industry-standard practices including the
**Page Object Model (POM)**, **OOP**, **SOLID**, and **DRY** principles.

The framework:
- Validates homepage content and structure
- Verifies random book navigation and detail page accuracy
- Checks data consistency between homepage and detail pages
- Detects broken hyperlinks across the homepage
- Validates product image attributes across multiple pages
- Generates HTML and Allure reports automatically
- Runs fully automated via GitHub Actions CI/CD on every push and pull request

---

## ✨ Features

- ✅ Page Object Model (POM) architecture for clean, reusable code
- ✅ 5 comprehensive test cases covering all functional requirements
- ✅ Random book selection for dynamic test coverage
- ✅ Broken link detection using Playwright request context
- ✅ Product image attribute validation with pagination support
- ✅ Data consistency checks across pages
- ✅ Automatic screenshot capture for every test (PASS and FAIL)
- ✅ Video recording for every test (PASS and FAIL)
- ✅ Trace capture for every test (PASS and FAIL)
- ✅ HTML report generation via pytest-html
- ✅ Allure report generation via allure-pytest
- ✅ GitHub Actions CI/CD pipeline with artifact upload
- ✅ No hardcoded waits — reliable synchronization strategies throughout
- ✅ Meaningful naming conventions and method docstrings

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Programming language |
| Playwright | 1.49.0 | Browser automation |
| Pytest | 8.2.2 | Test framework |
| pytest-playwright | 0.5.0 | Playwright-Pytest integration |
| pytest-html | 4.1.1 | HTML report generation |
| allure-pytest | 2.13.5 | Allure report generation |
| requests | 2.32.3 | HTTP client for link validation |
| GitHub Actions | - | CI/CD pipeline |
| Allure CLI | 2.27.0 | Allure report viewer |

---

## 📥 Installation Guide

### Prerequisites

Make sure these are installed on your machine:

- Python 3.10 or higher
- Git
- Java 17+ (required for Allure CLI)

### 1. Clone the repository

```bash
git clone https://github.com/Shahriar-Hasan123/books-automation.git
cd books-automation
```

### 2. Create and activate virtual environment

```
# Create virtual environment
python3 -m venv venv

# Activate on Mac/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Python dependencies

```
pip install -r requirements.txt
```

### 4. Install Playwright browser

```
playwright install chromium
```

### 5. Install Allure CLI (without sudo)

```
# Download Allure
wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz
tar -xzf allure-2.27.0.tgz
rm allure-2.27.0.tgz

# Download Java 17 (if not installed)
wget https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz
tar -xzf OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz
rm OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz

# Create allure.sh launcher
echo '#!/bin/bash
export JAVA_HOME="$HOME/Documents/books-automation/jdk-17.0.11+9"
export PATH="$JAVA_HOME/bin:$PATH"
~/Documents/books-automation/allure-2.27.0/bin/allure "$@"' > allure.sh

chmod +x allure.sh

# Verify
./allure.sh --version
```

---

## ⚙️ Environment Setup

### Verify installation

```
# Check Python
python3 --version

# Check Playwright
playwright --version

# Check Pytest
pytest --version

# Check Allure
./allure.sh --version
```

### Verify test collection

```
pytest --co -q
```

Expected output:

```
10 tests collected
```

---

## 🚀 Running Tests

### Run all tests

```
pytest -v
```

### Run a specific test case by marker

```
# TC1 - Homepage Validation
pytest -m homepage -v

# TC2 - Random Book Navigation
pytest -m navigation -v

# TC3 - Book Data Consistency
pytest -m consistency -v

# TC4 - Broken Link Validation
pytest -m broken_links -v

# TC5 - Product Image Validation
pytest -m images -v
```

### Run a specific test file

```
pytest tests/test_homepage.py -v
pytest tests/test_book_navigation.py -v
pytest tests/test_data_consistency.py -v
pytest tests/test_broken_links.py -v
pytest tests/test_image_validation.py -v
```

### Run with Makefile shortcuts

```
make test          # run all tests
make report-html   # open HTML report
make report-allure # generate and open Allure report
make clean         # clean all generated files
```

---

## 📁 Project Structure

```
books-automation/
│
├── .github/
│   └── workflows/
│       └── playwright.yml          # GitHub Actions CI/CD workflow
│
├── pages/                          # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py                # Shared methods for all pages
│   ├── home_page.py                # Homepage interactions
│   └── detail_page.py             # Book detail page interactions
│
├── tests/                          # All test files
│   ├── __init__.py
│   ├── test_homepage.py            # TC1: Homepage validation
│   ├── test_book_navigation.py     # TC2: Random book navigation
│   ├── test_data_consistency.py    # TC3: Data consistency
│   ├── test_broken_links.py        # TC4: Broken link validation
│   └── test_image_validation.py    # TC5: Product image validation
│
├── utils/                          # Helper utilities
│   ├── __init__.py
│   └── helpers.py                  # URL builder and shared helpers
│
├── reports/                        # Generated HTML reports (git ignored)
├── allure-results/                 # Raw Allure data (git ignored)
├── allure-report/                  # Generated Allure report (git ignored)
├── screenshots/                    # Test screenshots (git ignored)
├── videos/                         # Test videos (git ignored)
├── traces/                         # Playwright traces (git ignored)
│
├── conftest.py                     # Global fixtures and hooks
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
├── Makefile                        # Shortcut commands
└── README.md                       # Project documentation
```

---

## 🧪 Test Case Coverage

### TC1 — Homepage Validation

| Check | Description |
|-------|-------------|
| URL | Page URL matches expected value |
| Title | Browser tab title matches expected value |
| Headings | All h1–h6 headings are visible |
| Heading text | Every heading contains non-empty text |
| Books section | Books container is visible |
| Book count | At least one book is present |

### TC2 — Random Book Navigation

| Check | Description |
|-------|-------------|
| Random selection | 5 books randomly selected from homepage |
| Page load | Each detail page loads successfully |
| Title match | H1 on detail page matches homepage title |
| Book info | Product information table is visible |
| Navigation | Browser navigates back to homepage after each book |

### TC3 — Book Data Consistency

| Check | Description |
|-------|-------------|
| Random selection | 5 books randomly selected from homepage |
| Title consistency | Homepage title matches detail page title |
| Price consistency | Homepage price matches detail page price |
| No mismatches | Zero data inconsistencies across all 5 books |

### TC4 — Broken Link Validation

| Check | Description |
|-------|-------------|
| Link collection | All anchor href values collected from homepage |
| Deduplication | Duplicate URLs removed before checking |
| HTTP status | Every unique URL returns HTTP 200 |
| Error handling | Network errors reported clearly |

### TC5 — Product Image Validation

| Check | Description |
|-------|-------------|
| Visibility | Each image is visible on the page |
| src attribute | src exists and is not empty |
| alt attribute | alt exists and is not empty |
| class attribute | class contains "thumbnail" |
| Pagination | Validation repeats for up to 5 pages |

---

## 📊 Report Generation Guide

### HTML Report Guide

HTML report is generated automatically every time you run tests:

```
pytest -v
```

Report is saved to:

```
reports/report.html
```

Open the report:

```
# Linux
xdg-open reports/report.html

# Mac
open reports/report.html

# Windows
start reports/report.html

# Or via Makefile
make report-html
```

The HTML report shows:

- Total tests passed/failed
- Test duration
- Failure details with error messages
- Screenshots embedded for failed tests

---

## 🎨 HTML Report Guide

HTML report is generated automatically every time you run tests. The report includes:

- **Summary** — Total passed, failed, skipped test counts
- **Test Results** — Individual test details with pass/fail status
- **Duration** — Execution time for each test
- **Screenshots** — Embedded images for failed tests
- **Error Messages** — Full error details and tracebacks

---

## 📈 Allure Report Guide

**Step 1 — Run tests** (generates raw Allure data):

```
pytest -v
```

Raw data is saved to `allure-results/`

**Step 2 — Generate the report:**

```
./allure.sh generate allure-results --clean -o allure-report
```

**Step 3 — Open the report:**

```
./allure.sh open allure-report
```

Or use the Makefile shortcut:

```
make report-allure
```

The Allure report shows:

- Test suites grouped by feature
- Individual test steps
- Severity levels (Critical, Normal)
- Pass/fail breakdown charts
- Timeline view
- Screenshots, videos, and traces per test

---

## ⚙️ GitHub Actions Setup

### Workflow file location

```
.github/workflows/playwright.yml
```

### Triggers

The workflow runs automatically on:

- Every **push** to `main` or any `feature/**` branch
- Every **pull request** targeting `main`

### Pipeline Steps

```
1. Checkout Repository
2. Set Up Python 3.12
3. Cache pip packages
4. Install Python Dependencies
5. Install Playwright Browsers (with system dependencies)
6. Create Output Directories
7. Run All Tests
8. Upload HTML Report artifact
9. Upload Allure Results artifact
10. Upload Screenshots artifact
11. Upload Videos artifact
12. Upload Traces artifact
```

### Downloading Artifacts

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Click on any completed workflow run
4. Scroll to the **Artifacts** section at the bottom
5. Download:

- `html-report` → open `report.html` in browser
- `allure-results` → run `./allure.sh generate` to view
- `screenshots` → PASS/FAIL prefixed images per test
- `videos` → PASS/FAIL prefixed recordings per test
- `traces` → PASS/FAIL prefixed traces per test

### Viewing Allure Results from CI

```
# After downloading allure-results artifact and unzipping:
./allure.sh generate allure-results --clean -o allure-report
./allure.sh open allure-report
```

---

## 🏗️ Design Decisions

### Page Object Model (POM)

All page interactions are encapsulated in dedicated classes inside `pages/`.
Tests never interact with HTML selectors directly — they call page methods.
This ensures DRY (no duplicated locator logic) and makes maintenance easy.

### BasePage Inheritance

`BasePage` contains shared methods (`wait_for_element`, `is_element_visible`,
`get_current_url`, etc.). All page classes inherit from `BasePage`.
This follows the SOLID Open/Closed principle.

### No Hardcoded Waits

`time.sleep()` is never used. All synchronization uses Playwright's built-in
`wait_for_element()`, `wait_for_load_state()`, and element-level `wait_for()`
methods. This makes tests fast and reliable.

### Selectors as Class Constants

All CSS selectors are defined as class-level constants in page objects.
If the website changes its HTML structure, only the constant needs updating —
not every test that uses it.

### Playwright Request Context for Link Validation

TC4 uses `page.request.get()` instead of the `requests` library.
This shares the browser session, handles SSL correctly, and sends proper
browser headers — avoiding connection resets and SSL errors.

### Collect All Failures Before Asserting

TC4 and TC5 collect all failures into a list before calling `pytest.fail()`.
This ensures you see ALL broken links or ALL bad images in one run —
not just the first failure.

### Session-Scoped Browser, Function-Scoped Page

The browser instance is shared across all tests (session scope) for performance.
Each test gets its own browser context and page (function scope) for isolation.
No test state bleeds into another.

### Evidence for Every Test

Screenshots, videos, and traces are captured for every test (PASS and FAIL).
This provides full audit trails for QA review, not just failure debugging.

---

## ⚠️ Known Limitations

- **TC4 Broken Links** uses Playwright's request context. Some links that
require JavaScript rendering may not be validated accurately via HTTP request.
- **TC2 and TC3** randomly select 5 books from the first page only (20 books).
Books on subsequent pages are not included in random selection.
- **Allure CLI** requires Java 17+ installed locally. On machines without
sudo access, Java must be installed manually as shown in the Installation Guide.
- **Video files** are in `.webm` format. On Windows, you may need a media
player like VLC to view them.
- **Allure report** requires running `allure generate` after every test run.
It does not auto-refresh like the HTML report.
- **Test execution time** varies. TC4 (broken links) makes HTTP requests to
all homepage URLs and typically takes 30–60 seconds depending on network speed.