# סקריפט לבדיקת הרשאות בפועל לכל המודלים ב-Google AI Studio
# הקוד מציג את הרשימה, מפעיל את כלי ה-Search Grounding,
# ומייצר דוח JSON וסיכום GitHub Step Summary במידה ורץ בענן.

import sys
import subprocess
import os
import time
import json

# הגדרת קידוד UTF-8 עבור stdout ו-stderr למניעת UnicodeEncodeError בסביבת Windows
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

# 1. פונקציה להתקנת הספריות הדרושות
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
        print(f"מתקין את הספריות החסרות: {', '.join(missing)}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing + ["-q"])
        print("ההתקנה הושלמה!\n")

install_requirements()

# טעינת משתני סביבה מקובץ .env מקומי (אם קיים)
try:
    import dotenv
    dotenv.load_dotenv()
except Exception:
    pass

from google import genai
from google.genai import types

# ייבוא מחלקת השגיאות מתוך SDK במידה וקיימת
try:
    from google.genai.errors import APIError
except ImportError:
    APIError = Exception

# ==========================================
# 2. משיכת ה-API Key מתוך משתני הסביבה
API_KEY = os.environ.get("GEMINI_API_KEY")
# ==========================================

def save_github_step_summary(working_models, all_results):
    """כותב סיכום מעוצב בפורמט Markdown ל-GitHub Step Summary בעת הרצה ב-GitHub Actions"""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return

    try:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("## 📊 Gemini Models & Search Grounding Status\n\n")
            f.write(f"**Total working models with web search:** {len(working_models)}\n\n")
            f.write("| Model Code Name | Access Status |\n")
            f.write("| :--- | :--- |\n")
            for item in all_results:
                f.write(f"| `{item['model']}` | {item['status']} |\n")

            if working_models:
                f.write("\n### 💡 Recommended Models for OSINT / Live Search:\n")
                for wm in working_models:
                    f.write(f"- `{wm}`\n")
    except Exception as e:
        print(f"⚠️ לא ניתן היה לכתוב ל-GITHUB_STEP_SUMMARY: {e}")

def test_my_models_with_tools():
    """
    מתחבר ל-API, שולף את הרשימה, ומנסה לשלוח שאלה עדכנית לכל מודל
    *תוך הפעלת כלי החיפוש (Google Search)*, כדי לגלות איזה מודל נתמך במלואו.
    """
    if not API_KEY:
        print("❌ שגיאה: לא נמצא מפתח API. יש לוודא שהמשתנה GEMINI_API_KEY מוגדר ב-env/GitHub Secrets.")
        return

    print("🔍 מתחבר לשרתי Google AI Studio...")
    
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
        
        print("📥 שולף את הרשימה ומתחיל סבב בדיקות עם כלי החיפוש (Search Grounding)...\n")
        
        print(f"{'Model Code Name':<35} | {'Actual Access Status (with Search)':<40}")
        print("-" * 78)
        
        working_models = []
        all_results = []
        
        for m in models:
            clean_name = m.name.replace("models/", "") if m.name else "Unknown"
            
            # בדיקה מקדימה: האם המודל מיועד בכלל ליצירת תוכן (טקסט)
            methods = getattr(m, 'supported_generation_methods', [])
            if methods and 'generateContent' not in methods:
                continue
                
            status = ""
            is_working = False
            
            try:
                # הפעלת כלי החיפוש מול המודל עם האובייקטים המוקלדים של SDK גוגל
                search_tool = types.Tool(google_search=types.GoogleSearch()) if hasattr(types, "GoogleSearch") else {"google_search": {}}
                response = client.models.generate_content(
                    model=clean_name,
                    contents="What is the current main news headline? Reply in 3 words.",
                    config=types.GenerateContentConfig(
                        tools=[search_tool]
                    )
                )
                status = "✅ פתוח ועובד (כולל גישה לרשת)!"
                working_models.append(clean_name)
                is_working = True
                
            except APIError as api_err:
                error_str = str(api_err).lower()
                if "403" in error_str or "permission denied" in error_str:
                    status = "❌ חסום לחשבון שלך (403)"
                elif "429" in error_str or "quota" in error_str:
                    status = "⚠️ חריגת מכסה / עומס (429)"
                elif "404" in error_str or "not found" in error_str:
                    status = "❌ לא קיים או הוסר (404)"
                elif "not supported" in error_str or "tool" in error_str:
                    status = "❌ הכלי (Search) לא נתמך במודל זה"
                else:
                    status = f"❌ שגיאת API ({api_err})"
            except Exception as e:
                error_str = str(e).lower()
                if "403" in error_str or "permission denied" in error_str:
                    status = "❌ חסום לחשבון שלך (403)"
                elif "429" in error_str or "quota" in error_str:
                    status = "⚠️ חריגת מכסה / עומס (429)"
                elif "404" in error_str or "not found" in error_str:
                    status = "❌ לא קיים או הוסר (404)"
                elif "not supported" in error_str or "tool" in error_str:
                    status = "❌ הכלי (Search) לא נתמך במודל זה"
                else:
                    status = "❌ שגיאה (אולי המודל בעדכון)"

            print(f"{clean_name:<35} | {status:<40}")
            all_results.append({
                "model": clean_name,
                "status": status,
                "is_working": is_working
            })
            
            # השהייה למניעת חריגת Rate Limit
            time.sleep(2)
            
        print("-" * 78)
        print(f"📊 סה\"כ מודלים שנבדקו והצליחו לחפש ברשת: {len(working_models)}")
        
        if working_models:
            print("\n💡 אלו המודלים המומלצים לעבודה עם כלי ה-OSINT (תומכים בחיפוש חופשי):")
            for wm in working_models:
                print(f"  - {wm}")

        # שמירת דוח JSON
        report_data["working_models_count"] = len(working_models)
        report_data["total_tested"] = len(all_results)
        report_data["working_models"] = working_models
        report_data["all_results"] = all_results
        
        with open("models_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print("\n💾 דוח תוצאות מובנה נשמר בהצלחה לקובץ `models_report.json`.")

        # שמירת דוח Markdown מעוצב וקריא
        with open("models_report.md", "w", encoding="utf-8") as f:
            f.write("# 📊 דוח סריקת מודלים ב-Google AI Studio\n\n")
            f.write(f"**תאריך סריקה:** {report_data['timestamp']}\n\n")
            f.write(f"- **סה\"כ מודלים שנבדקו:** {len(all_results)}\n")
            f.write(f"- **סה\"כ מודלים פתוחים עם חיפוש ברשת (Search Grounding):** {len(working_models)}\n\n")
            
            if working_models:
                f.write("### 💡 מודלים מומלצים לעבודה (OSINT / Search Enabled):\n")
                for wm in working_models:
                    f.write(f"- `{wm}`\n")
                f.write("\n")
                
            f.write("### 📋 פירוט סטטוס נגישות לכל המודלים:\n\n")
            f.write("| Model Code Name | Actual Access Status (with Search) |\n")
            f.write("| :--- | :--- |\n")
            for item in all_results:
                f.write(f"| `{item['model']}` | {item['status']} |\n")
        print("📝 דוח מעוצב בפורמט Markdown נשמר בהצלחה לקובץ `models_report.md`.")

        # שמירה ל-GitHub Step Summary במידה והורץ בענן
        save_github_step_summary(working_models, all_results)
        
    except Exception as e:
        print(f"\n❌ שגיאה בתהליך הבדיקה מול שרתי גוגל.")
        print(f"פרטי השגיאה: {e}")

if __name__ == "__main__":
    test_my_models_with_tools()
