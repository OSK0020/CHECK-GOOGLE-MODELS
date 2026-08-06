# Script for checking real-time permissions, free/paid status, and Search Grounding
# capabilities for all models in Google AI Studio.
#
# Generates structured console output, 'models_report.json', 'models_report.md',
# and GitHub Step Summary when executed in CI/CD pipelines.

import sys
import subprocess
import os
import time
import json

# Reconfigure stdout/stderr encoding to UTF-8 to prevent Windows console encoding crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 1. Automatic dependency checker & installer
def install_requirements():
    missing = []
    try:
        import google.genai
    except ImportError:
        missing.append("google-genai")
    try:
        import dotenv
    except ImportError:
        missing.append("python-dotenv")

    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing + ["-q"])
        print("Installation complete!\n")

install_requirements()

# Load environment variables from local .env file if present
try:
    import dotenv
    dotenv.load_dotenv()
except Exception:
    pass

from google import genai
from google.genai import types

# Import API error class if available from SDK
try:
    from google.genai.errors import APIError
except ImportError:
    APIError = Exception

# ==========================================
# 2. Retrieve API Key from environment
API_KEY = os.environ.get("GEMINI_API_KEY")
# ==========================================

def save_github_step_summary(working_models, all_results):
    """Writes a formatted Markdown summary table to GITHUB_STEP_SUMMARY when running in GitHub Actions."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return

    try:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("## 📊 Gemini Models & Search Grounding Status Report\n\n")
            f.write(f"**Total Working Models (Web Search Enabled):** {len(working_models)}\n\n")
            f.write("| Model Code Name | Actual Access Status (with Search) |\n")
            f.write("| :--- | :--- |\n")
            for item in all_results:
                f.write(f"| `{item['model']}` | {item['status']} |\n")

            if working_models:
                f.write("\n### 💡 Recommended Models for OSINT / Live Search:\n")
                for wm in working_models:
                    f.write(f"- `{wm}`\n")
    except Exception as e:
        print(f"⚠️ Could not write to GITHUB_STEP_SUMMARY: {e}")

def test_my_models_with_tools():
    """
    Connects to Google AI Studio API, lists all available models, and actively tests
    each text model with the Google Search Grounding tool enabled to verify actual permissions.
    """
    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY environment variable not found.")
        print("   Please set GEMINI_API_KEY in your .env file or GitHub Secrets.")
        return

    print("🔍 Connecting to Google AI Studio servers...")
    
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "working_models_count": 0,
        "total_tested": 0,
        "working_models": [],
        "all_results": []
    }
    
    try:
        client = genai.Client(api_key=API_KEY)
        models = client.models.list()
        
        print("📥 Retrieving models list and testing Search Grounding capabilities...\n")
        
        print(f"{'Model Code Name':<35} | {'Actual Access Status (with Search)':<45}")
        print("-" * 83)
        
        working_models = []
        all_results = []
        
        for m in models:
            clean_name = m.name.replace("models/", "") if m.name else "Unknown"
            
            # Filter: Check if the model supports text content generation
            methods = getattr(m, 'supported_generation_methods', [])
            if methods and 'generateContent' not in methods:
                continue
                
            status = ""
            is_working = False
            
            try:
                # Configure Google Search tool using official typed SDK objects
                search_tool = types.Tool(google_search=types.GoogleSearch()) if hasattr(types, "GoogleSearch") else {"google_search": {}}
                response = client.models.generate_content(
                    model=clean_name,
                    contents="What is the current main news headline? Reply in 3 words.",
                    config=types.GenerateContentConfig(
                        tools=[search_tool]
                    )
                )
                status = "✅ Open & Working (Web Search Enabled)!"
                working_models.append(clean_name)
                is_working = True
                
            except APIError as api_err:
                error_str = str(api_err).lower()
                if "403" in error_str or "permission denied" in error_str:
                    status = "❌ Access Denied / Requires Paid Billing (403 Forbidden)"
                elif "429" in error_str or "quota" in error_str:
                    status = "⚠️ Free Tier Rate Limit / Quota Exceeded (429 Rate Limit)"
                elif "404" in error_str or "not found" in error_str:
                    status = "❌ Model Removed or Not Found (404 Not Found)"
                elif "not supported" in error_str or "tool" in error_str:
                    status = "❌ Open for Text Generation Only (Web Search Not Supported)"
                else:
                    status = f"❌ API Error ({api_err})"
            except Exception as e:
                error_str = str(e).lower()
                if "403" in error_str or "permission denied" in error_str:
                    status = "❌ Access Denied / Requires Paid Billing (403 Forbidden)"
                elif "429" in error_str or "quota" in error_str:
                    status = "⚠️ Free Tier Rate Limit / Quota Exceeded (429 Rate Limit)"
                elif "404" in error_str or "not found" in error_str:
                    status = "❌ Model Removed or Not Found (404 Not Found)"
                elif "not supported" in error_str or "tool" in error_str:
                    status = "❌ Open for Text Generation Only (Web Search Not Supported)"
                else:
                    status = "❌ General Error (Model under maintenance or updating)"

            print(f"{clean_name:<35} | {status:<45}")
            all_results.append({
                "model": clean_name,
                "status": status,
                "is_working": is_working
            })
            
            # Delay to avoid API rate limit restrictions
            time.sleep(2)
            
        print("-" * 83)
        print(f"📊 Total models tested with Web Search support: {len(working_models)}")
        
        if working_models:
            print("\n💡 Recommended models for OSINT / Live Search tasks:")
            for wm in working_models:
                print(f"  - {wm}")

        # Save structured JSON report
        report_data["working_models_count"] = len(working_models)
        report_data["total_tested"] = len(all_results)
        report_data["working_models"] = working_models
        report_data["all_results"] = all_results
        
        with open("models_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print("\n💾 Structured JSON report saved to 'models_report.json'.")

        # Save clean formatted Markdown report
        with open("models_report.md", "w", encoding="utf-8") as f:
            f.write("# 📊 Google AI Studio Models Scan Report\n\n")
            f.write(f"**Scan Date & Time:** {report_data['timestamp']}\n\n")
            f.write(f"- **Total Models Tested:** {len(all_results)}\n")
            f.write(f"- **Total Open Models with Web Search (Search Grounding):** {len(working_models)}\n\n")
            
            if working_models:
                f.write("### 💡 Recommended Models (OSINT / Web Search Enabled):\n")
                for wm in working_models:
                    f.write(f"- `{wm}`\n")
                f.write("\n")
                
            f.write("### 📋 Access Status & Permissions Details:\n\n")
            f.write("| Model Code Name | Actual Access Status (with Search) |\n")
            f.write("| :--- | :--- |\n")
            for item in all_results:
                f.write(f"| `{item['model']}` | {item['status']} |\n")
        print("📝 Formatted Markdown report saved to 'models_report.md'.")

        # Save to GitHub Step Summary if running in CI/CD pipeline
        save_github_step_summary(working_models, all_results)
        
    except Exception as e:
        print(f"\n❌ Error during model scanning process.")
        print(f"Error Details: {e}")

if __name__ == "__main__":
    test_my_models_with_tools()
