# סקריפט לשליפת כל המודלים הזמינים למשתמש ב-Google AI Studio
# מותאם להרצה ב-GitHub Actions תוך שימוש בסודות (Secrets)

import sys
import subprocess
import os

# 1. פונקציה להתקנת הספריות הדרושות אוטומטית (מותאם לספרייה החדשה)
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
# הקוד לא מכיל את המפתח עצמו, אלא מבקש אותו מהשרת בזמן ההרצה
API_KEY = os.environ.get("GEMINI_API_KEY")
# ==========================================

def fetch_my_models():
    """
    מתחבר ל-API של גוגל ומדפיס טבלה של כל המודלים הזמינים למפתח.
    """
    if not API_KEY:
        print("❌ שגיאה: לא נמצא מפתח API. יש לוודא שהסוד GEMINI_API_KEY מוגדר ב-GitHub.")
        return

    print("🔍 מתחבר לשרתי Google AI Studio...")
    print("📥 שולף את רשימת המודלים שפתוחים עבורך...\n")
    
    try:
        # התחברות עם הספרייה החדשה ומפתח ה-API החבוי
        client = genai.Client(api_key=API_KEY)
        
        # שליפת רשימת המודלים מהשרת
        models = client.models.list()
        
        # הדפסת כותרות הטבלה
        print(f"{'Model Code Name':<35} | {'Display Name':<25}")
        print("-" * 65)
        
        count = 0
        
        for m in models:
            # ניקוי השם להצגה נוחה יותר
            clean_name = m.name.replace("models/", "") if m.name else "Unknown"
            display_name = m.display_name if m.display_name else "N/A"
            
            # הדפסת שורת המודל
            print(f"{clean_name:<35} | {display_name:<25}")
            count += 1
            
        print("-" * 65)
        print(f"📊 סה\"כ מודלים בחשבון: {count}")
        print("\n💡 טיפ: העתק את השם מהעמודה השמאלית (Model Code Name) כדי להשתמש בו בקוד ה-OSINT שלך.")
        
    except Exception as e:
        print(f"\n❌ שגיאה בשליפת המודלים.")
        print(f"פרטי השגיאה: {e}")

if __name__ == "__main__":
    fetch_my_models()
