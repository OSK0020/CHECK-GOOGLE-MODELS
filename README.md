# 🤖 CHECK-GOOGLE-MODELS
> **Active Model Scanner for Google AI Studio — 1-Click test for permissions, free/paid status, quotas, and real-time Web Search Grounding.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google GenAI SDK](https://img.shields.io/badge/SDK-google--genai-green.svg)](https://pypi.org/project/google-genai/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange.svg)](https://github.com/OSK0020/CHECK-GOOGLE-MODELS/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 The Story — Why I Built This?

When I started building AI bots and automation workflows, I wanted to give them a **smart "brain"** capable of searching for up-to-date real-time information on the web.

However, when I accessed **Google AI Studio**, I felt completely overwhelmed:
* ❓ Which models are actually open and accessible in my account?
* 💰 What is available for free (Free Tier) vs. what requires a paid billing account (`403 Forbidden`)?
* ⚠️ Which models are constrained due to rate limits or quota caps (`429 Rate Limit`)?
* 🌐 And most importantly — **Which model actually supports live Google Search Grounding?**

Google's official models list displays dry metadata, but it doesn't reveal what actually works for your specific account. 
That's why I created this repository: **a single 1-click execution script**, requiring only a single API Key, that actively scans all models and generates a comprehensive, beautiful report!

---

## 🌟 Key Features

* ⚡ **Active Grounding Test**: Sends an actual test request to every text model with Google Search Grounding enabled (`types.Tool(google_search=types.GoogleSearch())`).
* 📊 **Clear Access & Cost Classification**:
  * ✅ `Open & Working (Web Search Enabled)`: Model is accessible and ready to use (including Free Tier).
  * ⚠️ `Free Tier Rate Limit / Quota Exceeded (429 Rate Limit)`: Model exists but currently hit request limits.
  * ❌ `Access Denied / Requires Paid Billing (403 Forbidden)`: Restricted on free accounts; requires paid billing.
  * ❌ `Open for Text Generation Only`: Model generates text but does not support Web Search Grounding.
* 📝 **Multi-Format Report Generation**:
  * **`models_report.md`**: Clean, human-readable Markdown report.
  * **`models_report.json`**: Structured JSON data for programmatic pipelines.
  * **`GITHUB_STEP_SUMMARY`**: Visual summary rendered directly in GitHub Actions.
* 🛡️ **Cross-Platform & Windows Safe**: Built-in UTF-8 stream reconfiguration prevents `UnicodeEncodeError` crashes on Windows consoles.

---

## 🚀 Quick Start

### Option 1: 1-Click Execution on GitHub (No Installation Required!)

1. Navigate to **Actions** tab -> Select **Run Gemini Models Check** -> Click **Run workflow**.
2. **Choose your API Key source**:
   - **Method A (Custom Input)**: Type your API Key directly into the `api_key` text input box.
   - **Method B (Repository Secret)**: Leave the text box empty to automatically use your stored `GEMINI_API_KEY` repository secret.
3. Click **Run workflow**.
4. View the formatted table directly in the run Summary or download the reports as artifacts!

---

### Option 2: Local Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OSK0020/CHECK-GOOGLE-MODELS.git
   cd CHECK-GOOGLE-MODELS
   ```

2. **Run with your API Key**:
   
   *Via CLI argument*:
   ```bash
   python get_available_models.py YOUR_API_KEY_HERE
   ```

   *Or via `.env` file*:
   Create a `.env` file (see `.env.example`):
   ```env
   GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```
   ```bash
   python get_available_models.py
   ```

---

## 📋 Sample Output Report (`models_report.md`)

```markdown
# 📊 Google AI Studio Models Scan Report

**Scan Date & Time:** 2026-08-07 02:00:00

- **Total Models Tested:** 15
- **Total Open Models with Web Search (Search Grounding):** 4

### 💡 Recommended Models (OSINT / Web Search Enabled):
- `gemini-2.5-flash`
- `gemini-2.0-flash`

### 📋 Access Status & Permissions Details:
| Model Code Name | Actual Access Status (with Search) |
| :--- | :--- |
| `gemini-2.5-flash` | ✅ Open & Working (Web Search Enabled)! |
| `gemini-1.5-pro` | ⚠️ Free Tier Rate Limit Exceeded (429 Quota — Retry Later) |
| `gemini-ultra-experimental` | ❌ Access Denied / Requires Paid Billing (403 Forbidden) |
```

---

## 🛠️ Tech Stack & Dependencies

* **Python 3.11+**
* **`google-genai`**: Official, updated Google Gen AI Python SDK.
* **`python-dotenv`**: For safe local environment variable loading.
* **GitHub Actions**: For automated CI/CD cloud execution.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
