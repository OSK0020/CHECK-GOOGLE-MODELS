# סקריפט לשליפת כל המודלים הזמינים למשתמש ב-Google AI Studio
# מותאם להרצה מקומית, ב-Colab, או להעלאה ל-GitHub

import sys
import subprocess

# 1. פונקציה להתקנת הספריות הדרושות אוטומטית (נוח מאוד למשתמשי קצה)
def install_requirements():
    try:
        import google.generativeai
    except ImportError:
        print("מתקין את ספריית google-generativeai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai", "-q"])
        print("ההתקנה הושלמה!\n")

install_requirements()

import google.generativeai as genai

# ==========================================
# 2. הגדרת מפתח ה-API
# מומלץ: אם אתה מעלה ל-GitHub הציבורי, *אל תשמור* את המפתח בקובץ.
# במקום זאת, תוכל להשתמש ב- os.environ.get('GEMINI_API_KEY') 
# אבל לצורך בדיקה פשוטה, שים אותו כאן:
API_KEY = "הכנס_כאן_את_מפתח_ה_API_שלך"
# ==========================================

def fetch_my_models():
    """
    מתחבר ל-API של גוגל ומדפיס טבלה של כל המודלים הזמינים למפתח.
    """
    if not API_KEY or API_KEY == "הכנס_כאן_את_מפתח_ה_API_שלך":
        print("❌ שגיאה: לא הוזן מפתח API. נא להזין את המפתח במשתנה API_KEY.")
        return

    # הגדרת מפתח הגישה
    genai.configure(api_key=API_KEY)
    
    print("🔍 מתחבר לשרתי Google AI Studio...")
    print("📥 שולף את רשימת המודלים שפתוחים עבורך...\n")
    
    try:
        # שליפת רשימת המודלים מהשרת
        models = genai.list_models()
        
        # הדפסת כותרות הטבלה
        # השתמשנו ביישור לשמאל (<) כדי שהאנגלית תסתדר טוב בקונסול
        print(f"{'Model Code Name (For API)':<35} | {'Display Name':<25} | {'Supports Text? (generateContent)'}")
        print("-" * 90)
        
        count = 0
        text_models_count = 0
        
        for m in models:
            # בדיקה אילו פעולות המודל תומך (חלקם מיועדים רק ל-Embeddings ולא ליצירת טקסט)
            supports_text = "generateContent" in m.supported_generation_methods
            
            if supports_text:
                status = "✅ Yes"
                text_models_count += 1
            else:
                status = "❌ No (Embeddings/Other)"
                
            # חיתוך המילה 'models/' מהשם כדי שיהיה קל יותר להעתיק לקוד שלנו
            clean_name = m.name.replace("models/", "")
            
            # הדפסת שורת המודל
            print(f"{clean_name:<35} | {m.display_name:<25} | {status}")
            count += 1
            
        print("-" * 90)
        print(f"📊 סה\"כ מודלים בחשבון: {count}")
        print(f"📝 מתוכם מודלים ליצירת טקסט/OSINT שניתן להשתמש בהם: {text_models_count}")
        print("\n💡 טיפ: העתק את השם מהעמודה השמאלית (Model Code Name) כדי להשתמש בו בקוד שלך.")
        
    except Exception as e:
        print(f"\n❌ שגיאה בשליפת המודלים. ודא שמפתח ה-API תקין.")
        print(f"פרטי השגיאה: {e}")

if __name__ == "__main__":
    fetch_my_models()
