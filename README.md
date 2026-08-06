# 🤖 CHECK-GOOGLE-MODELS
> **סורק מודלים אקטיבי עבור Google AI Studio — בדיקה בלחיצת כפתור של הרשאות, עלויות ותמיכה בחיפוש בזמן אמת (Search Grounding).**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google GenAI SDK](https://img.shields.io/badge/SDK-google--genai-green.svg)](https://pypi.org/project/google-genai/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange.svg)](https://github.com/OSK0020/CHECK-GOOGLE-MODELS/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 הסיפור מאחורי הפרויקט — למה בניתי את זה?

כשהתחלתי לבנות בוטים ואוטומציות חכמות, רציתי להעניק להם **"מוח"** חזק שיוכל גם לחפש מידע עדכני ברשת בזמן אמת. 

אבל כשנכנסתי ל-**Google AI Studio**, הלכתי לאיבוד:
* ❓ אילו מודלים באמת פתוחים ונגישים בחשבון שלי?
* 💰 מה פתוח בחינם (Free Tier) ומה דורש מנוי בתשלום (Billing / 403 Forbidden)?
* ⚠️ אילו מודלים מוגבלים בגלל חריגת מכסה (Rate Limit / 429 Quota)?
* 🌐 ואולי הכי חשוב — **איזה מודל באמת תומך בחיפוש חופשי ברשת (Search Grounding)?**

רשימת המודלים הרשמית של גוגל מציגה מטא-דאטה יבשה, אך אינה מגלה מה עובד בפועל בחשבון הספציפי שלך. 
לכן בניתי את הפרויקט הזה: **הרצה יחידה בלחיצת כפתור**, המבוססת על מפתח API יחיד, שסורקת אקטיבית את כל המודלים ומפיקה דוח מפורט וברור!

---

## 🌟 תכונות מרכזיות

* ⚡ **הרצה אקטיבית (Search Grounding Test)**: הקוד אינו מסתפק ברשימה יבשה, אלא שולח בקשת אמת מול כל מודל יחד עם כלי החיפוש ברשת של גוגל (`types.Tool(google_search=types.GoogleSearch())`).
* 📊 **סיווג הרשאות ועלויות ברור**:
  * ✅ `פתוח ועובד בחשבון`: מודל נגיש ופעיל לשימוש (כולל במסלול החינמי).
  * ⚠️ `חריגת מכסה חינמית (429 Rate Limit)`: מודל זמין בחשבון שכרגע חרג ממגבלת הבקשות החינמית.
  * ❌ `חסום / מיועד למנוי בתשלום (403 Forbidden)`: מודל שחסום בחשבון חינמי ודורש הגדרת Billing.
  * ❌ `פתוח לטקסט בלבד`: מודל שיוצר טקסט אך אינו תומך בכלי ה-Search Grounding.
* 📝 **ייצוא דוחות אוטומטי במגוון פורמטים**:
  * **`models_report.md`**: דוח קריא ומעוצב ב-Markdown.
  * **`models_report.json`**: דוח מובנה לעיבוד בסקריפטים ומערכות אחרות.
  * **`GITHUB_STEP_SUMMARY`**: הצגת דוח ויזואלי בלשונית הסיכום ב-GitHub Actions.
* 🛡️ **תמיכה מלאה ב-Windows**: מנגנון Reconfigure UTF-8 מובנה המונע קריסות `UnicodeEncodeError`.

---

## 🚀 איך מריצים? (Quick Start)

### אפשרות 1: הרצה בלחיצת כפתור ב-GitHub (ללא התקנות!)

1. בצע Fork למאגר זה או העלה אותו לחשבון ה-GitHub שלך.
2. הגדר את מפתח ה-API שלך ב-GitHub Secrets:
   - היכנס ל-**Settings** -> **Secrets and variables** -> **Actions**.
   - לחץ על **New repository secret**.
   - שם הסוד: `GEMINI_API_KEY`, והזן את המפתח מ-Google AI Studio.
3. היכנס בלשונית **Actions** -> בחר ב-**Run Gemini Models Check** -> לחץ על **Run workflow**.
4. בסיום ההרצה תוכל לצפות בטבלה המעוצבת ישירות בדף הסיכום (Summary) ולהוריד את קובצי הדוחות כ-Artifact!

---

### אפשרות 2: הרצה מקומית במחשב (Local Run)

1. **שכפול המאגר**:
   ```bash
   git clone https://github.com/OSK0020/CHECK-GOOGLE-MODELS.git
   cd CHECK-GOOGLE-MODELS
   ```

2. **הגדרת מפתח API**:
   צור קובץ `.env` בתיקיית הפרויקט (ניתן להעתיק מ-`.env.example`):
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **הרצת הסקריפט**:
   ```bash
   python get_available_models.py
   ```

---

## 📋 דוגמה לפלט הדוח (`models_report.md`)

```markdown
# 📊 דוח סריקת מודלים ב-Google AI Studio

**תאריך סריקה:** 2026-08-07 02:00:00

- **סה"כ מודלים שנבדקו:** 15
- **סה"כ מודלים פתוחים עם חיפוש ברשת (Search Grounding):** 4

### 💡 מודלים מומלצים לעבודה (OSINT / Search Enabled):
- `gemini-2.5-flash`
- `gemini-2.0-flash`

### 📋 פירוט סטטוס נגישות לכל המודלים:
| Model Code Name | Actual Access Status (with Search) |
| :--- | :--- |
| `gemini-2.5-flash` | ✅ פתוח ועובד בחשבון (כולל חיפוש ברשת)! |
| `gemini-1.5-pro` | ⚠️ חריגת מכסה חינמית / עומס בקשות (429 Rate Limit) |
| `gemini-ultra-experimental` | ❌ חסום / מיועד למנוי בתשלום (403 Forbidden) |
```

---

## 🛠️ טכנולוגיות ותלויות

* **Python 3.11+**
* **`google-genai`**: ספריית ה-SDK הרשמית והמעודכנת של גוגל.
* **`python-dotenv`**: לטעינה מאובטחת של משתני סביבה.
* **GitHub Actions**: לאוטומציה והרצה בענן.

---

## 📜 רישיון (License)

פרויקט זה מופץ תחת רישיון MIT. ראה קובץ [LICENSE](LICENSE) לפרטים נוספים.
