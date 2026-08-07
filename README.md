# 🤖 CHECK-GOOGLE-MODELS
> **Active Model Scanner for Google AI Studio — 1-Click test for permissions, free/paid status, quotas, and real-time Web Search Grounding.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google GenAI SDK](https://img.shields.io/badge/SDK-google--genai-green.svg)](https://pypi.org/project/google-genai/)
[![Run Workflow 1-Click](https://img.shields.io/badge/CI%2FCD-Run%20Workflow%20(1--Click)-orange.svg)](https://github.com/OSK0020/CHECK-GOOGLE-MODELS/actions/workflows/manual_run.yml)
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

## 🧠 How to Make Your Bot Smart — Step-by-Step Guide

### Step 1: Open a Google AI Studio Account
1. Visit the official [Google AI Studio](https://aistudio.google.com/) portal.
2. Sign in with your Google account (no credit card required for Free Tier access).

---

### Step 2: Generate Your Google AI API Key
1. Click **"Get API key"** in the top navigation bar or left sidebar.
2. Click **"Create API key"** (choose a project or create a new default project).
3. Copy your newly generated API key string.

---

### Step 3: Connect Your API Key to This Repository

Choose **ONE** of the following options to connect your API Key:

#### 🟢 Option 1: Direct 1-Click Workflow Execution (Quickest)
👉 **[Click Here to Open the 1-Click Workflow Page Directly](https://github.com/OSK0020/CHECK-GOOGLE-MODELS/actions/workflows/manual_run.yml)**

1. Click the **Run workflow** dropdown button on the right side of the page.
2. **Choose your API Key source**:
   - **Method A (Custom Input)**: Paste your API Key directly into the **`api_key`** text input box.
   - **Method B (Repository Secret)**: Leave the text box empty to use your stored `GEMINI_API_KEY` repository secret.
3. Click the green **Run workflow** button.
4. View the formatted table directly in the run Summary or download the reports as artifacts!

> 🔒 *Security Note: Custom API Keys entered in the text box are automatically masked (`***`) in GitHub Action logs.*

---

#### 🔵 Option 2: Store as GitHub Repository Secret (Permanent & Recommended)
1. In your GitHub repository, navigate to **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret**.
3. **Exact Secret Name Required**: Enter `GEMINI_API_KEY` (must match the code exact name!).
4. **Secret Value**: Paste your API Key.
5. Click **Add secret**.
6. Now you can run the [1-Click Workflow](https://github.com/OSK0020/CHECK-GOOGLE-MODELS/actions/workflows/manual_run.yml) anytime without re-entering your key!

---

#### 🟡 Option 3: Local Execution on Your Computer
* **Via Command Line Argument**:
  ```bash
  python get_available_models.py YOUR_API_KEY_HERE
  ```
* **Via `.env` File**:
  Create a `.env` file in the project root containing:
  ```env
  GEMINI_API_KEY=YOUR_API_KEY_HERE
  ```
  Then run:
  ```bash
  python get_available_models.py
  ```

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
