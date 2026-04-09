# סקריפט לבדיקת הרשאות בפועל לכל המודלים ב-Google AI Studio
# הקוד לא רק מציג את הרשימה, אלא מפעיל את כלי ה-Search Grounding
# כדי לראות למי יש גישה פתוחה לאינטרנט בחשבון שלך.

import sys
import subprocess
import os
import time

# 1. פונקציה להתקנת הספריות הדרושות
def install_requirements():
    try:
        import google.genai
    except ImportError:
        print("מתקין את ספריית google-genai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "-q"])
        print("ההתקנה הושלמה!\n")

install_requirements()

from google import genai
# ייבוא האובייקטים הנדרשים להפעלת כלים (Tools)
from google.genai import types

# ==========================================
# 2. משיכת ה-API Key מתוך הסודות (Secrets) של GitHub
API_KEY = os.environ.get("GEMINI_API_KEY")
# ==========================================

def test_my_models_with_tools():
    """
    מתחבר ל-API, שולף את הרשימה, ומנסה לשלוח שאלה עדכנית לכל מודל
    *תוך הפעלת כלי החיפוש (Google Search)*, כדי לגלות איזה מודל נתמך במלואו.
    """
    if not API_KEY:
        print("❌ שגיאה: לא נמצא מפתח API. יש לוודא שהסוד GEMINI_API_KEY מוגדר ב-GitHub.")
        return

    print("🔍 מתחבר לשרתי Google AI Studio...")
    
    try:
        client = genai.Client(api_key=API_KEY)
        models = client.models.list()
        
        print("📥 שולף את הרשימה ומתחיל סבב בדיקות עם כלי החיפוש (Search Grounding)...\n")
        
        print(f"{'Model Code Name':<35} | {'Actual Access Status (with Search)':<40}")
        print("-" * 78)
        
        working_models = []
        
        for m in models:
            clean_name = m.name.replace("models/", "") if m.name else "Unknown"
            
            # בדיקה מקדימה: האם המודל מיועד בכלל ליצירת תוכן (טקסט)
            methods = getattr(m, 'supported_generation_methods', [])
            if methods and 'generateContent' not in methods:
                continue
                
            try:
                # הדרך להפעיל את הכלים בספרייה החדשה
                response = client.models.generate_content(
                    model=clean_name,
                    contents="What is the current main news headline? Reply in 3 words.",
                    config=types.GenerateContentConfig(
                        # הפעלת כלי החיפוש של גוגל!
                        tools=[{"google_search": {}}]
                    )
                )
                status = "✅ פתוח ועובד (כולל גישה לרשת)!"
                working_models.append(clean_name)
                
            except Exception as e:
                error_str = str(e).lower()
                # סיווג השגיאות כדי שתבין למה המודל לא זמין
                if "403" in error_str or "permission denied" in error_str:
                    status = "❌ חסום לחשבון שלך (403)"
                elif "429" in error_str or "quota" in error_str:
                    status = "⚠️ חריגת מכסה / עומס (429)"
                elif "404" in error_str or "not found" in error_str:
                    status = "❌ לא קיים או הוסר (404)"
                elif "not supported" in error_str or "tool" in error_str:
                    # כאן אנחנו תופסים מודלים שפתוחים לטקסט אבל חסומים לחיפוש
                    status = "❌ הכלי (Search) לא נתמך במודל זה"
                else:
                    status = "❌ שגיאה (אולי המודל בעדכון)"

            print(f"{clean_name:<35} | {status:<40}")
            
            # השהייה כדי לא לעבור את מגבלת הבקשות לדקה של API (Rate Limit)
            time.sleep(2)
            
        print("-" * 78)
        print(f"📊 סה\"כ מודלים שנבדקו והצליחו לחפש ברשת: {len(working_models)}")
        
        if working_models:
            print("\n💡 אלו המודלים המומלצים לעבודה עם כלי ה-OSINT (תומכים בחיפוש חופשי):")
            for wm in working_models:
                print(f"  - {wm}")
        
    except Exception as e:
        print(f"\n❌ שגיאה בתהליך הבדיקה מול שרתי גוגל.")
        print(f"פרטי השגיאה: {e}")

if __name__ == "__main__":
    test_my_models_with_tools()
