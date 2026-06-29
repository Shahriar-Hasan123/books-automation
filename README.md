# Books Automation — UI Testing Framework

![Playwright Tests](https://github.com/Shahriar-Hasan123/books-automation/actions/workflows/playwright.yml/badge.svg)

A production-ready automation framework built with Playwright and Pytest for testing [books.toscrape.com](https://books.toscrape.com). Validates UI elements, navigation, data consistency, and website functionality with automated reporting.

---

## 1. Project Overview

This framework provides comprehensive UI testing for the Books to Scrape website using industry-standard practices:

- **Page Object Model** architecture for clean, maintainable code
- **5 comprehensive test cases** covering homepage validation, navigation, data consistency, link validation, and image verification
- **Automated evidence capture** — screenshots, videos, and traces attached to reports
- **CI/CD integration** — GitHub Actions pipeline for continuous testing
- **Professional reporting** — HTML and Allure reports with multimedia attachments

Designed for easy setup and maintenance by any engineer without additional guidance.

---

## 2. Features

- ✅ **Page Object Model (POM)** — Clean separation of page interactions from test logic
- ✅ **5 Test Cases** — Homepage validation, navigation, consistency, broken links, image validation
- ✅ **Random Test Data** — Dynamic book selection for varied test coverage
- ✅ **Link Validation** — HTTP 200 checks on all unique homepage links
- ✅ **Image Validation** — Attribute verification across paginated results
- ✅ **Multimedia Capture** — Screenshots, videos, and traces for every test
- ✅ **Professional Reports** — HTML and Allure reports with embedded evidence
- ✅ **No Hardcoded Waits** — Reliable synchronization throughout
- ✅ **GitHub Actions CI/CD** — Automatic testing on every push and PR
- ✅ **Clear Documentation** — Docstrings, meaningful naming, organized structure

---

## 3. Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12 | Programming language |
| Playwright | 1.49.0 | Browser automation |
| Pytest | 8.2.2 | Test framework |
| pytest-html | 4.1.1 | HTML reports |
| allure-pytest | 2.13.5 | Allure reports |
| GitHub Actions | Latest | CI/CD pipeline |
| Allure CLI | 2.27.0 | Report viewer |
| Java | 17+ | Allure dependency |

---

## 4. Installation Guide

### Prerequisites

- Python 3.10+
- Git
- Java 17+ (for Allure)

### Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/Shahriar-Hasan123/books-automation.git
cd books-automation

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
# or: venv\Scripts\activate        # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browser
playwright install chromium

# 5. Install Allure and Java (Linux/Mac)
wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz
tar -xzf allure-2.27.0.tgz
rm allure-2.27.0.tgz

wget https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz
tar -xzf OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz
rm OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz

# 6. Create Allure launcher
echo '#!/bin/bash
export JAVA_HOME="$HOME/Documents/books-automation/jdk-17.0.11+9"
export PATH="$JAVA_HOME/bin:$PATH"
~/Documents/books-automation/allure-2.27.0/bin/allure "$@"' > allure.sh
chmod +x allure.sh

# 7. Verify
./allure.sh --version
```

---

## 5. Environment Setup

### Verify Installation

```bash
python3 --version      # Python 3.12+
playwright --version   # Playwright installed
pytest --version       # Pytest 8.2.2+
./allure.sh --version  # Allure 2.27.0
```

### Verify Test Collection

```bash
pytest --co -q
# Expected: 10 tests collected
```

---

## 6. Running Tests

### All Tests

```bash
pytest -v
```

### By Test Marker

```bash
pytest -m homepage -v           # TC1: Homepage validation
pytest -m navigation -v         # TC2: Random navigation
pytest -m consistency -v        # TC3: Data consistency
pytest -m broken_links -v       # TC4: Broken links
pytest -m images -v            # TC5: Image validation
```

### Using Makefile

```bash
make test                  # Run all tests
make report-html          # Open HTML report
make report-allure        # Generate and open Allure report
make clean                # Clean generated files
```

---

## 7. Project Structure

```
books-automation/
│
├── .github/
│   └── workflows/
│       └── playwright.yml           # GitHub Actions CI/CD workflow
│
├── pages/                           # Page Object Model classes
│   ├── init.py
│   ├── base_page.py                 # Shared methods for all pages
│   ├── home_page.py                 # Homepage-specific interactions
│   └── detail_page.py              # Book detail page interactions
│
├── tests/                           # All test files
│   ├── init.py
│   ├── test_homepage.py             # TC1: Homepage validation
│   ├── test_book_navigation.py      # TC2: Random book navigation
│   ├── test_data_consistency.py     # TC3: Data consistency
│   ├── test_broken_links.py         # TC4: Broken link validation
│   └── test_image_validation.py     # TC5: Product image validation
│
├── utils/                           # Utility helpers
│   ├── init.py
│   └── helpers.py                   # URL builder and shared helpers
│
├── reports/                         # Generated HTML reports     [git ignored]
├── allure-results/                  # Raw Allure result data     [git ignored]
├── allure-report/                   # Generated Allure report    [git ignored]
├── screenshots/                     # Test screenshots           [git ignored]
├── videos/                          # Test video recordings      [git ignored]
├── traces/                          # Playwright trace files     [git ignored]
│
├── conftest.py                      # Global fixtures and hooks
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
├── Makefile                         # Shortcut commands
└── README.md                        # Project documentatio
```

---

## 8. Test Case Coverage

### TC1 — Homepage Validation

**Purpose:** Verify homepage structure, title, and content visibility

| Check | Details |
|-------|---------|
| URL Correctness | Page URL matches expected value |
| Page Title | Browser title matches expected value |
| Headings Visible | All h1–h6 headings are visible |
| Heading Content | All headings contain non-empty text |
| Books Section | Books container is visible |
| Book Presence | At least one book exists |

### TC2 — Random Book Navigation

**Purpose:** Verify book detail page loads and matches homepage data

| Check | Details |
|-------|---------|
| Random Selection | 5 books randomly selected |
| Page Load | Detail page loads successfully |
| Title Match | Detail page H1 matches homepage title |
| Book Info Visible | Product info table visible |
| Navigation Works | Browser back button works |

### TC3 — Book Data Consistency

**Purpose:** Verify title and price match across pages

| Check | Details |
|-------|---------|
| Random Selection | 5 books randomly selected |
| Title Consistency | Homepage title = Detail page title |
| Price Consistency | Homepage price = Detail page price |
| All Match | Zero mismatches across all books |

### TC4 — Broken Link Validation

**Purpose:** Verify all homepage links return HTTP 200

| Check | Details |
|-------|---------|
| Link Collection | All anchor hrefs collected |
| Deduplication | Duplicate URLs removed |
| HTTP Status | All URLs return HTTP 200 |
| Error Reporting | All failures reported together |

### TC5 — Product Image Validation

**Purpose:** Verify product images have required attributes

| Check | Details |
|-------|---------|
| Visibility | Image is visible on page |
| src Attribute | src exists and is not empty |
| alt Attribute | alt exists and is not empty |
| class Attribute | class contains "thumbnail" |
| Multiple Pages | Validation repeats for up to 5 pages |

---

## 9. Report Generation Guide

### HTML Report

Generated automatically after every test run:

```bash
pytest -v
# Report saved to: reports/report.html
```

**Contents:**
- Test pass/fail summary
- Individual test results with duration
- Failure screenshots embedded
- Error messages and tracebacks

### Allure Report

```bash
# Generate from raw data
./allure.sh generate allure-results --clean -o allure-report

# View in browser
./allure.sh open allure-report

# Or use shortcut
make report-allure
```

**Contents:**
- Test suites grouped by feature
- Pass/fail breakdown with charts
- Timeline view of execution
- Severity levels per test
- Screenshots, videos, and traces per test

---

## 10. HTML Report Guide

The HTML report is self-contained and opens in any browser:

**How to View:**
```bash
# Linux/Mac
xdg-open reports/report.html

# Windows
start reports/report.html

# Or via Makefile
make report-html
```

**Report Information:**
- **Summary** — Total passed, failed, skipped tests
- **Execution Time** — Duration per test and total
- **Test Details** — Step-by-step execution info
- **Screenshots** — Failure screenshots embedded
- **Errors** — Full error messages and stack traces

The report is fully responsive and printable.

---

## 11. Allure Report Guide

Allure provides detailed multimedia reports with better visualization than HTML reports.

**Step 1: Run Tests**
```bash
pytest -v
# Generates raw data in allure-results/
```

**Step 2: Generate Report**
```bash
./allure.sh generate allure-results --clean -o allure-report
```

**Step 3: View Report**
```bash
./allure.sh open allure-report
```

**Report Features:**
- Suites view with hierarchical test organization
- Behaviors (Features) grouped by story
- Graphs showing pass/fail trends
- Timeline showing test execution order
- **Multimedia Attachments:**
  - 📸 Screenshots (Initial state, validation steps, failure state)
  - 🎥 Video recording (Full test playback in WebM format)
  - 📦 Playwright trace (For step-by-step replay in Playwright Inspector)

---

## 12. GitHub Actions Setup

### Workflow File

Location: `.github/workflows/playwright.yml`

### Triggers

Runs automatically on:
- Push to `main` or `feature/**` branches
- Pull requests targeting `main`

### Pipeline Steps

```
1. Checkout code
2. Setup Python 3.12
3. Cache pip dependencies
4. Install Python packages
5. Install Playwright browsers
6. Create output directories
7. Run all tests
8. Upload HTML report artifact
9. Upload Allure results artifact
10. Upload screenshots artifact
11. Upload videos artifact
12. Upload traces artifact
```

### Download Artifacts from GitHub

1. Go to repository → **Actions** tab
2. Click on completed workflow run
3. Scroll to **Artifacts** section
4. Download desired artifact:
   - `html-report` — Open `report.html` in browser
   - `allure-results` — Run `./allure.sh generate` locally
   - `screenshots` — View test evidence images
   - `videos` — Watch test recordings
   - `traces` — Use with Playwright Inspector

---

## 13. Design Decisions

### Page Object Model (POM)

All page interactions encapsulated in `pages/` classes. Tests call page methods, never direct selectors. **Benefits:** DRY principle, easy maintenance, single point of change.

### BasePage Inheritance

Shared methods (`wait_for_element`, `is_element_visible`, `take_screenshot`) in `BasePage`. All pages inherit. **Benefits:** Code reuse, SOLID Open/Closed principle.

### No Hardcoded Waits

No `time.sleep()` anywhere. Uses Playwright's built-in `wait_for_element()`, `wait_for_load_state()`, and element-level `wait_for()`. **Benefits:** Fast, reliable, no flaky tests.

### Selectors as Constants

All CSS selectors defined as class constants. When HTML changes, only update the constant. **Benefits:** Single point of change, easy refactoring.

### Playwright Request Context for Links

TC4 uses `page.request.get()` instead of `requests` library. Shares browser session, handles SSL correctly. **Benefits:** Avoids connection resets, proper headers.

### Collect All Failures

TC4 and TC5 collect all failures before asserting. See ALL broken links/bad images in one run. **Benefits:** Faster debugging, complete visibility.

### Session Browser, Function Context

Browser shared across tests (performance). Each test gets fresh context/page (isolation). **Benefits:** Balance between speed and test independence.

### Evidence for All Tests

Captures screenshots, videos, traces for PASS and FAIL. Provides audit trail, not just debugging. **Benefits:** QA confidence, compliance, troubleshooting.

---

## 14. Known Limitations

- **Broken Link Validation (TC4)** — Uses HTTP requests; links requiring JavaScript rendering may not validate accurately
- **Random Book Selection (TC2, TC3)** — Only selects from first page (20 books); subsequent pages not included
- **Allure CLI** — Requires Java 17+; manual installation needed on machines without sudo
- **Video Format** — WebM format; Windows users may need VLC player to view
- **Allure Report** — Requires manual `allure generate` after each test run (no auto-refresh)
- **Execution Time** — TC4 (broken links) typically 30–60 seconds due to HTTP requests
- **Trace Files** — ZIP files can be large (5–50 MB per test); archived in CI but not auto-deleted locally

---

## Support & Maintenance

For issues or improvements, refer to individual page objects and test files for detailed docstrings. Each method explains its purpose and usage.

**Quick Commands:**
```bash
make test              # Run tests
make report-html       # View HTML report
make report-allure     # View Allure report
make clean             # Clean artifacts
```

---

**Last Updated:** June 2026  
**Framework Version:** 1.0.0  
**Status:** Production Ready
