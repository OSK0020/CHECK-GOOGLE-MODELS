# סקריפט לבדיקת הרשאות בפועל לכל המודלים ב-Google AI Studio
# הקוד לא רק מציג את הרשימה, אלא שולח בקשה לכל מודל כדי לוודא גישה אמיתית.

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

# ==========================================
# 2. משיכת ה-API Key מתוך הסודות (Secrets) של GitHub
API_KEY = os.environ.get("GEMINI_API_KEY")
# ==========================================

def test_my_models():
    """
    מתחבר ל-API, שולף את הרשימה, ומנסה לשלוח "Test" לכל מודל
    כדי לראות למי מהם יש לך באמת גישה חינמית/פתוחה.
    """
    if not API_KEY:
        print("❌ שגיאה: לא נמצא מפתח API. יש לוודא שהסוד GEMINI_API_KEY מוגדר ב-GitHub.")
        return

    print("🔍 מתחבר לשרתי Google AI Studio...")
    
    try:
        client = genai.Client(api_key=API_KEY)
        models = client.models.list()
        
        print("📥 שולף את הרשימה ומתחיל סבב בדיקות אקטיבי לכל מודל (זה ייקח כמה רגעים)...\n")
        
        print(f"{'Model Code Name':<35} | {'Actual Access Status':<30}")
        print("-" * 65)
        
        working_models = []
        
        for m in models:
            clean_name = m.name.replace("models/", "") if m.name else "Unknown"
            
            # בדיקה מקדימה: האם המודל מיועד בכלל ליצירת תוכן (טקסט)
            methods = getattr(m, 'supported_generation_methods', [])
            if methods and 'generateContent' not in methods:
                # מדלג על מודלים של חיפוש וקטורי/Embeddings שלא נועדו לשיחה
                continue
                
            try:
                # ניסיון אמיתי לשלוח בקשה למודל
                response = client.models.generate_content(
                    model=clean_name,
                    contents="Hi, this is an automated access test. Reply 'OK'."
                )
                status = "✅ פתוח ועובד!"
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
                elif "not supported" in error_str:
                    status = "❌ לא תומך בטקסט"
                else:
                    status = "❌ שגיאה (אולי המודל בעדכון)"

            print(f"{clean_name:<35} | {status:<30}")
            
            # השהייה קלה כדי לא לעבור את מגבלת הבקשות לדקה של API (Rate Limit)
            time.sleep(2)
            
        print("-" * 65)
        print(f"📊 סה\"כ מודלי טקסט שנבדקו: {len(working_models)} נמצאו כזמינים ופתוחים עבורך!")
        
        if working_models:
            print("\n💡 אלו המודלים שאתה יכול להעתיק ולהשתמש בהם בוודאות בקוד ה-OSINT שלך:")
            for wm in working_models:
                print(f"  - {wm}")
        
    except Exception as e:
        print(f"\n❌ שגיאה בתהליך הבדיקה מול שרתי גוגל.")
        print(f"פרטי השגיאה: {e}")

if __name__ == "__main__":
    test_my_models()
