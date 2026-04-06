# ⚡ AuraTest: Autonomous Self-Healing Test Framework

AuraTest is an intelligent QA automation layer designed to eliminate "flaky tests." By integrating Generative AI with Selenium, AuraTest can autonomously detect element changes and heal broken locators in real-time without human intervention.

---

## 🧠 The Intelligence Engine (Module 3)
The core of AuraTest is a **Proprietary AI Healer** that acts as the "brain" of the execution cycle. 

### Key Capabilities:
* **Dynamic DOM Analysis:** When a standard Selenium locator fails, the AI performs a real-time scan of the minimized HTML Document Object Model (DOM).
* **Semantic Mapping:** Uses advanced Large Language Models (LLMs) to identify the "successor" of a broken element based on visual context, attributes, and structural positioning.
* **Autonomous Resolution:** Automatically generates a replacement locator and re-injects it into the active browser session to prevent test failure.

---

## 🏗️ High-Level Architecture
AuraTest operates on a three-tier "Intercept-Analyze-Heal" architecture:

1.  **The Interceptor:** Monitors the execution flow and catches `NoSuchElementException` errors before they crash the test suite.
2.  **The Context Optimizer:** Pre-processes the raw HTML page source, stripping noise (scripts/styles) to focus on structural elements.
3.  **The Neural Healer:** Leverages enterprise-grade LLM endpoints to perform inference on the broken state and return a high-confidence replacement ID.

---

## 🚀 Impact & Results
* **Zero-Touch Maintenance:** Tests stay "green" even when UI developers change button IDs or CSS classes.
* **Reduced Latency:** Optimized DOM processing ensures the healing process takes less than 2 seconds.
* **Resilient Automation:** Dramatic reduction in manual script updates and "flaky" test reports.

---

## 🛠️ Setup & Requirements
* **Python 3.10+**
* **Selenium Webdriver**
* **Enterprise API Access:** (Requires configured `.env` with secure credentials)
* **BeautifulSoup4:** For structural DOM optimization.
