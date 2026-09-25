import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. إعدادات الصفحة والألوان (Burgundy & Beige Theme) ---
st.set_page_config(
    page_title="AI Threat & Phishing Scanner",
    page_icon="🛡️",
    layout="centered"
)

# تطبيق ألوان البرغندي والبيج عبر Custom CSS
st.markdown("""
    <style>
    /* خلفية الصفحة لون بيج ناعم */
    .stApp {
        background-color: #FDFBF7;
        color: #2C2C2C;
    }
    /* العناوين باللون البرغندي */
    h1, h2, h3, h4 {
        color: #800020 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* الأزرار باللون البرغندي مع كتابة بيج */
    .stButton>button {
        background-color: #800020 !important;
        color: #FDFBF7 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #600018 !important;
        color: #FFFFFF !important;
    }
    /* كروت وصناديق الإدخال */
    .stTextArea, .stFileUploader {
        background-color: #F5F0EB;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_length=True)

# --- 2. إعداد مفتاح API ---
API_KEY = "AQ.Ab8RN6JiSQdjn-jJHhoCJ9zQt0Ao4kyOoMv5x9LxCwniFv4dJw"
genai.configure(api_key=API_KEY)

# --- 3. واجهة المستخدم (UI) ---
st.title("🛡️ مٌحلل التهديدات ومكافحة الصيد الاحتيالي")
st.subheader("AI Phishing & Malicious Image Scanner")
st.write("افحص الإيميلات والروابط المشبوهة أو ارفع **صورة (Screenshot)** للرسالة خوفاً من فتح اللينكات الخبيثة.")

st.markdown("---")

# اختيار طريقة الفحص
option = st.radio("اختر طريقة الفحص / Select Analysis Method:", ("نص / إيميل / رابط (Text/URL)", "رفع صورة / سكرين شوت (Screenshot)"))

report_result = ""

if option == "نص / إيميل / رابط (Text/URL)":
    email_input = st.text_area("أدخل نص الإيميل أو الرابط المشبوه هنا:", height=150, placeholder="ضع النص أو اللينك المشبوه هنا...")
    
    if st.button("🔍 فحص النص والروابط"):
        if email_input.strip():
            with st.spinner("جاري تحليل النص والروابط بواسطة الذكاء الاصطناعي..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"""
                    أنت خبير أمن سيبراني متخصص في كشف هجمات الصيد الاحتيالي (Phishing).
                    قم بتحليل النص والروابط التالية بأسلوب تقني واحترافي باللغة العربية والإنجليزي:
                    
                    النص المراد فحصه:
                    {email_input}
                    
                    المطلوب في التقرير:
                    1. تقييم مستوى الخطر (منخفض - متوسط - مرتفع جداً) مع نسبة الثقة.
                    2. المؤشرات المشبوهة والروابط الخبيثة المعقدة.
                    3. التوصية الأمنية المباشرة للمستخدم.
                    """
                    response = model.generate_content(prompt)
                    report_result = response.text
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
        else:
            st.warning("رجاءً أدخل نصاً أو رابطاً للفحص.")

else:
    uploaded_file = st.file_uploader("قم برفع صورة الإيميل أو الرسالة المشبوهة (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة للفحص", use_column_width=True)
        
        if st.button("🚨 فحص الصورة واستخراج التهديدات"):
            with st.spinner("جاري قراءة الصورة وتحليل المحتوى الأمني..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = """
                    أنت خبير أمن سيبراني. قم بقراءة وتحليل الصورة المرفقة (سواء كانت سكرين شوت لإيميل أو موقع أو رسالة نصية):
                    1. حدد هل تحتوي الصورة على محاولة صيد احتيالي (Phishing) أو روابط مزيفة أنشأها الهكرز؟
                    2. استخرج العناوين والروابط الظاهرة وتقييم مدى خطورتها.
                    3. حدد مستوى الخطر المباشر (Low, Medium, Critical).
                    4. قدم قدم نصيحة أمان فورية للمستخدم.
                    """
                    response = model.generate_content([prompt, image])
                    report_result = response.text
                except Exception as e:
                    st.error(f"حدث خطأ أثناء فحص الصورة: {e}")

# عرض التقرير إن وجد
if report_result:
    st.markdown("---")
    st.markdown("### 📊 تقرير التحليل الأمني (Security Report)")
    st.info(report_result)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #800020;'>Developed by <b>Hafsa Hussein</b> — Defensive AI & Cybersecurity Specialist</p>", unsafe_allow_html=True)
