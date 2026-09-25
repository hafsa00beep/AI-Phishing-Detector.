import requests

# 1. مفتاح الـ API
API_KEY = "AQ.Ab8RN6JiSQdjn-jJHhoCJ9zQt0Ao4kyOoMv5x9LxCwniFv4dJw"

# رابط الـ API المباشر
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def analyze_phishing_email(email_text):
    prompt_text = f"""
    أنت خبير أمن سيبراني متخصص في كشف هجمات الصيد الاحتيالي (Phishing).
    قم بتحليل النص التالي بأسلوب تقني واحترافي:

    --- النص المراد فحصه ---
    {email_text}
    ------------------------

    المطلوب في التقرير:
    1. تقييم مستوى الخطر (منخفض - متوسط - مرتفع جداً) مع نسبة مئوية.
    2. المؤشرات المشبوهة (Suspicious Indicators).
    3. نوع الهجوم المحتمل.
    4. التوصية الأمنية المباشرة.
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    try:
        response = requests.post(URL, json=payload)
        result = response.json()
        
        # استخراج النتيجة
        report = result['candidates'][0]['content']['parts'][0]['text']
        print("\n================ 🛡️ تقرير الفحص السيبراني للشركات 🛡️ ================\n")
        print(report)
    except Exception as e:
        print("حدث خطأ أثناء الاتصال بالذكاء الاصطناعي:", e)

# --- تجربة فحص رسالة ---
if __name__ == "__main__":
    sample_email = """
    Dear Employee, 
    Your Office365 password will expire in 2 hours. 
    Please click on http://192.168.1.45/auth/login to keep your current password.
    Failure to do so will result in immediate suspension of your corporate account.
    IT Support Team.
    """
    analyze_phishing_email(sample_email)
