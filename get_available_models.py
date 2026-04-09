# סקריפט לבדיקת הרשאות ממוקדת לרשימת מודלים ספציפית
# כולל השהייה ארוכה למניעת שגיאות 429 (Rate Limit)

import sys
import subprocess
import os
import time

# 1. התקנת הספריות הדרושות
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

# רשימת המודלים הספציפית שביקשת לבדוק
MODELS_TO_TEST = [
    "gemini-2.5-pro",
    "gemini-pro-latest",
    "gemini-3-pro-preview",
    "gemini-3.1-pro-preview",
    "gemini-3.1-pro-preview-customtools",
    "gemini-2.5-computer-use-preview-10-2025"
]

def test_specific_models():
    """
    מתחבר ל-API ומנסה לשלוח "Test" אך ורק למודלים שברשימה.
    """
    if not API_KEY:
        print("❌ שגיאה: לא נמצא מפתח API. יש לוודא שהסוד GEMINI_API_KEY מוגדר ב-GitHub.")
        return

    print("🔍 מתחבר לשרתי Google AI Studio...")
    
    try:
        client = genai.Client(api_key=API_KEY)
        
        print("📥 מתחיל סבב בדיקות אקטיבי למודלים הממוקדים...")
        print("⏳ שים לב: הסקריפט ימתין 15 שניות בין בדיקה לבדיקה כדי למנוע שגיאות 429 (עומס).\n")
        
        print(f"{'Model Code Name':<40} | {'Actual Access Status':<30}")
        print("-" * 75)
        
        working_models = []
        
        for model_name in MODELS_TO_TEST:
            try:
                # ניסיון אמיתי לשלוח בקשה למודל
                response = client.models.generate_content(
                    model=model_name,
                    contents="Hi, this is an automated access test. Reply 'OK'."
                )
                status = "✅ פתוח ועובד!"
                working_models.append(model_name)
                
            except Exception as e:
                error_str = str(e).lower()
                # סיווג השגיאות כדי שתבין למה המודל לא זמין
                if "403" in error_str or "permission denied" in error_str:
                    status = "❌ חסום לחשבון שלך (403)"
                elif "429" in error_str or "quota" in error_str:
                    status = "⚠️ עדיין חורג ממכסה/עומס (429)"
                elif "404" in error_str or "not found" in error_str:
                    status = "❌ לא קיים למפתח שלך (404)"
                elif "not supported" in error_str:
                    status = "❌ לא תומך בטקסט"
                else:
                    status = f"❌ שגיאה אחרת"

            print(f"{model_name:<40} | {status:<30}")
            
            # השהייה של 15 שניות כדי לא לעצבן את השרתים של גוגל
            time.sleep(15)
            
        print("-" * 75)
        print(f"📊 סה\"כ מודלים שנבדקו: {len(MODELS_TO_TEST)}")
        print(f"✅ מתוכם פתוחים וזמינים עבורך: {len(working_models)}")
        
    except Exception as e:
        print(f"\n❌ שגיאה בתהליך הבדיקה מול שרתי גוגל.")
        print(f"פרטי השגיאה: {e}")

if __name__ == "__main__":
    test_specific_models()
