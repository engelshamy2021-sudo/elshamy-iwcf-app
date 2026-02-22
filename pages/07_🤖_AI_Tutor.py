import streamlit as st
from datetime import datetime
import time
import random

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Tutor - Elshamy IWCF",
    page_icon="🤖",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 ENHANCED CSS (من الكود الجديد + القديم)
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main theme */
    :root {
        --primary: #8B5CF6;
        --secondary: #3B82F6;
        --success: #10B981;
        --warning: #F59E0B;
    }
    
    /* Header */
    .tutor-header {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        animation: slideDown 0.5s ease;
    }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* User Message */
    .user-message {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 5px 18px;
        margin: 1rem 0;
        margin-left: auto;
        max-width: 75%;
        border-left: 4px solid #3B82F6;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    /* AI Message */
    .ai-message {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 5px;
        margin: 1rem 0;
        max-width: 75%;
        border-left: 4px solid #10B981;
        animation: slideInLeft 0.3s ease;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
    
    /* Typing Indicator */
    .typing-indicator {
        background: #F3F4F6;
        padding: 1rem 1.5rem;
        border-radius: 18px;
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6B7280;
        margin: 0 3px;
        animation: bounce 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    /* Suggestion Chips */
    .suggestion-chip {
        background: white;
        border: 2px solid #E5E7EB;
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .suggestion-chip:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        border-color: #8B5CF6;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #F59E0B;
        margin: 1rem 0;
    }
    
    /* Stats Card */
    .stat-card {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        border-left: 4px solid var(--primary);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    /* Related Topics Badge */
    .related-badge {
        background: #EDE9FE;
        color: #7C3AED;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.5;
        }
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #F3F4F6;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #8B5CF6;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #7C3AED;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📚 ENHANCED KNOWLEDGE BASE (من كودك + إضافات)
# ═══════════════════════════════════════════════════════

KNOWLEDGE_BASE = {
    "hydrostatic pressure": {
        "answer": """
**🎯 Hydrostatic Pressure (HP)** هو الضغط الناتج عن وزن عمود السائل الساكن.

**📐 المعادلة الأساسية:**
HP = 0.052 × MW × TVD



**حيث:**
- **HP** = Hydrostatic Pressure (psi)
- **MW** = Mud Weight (ppg)
- **TVD** = True Vertical Depth (ft)
- **0.052** = ثابت التحويل

**📊 مثال عملي:**
المعطيات:

Mud Weight = 10 ppg
TVD = 5,000 ft
الحل:
HP = 0.052 × 10 × 5,000
HP = 2,600 psi



**💡 نصيحة سريعة:**
للحساب السريع: اضرب العمق في **0.52** للطين 10 ppg

**⚠️ ملاحظات مهمة:**
1. استخدم **TVD** وليس **MD** (Measured Depth)
2. تأكد من وحدات القياس
3. الضغط الهيدروستاتيكي يزيد بزيادة العمق أو كثافة الطين

**🔄 صيغ بديلة:**
- بالـ **bar**: HP = 0.00981 × MW × TVD
- بالـ **kPa**: HP = 0.0981 × MW × TVD
        """,
        "related": ["formation pressure", "mud weight", "kill mud weight", "pressure gradient"],
        "category": "Calculations"
    },
    
    "kill mud weight": {
        "answer": """
**🎯 Kill Mud Weight (KMW)** هو وزن الطين المطلوب لقتل البئر بأمان.

**📐 المعادلة:**
KMW = (SIDPP ÷ (0.052 × TVD)) + OMW



**حيث:**
- **KMW** = Kill Mud Weight (ppg)
- **SIDPP** = Shut-In Drill Pipe Pressure (psi)
- **TVD** = True Vertical Depth (ft)
- **OMW** = Original Mud Weight (ppg)

**📊 مثال عملي:**
المعطيات:

SIDPP = 500 psi
TVD = 10,000 ft
OMW = 10 ppg
الحل:
KMW = (500 ÷ (0.052 × 10,000)) + 10
KMW = (500 ÷ 520) + 10
KMW = 0.96 + 10
KMW = 10.96 ppg



**✅ Round up to: 11 ppg**

**⚠️ أخطاء شائعة:**
1. ❌ نسيان إضافة OMW في النهاية
2. ❌ استخدام MD بدلاً من TVD
3. ❌ عدم التقريب لأعلى

**🛡️ Safety Margin:**
يُنصح بإضافة 0.5 ppg للأمان:
KMW (Final) = 11 + 0.5 = 11.5 ppg



**💡 تذكر:**
- KMW دائماً أكبر من OMW
- استخدم الآلة الحاسبة للتأكد
- راجع الحسابات مرتين
        """,
        "related": ["icp", "fcp", "formation pressure", "sidpp"],
        "category": "Calculations"
    },
    
    "kick": {
        "answer": """
**⚠️ Kick** هو دخول سوائل التكوين (نفط/غاز/ماء) إلى البئر بشكل غير مخطط له.

**🔍 الأسباب الرئيسية:**

1. **Underbalanced Condition**
   - ضغط الطين أقل من ضغط التكوين
   - السبب الأكثر شيوعاً

2. **Swabbing**
   - سحب الطين أثناء رفع الأنابيب
   - يحدث عند السحب السريع

3. **Lost Circulation**
   - فقدان الطين في التكوين
   - يقلل الضغط الهيدروستاتيكي

4. **Insufficient Mud Weight**
   - عدم كفاية كثافة الطين
   - خطأ في الحسابات

**📊 علامات الـ Kick (مهم جداً!):**

✅ **Primary Signs:**
- **Pit Gain** - زيادة في حجم الطين
- **Flow Rate Increase** - زيادة معدل التدفق
- **Flow with Pumps Off** - تدفق والمضخات متوقفة

✅ **Secondary Signs:**
- **Pump Pressure Decrease** - انخفاض ضغط المضخة
- **Drilling Break** - زيادة سرعة الحفر
- **Cut Mud** - تغير خواص الطين
- **Gas in Mud** - ظهور غاز في الطين

**🚨 الإجراء الفوري (Critical!):**

**خلال 30 ثانية:**
1. ⏸️ **Stop Pumping** - أوقف الضخ فوراً
2. ⬆️ **Pick Up Off Bottom** - ارفع الريشة عن القاع
3. 🔒 **Shut-In the Well** - أغلق البئر
   - Close Annular BOP أولاً
   - أو استخدم Pipe Rams
4. 📊 **Record Pressures** - سجل الضغوط:
   - **SIDPP** (Shut-In Drill Pipe Pressure)
   - **SICP** (Shut-In Casing Pressure)
5. 📢 **Notify Supervisor** - أبلغ المسؤول فوراً

**💡 القاعدة الذهبية:**
> "The faster you detect a kick, the easier it is to control!"

**⚠️ تحذيرات:**
- لا تتأخر في الإغلاق
- لا تحاول "تخفيف" الموقف
- اتبع الإجراءات بدقة
        """,
        "related": ["shut-in", "well control", "kill methods", "sidpp", "sicp"],
        "category": "Well Control"
    },
    
    "driller's method": {
        "answer": """
**🎯 Driller's Method** - طريقة قتل البئر بدورتين منفصلتين.

**📋 الخطوات التفصيلية:**

**🔄 Circulation #1 - Kick Removal:**

1️⃣ **Calculate ICP:**
ICP = SIDPP + SCR



2️⃣ **Start Circulation:**
   - استخدم **Original Mud Weight**
   - ابدأ الضخ ببطء
   - حافظ على الضغط = **ICP**

3️⃣ **Circulate Out Kick:**
   - اخرج سائل الـ Kick من البئر
   - راقب الضغط باستمرار
   - خفض الضغط تدريجياً للصفر

4️⃣ **Check Success:**
   - الضغط يجب أن يصل للصفر
   - إذا لم يصل = Kick لم يخرج كاملاً

**🔄 Circulation #2 - Kill Mud Weight:**

5️⃣ **Prepare Kill Mud:**
   - احسب **KMW** (Kill Mud Weight)
   - حضر الطين الثقيل

6️⃣ **Calculate FCP:**
FCP = SCR × (KMW ÷ OMW)



7️⃣ **Start Second Circulation:**
   - ابدأ الضخ بـ Kill Mud
   - الضغط البداية = **ICP** (مرة أخرى)
   - خفض الضغط من ICP إلى FCP

8️⃣ **Kill Mud at Bit:**
   - عندما يصل KMW للريشة
   - الضغط يجب أن يكون = **FCP**

9️⃣ **Complete Circulation:**
   - استمر بالضخ حتى يملأ KMW البئر
   - حافظ على الضغط = **FCP**

🔟 **Final Check:**
   - أوقف الضخ
   - أغلق البئر
   - الضغط يجب أن يكون **صفر**
   - ✅ البئر مقتول!

**✅ المميزات:**
- ✅ بسيطة وسهلة التطبيق
- ✅ لا تحتاج انتظار تحضير KMW
- ✅ مناسبة للمبتدئين
- ✅ أقل احتمال للأخطاء

**❌ العيوب:**
- ❌ تحتاج دورتين (وقت أطول)
- ❌ تعرض أطول للضغط على التكوين
- ❌ استهلاك أكبر للوقت والموارد

**💡 متى تستخدم:**
- عند عدم وجود KMW جاهز
- مع أطقم قليلة الخبرة
- في الحالات البسيطة

**⚠️ نصائح مهمة:**
1. سجل كل القراءات
2. راقب Pit Level باستمرار
3. لا تتعجل في الضخ
4. اتبع Pressure Schedule
        """,
        "related": ["wait and weight", "icp", "fcp", "kill methods", "scr"],
        "category": "Kill Methods"
    },
    
    "wait and weight": {
        "answer": """
**🎯 Wait & Weight Method** - طريقة قتل البئر بدورة واحدة فقط.

**📋 الخطوات:**

**⏱️ Phase 1 - Wait (الانتظار):**

1️⃣ **Shut-in the Well:**
   - أغلق البئر فوراً
   - سجل **SIDPP** و **SICP**

2️⃣ **Calculate KMW:**
KMW = (SIDPP ÷ (0.052 × TVD)) + OMW



3️⃣ **Prepare Kill Mud:**
   - حضر الطين الثقيل
   - تأكد من الكثافة الصحيحة
   - ⏰ هذا يأخذ وقت (Wait!)

4️⃣ **Calculate Pressures:**
ICP = SIDPP + SCR
FCP = SCR × (KMW ÷ OMW)



**⚖️ Phase 2 - Weight (الوزن):**

5️⃣ **Start Circulation:**
   - ابدأ الضخ بـ **Kill Mud** مباشرة
   - الضغط البداية = **ICP**

6️⃣ **Follow Pressure Schedule:**
   - خفض الضغط من **ICP** إلى **FCP**
   - حسب جدول الضغط المحسوب

7️⃣ **KMW at Bit:**
   - عندما يصل KMW للريشة
   - الضغط = **FCP**

8️⃣ **Complete Circulation:**
   - استمر حتى يملأ KMW البئر كله
   - حافظ على **FCP** ثابت

9️⃣ **Final Check:**
   - أوقف الضخ وأغلق البئر
   - الضغط = **صفر** ✅

**✅ المميزات:**
- ✅ دورة واحدة فقط (أسرع)
- ✅ وقت أقل تحت الضغط
- ✅ تكلفة أقل
- ✅ أكثر كفاءة

**❌ العيوب:**
- ❌ تحتاج انتظار تحضير KMW
- ❌ تحتاج خبرة أكثر
- ❌ حسابات أكثر تعقيداً
- ❌ أخطاء محتملة أكبر

**💡 متى تستخدم:**
- عند توفر معدات خلط سريعة
- مع أطقم ذات خبرة عالية
- عند الحاجة للسرعة
- في الحالات المعقدة

**⚠️ نصائح:**
1. تأكد من KMW الصحيح قبل البدء
2. اتبع Pressure Schedule بدقة
3. لا تبدأ قبل جاهزية الطين
4. راقب Pit Level باستمرار

**📊 مقارنة الوقت:**
- Driller's Method: ~4 ساعات
- Wait & Weight: ~2-3 ساعات
        """,
        "related": ["driller's method", "icp", "fcp", "kill mud weight"],
        "category": "Kill Methods"
    },
    
    "bop": {
        "answer": """
**🛡️ BOP (Blowout Preventer)** - نظام السلامة الرئيسي للبئر.

**🏗️ المكونات الرئيسية:**

**1️⃣ Annular Preventer (الحلقي):**
الموقع: أعلى BOP Stack
الوظيفة: الإغلاق حول أي شكل



**المميزات:**
- ✅ يغلق على أي حجم من الأنابيب
- ✅ يغلق على Kelly, Tool Joints
- ✅ يمكن الحفر من خلاله (Stripping)
- ✅ مرن ويتكيف

**المواصفات:**
- Working Pressure: 3,000 - 5,000 psi
- يستخدم Rubber Packing Element
- أول خط دفاع

**2️⃣ Ram Preventers (الكباش):**

**🔹 Pipe Rams:**
الوظيفة: إغلاق على مقاس محدد من الأنابيب


- ✅ أقوى من Annular
- ✅ Working Pressure: 10,000 - 15,000 psi
- ✅ خاص بكل حجم أنبوب
- ⚠️ لا يغلق إلا على الحجم المحدد

**🔹 Blind Rams:**
الوظيفة: إغلاق البئر بالكامل (بدون أنابيب)


- ✅ يستخدم عند البئر الفارغ
- ✅ إغلاق كامل محكم
- ✅ للطوارئ

**🔹 Shear Rams:**
الوظيفة: قطع وإغلاق الأنابيب


- ⚠️ آخر خيار (Emergency!)
- ✅ قوة قطع عالية جداً
- ✅ يقطع Drill Pipe ويغلق
- ❌ يُستخدم فقط في الطوارئ القصوى

**🔹 Variable Bore Rams (VBR):**
الوظيفة: التكيف مع أحجام مختلفة


- ✅ يغلق على range من الأحجام
- ✅ أكثر مرونة من Pipe Rams
- ✅ يقلل عدد الـ Rams المطلوبة

**3️⃣ Choke & Kill Manifold:**
الوظيفة: التحكم في التدفق والضخ



**Choke Line:**
- لخروج السوائل من البئر
- يحتوي على Choke للتحكم بالضغط
- مهم جداً في Well Control

**Kill Line:**
- لضخ Kill Mud للبئر
- bypass للـ standpipe
- يُستخدم في عمليات القتل

**4️⃣ Inside BOP (Kelly Cock):**
الموقع: داخل Drill String
الوظيفة: منع التدفق العكسي


- ✅ يُركب على Kelly
- ✅ حماية من Back Flow
- ✅ يمكن تشغيله بسرعة

**📋 الاختبارات المطلوبة:**

**1. Function Test:**
- 📅 كل **14 يوم**
- اختبار تشغيل جميع المكونات
- بدون ضغط

**2. Pressure Test:**
- 📅 كل **21 يوم**
- 📅 بعد التركيب
- 📅 بعد أي صيانة
- اختبار تحمل الضغط

**ضغوط الاختبار:**
Annular: 70% من Rated Pressure
Rams: 100% من Rated Pressure
Low Pressure: 250-500 psi
High Pressure: حسب العمق


**⚠️ CRITICAL RULES:**

1. ✅ اختبر قبل كل عملية حفر
2. ✅ سجل جميع الاختبارات
3. ✅ لا تحفر مع BOP معطل
4. ✅ يجب وجود backup لكل مكون
5. ✅ تدريب الطاقم على الاستخدام

**🚨 Emergency Procedures:**

**في حالة Kick:**
1. Close Annular (أسرع)
2. إذا فشل → Close Pipe Rams
3. إذا فشل → Close Blind Rams
4. Last Resort → Shear Rams

**💡 تذكر:**
> "BOP is your last line of defense - test it, trust it, use it wisely!"
        """,
        "related": ["annular", "ram", "well control equipment", "kick"],
        "category": "Equipment"
    },
    
    "icp": {
        "answer": """
**🎯 ICP (Initial Circulating Pressure)** - ضغط بداية عملية القتل.

**📐 المعادلة:**
ICP = SIDPP + SCR



**حيث:**
- **ICP** = Initial Circulating Pressure (psi)
- **SIDPP** = Shut-In Drill Pipe Pressure (psi)
- **SCR** = Slow Circulating Rate Pressure (psi)

**🧠 الشرح المفصل:**

**SIDPP (Shut-In Drill Pipe Pressure):**
- الضغط الزائد من التكوين
- يمثل الـ Kick pressure
- يُقاس بعد إغلاق البئر

**SCR (Slow Circulating Rate):**
- الضغط المطلوب لتحريك الطين
- يُقاس قبل الـ Kick
- عند سرعة ضخ بطيئة (نصف السرعة العادية)

**المجموع (ICP):**
- الضغط المطلوب للبدء
- يتغلب على ضغط التكوين
- + يحرك الطين

**📊 مثال عملي:**
المعطيات:

SIDPP = 500 psi
SCR = 400 psi
الحل:
ICP = 500 + 400
ICP = 900 psi



**✅ هذا يعني:**
- ابدأ الضخ عند 900 psi
- حافظ على هذا الضغط في البداية
- خفضه تدريجياً حسب الجدول

**🎯 الاستخدام في Kill Methods:**

**Driller's Method:**
1. Circulation #1: ابدأ بـ ICP
2. خفض تدريجياً للصفر
3. Circulation #2: ابدأ بـ ICP مرة أخرى
4. خفض من ICP إلى FCP

**Wait & Weight:**
1. ابدأ مباشرة بـ ICP
2. خفض من ICP إلى FCP
3. حافظ على FCP حتى النهاية

**📈 Pressure Schedule:**
الوقت الضغط
Start → ICP (900 psi)
25% → ICP - 25%
50% → ICP - 50%
75% → ICP - 75%
Bit → FCP



**⚠️ ملاحظات مهمة:**

1. **لا تبدأ بضغط أقل من ICP:**
   - يسبب influx إضافي
   - خطر على البئر

2. **لا تبدأ بضغط أعلى من ICP:**
   - يسبب lost circulation
   - كسر في التكوين

3. **حافظ على الضغط ثابت:**
   - في بداية الضخ
   - حتى تستقر الدورة

4. **راقب الـ Pit Level:**
   - أي زيادة = influx جديد
   - أي نقص = lost circulation

**💡 Tips:**
- سجل ICP بدقة
- استخدم Pressure Chart
- راجع الحسابات مرتين
- تدرب على القراءة السريعة

**📚 Related Concepts:**
- ICP = Start point
- FCP = End point
- الفرق بينهما = Pressure reduction
        """,
        "related": ["fcp", "sidpp", "scr", "kill methods"],
        "category": "Well Control"
    },
    
    "fcp": {
        "answer": """
**🎯 FCP (Final Circulating Pressure)** - ضغط نهاية عملية القتل.

**📐 المعادلة:**
FCP = SCR × (KMW ÷ OMW)



**حيث:**
- **FCP** = Final Circulating Pressure (psi)
- **SCR** = Slow Circulating Rate Pressure (psi)
- **KMW** = Kill Mud Weight (ppg)
- **OMW** = Original Mud Weight (ppg)

**🧠 الشرح التفصيلي:**

**لماذا يتغير الضغط؟**
1. الطين الأثقل = مقاومة أعلى
2. الضغط يتناسب طردياً مع الكثافة
3. النسبة بين الأوزان تحدد التغيير

**الحساب خطوة بخطوة:**
إذا كان:

SCR = 400 psi (للطين الأصلي)
OMW = 10 ppg
KMW = 11 ppg
فإن:
FCP = 400 × (11 ÷ 10)
FCP = 400 × 1.1
FCP = 440 psi



**📊 مثال عملي كامل:**
المعطيات:

SIDPP = 500 psi
SCR = 400 psi
TVD = 10,000 ft
OMW = 10 ppg
الخطوات:
1️⃣ Calculate KMW:
KMW = (500 ÷ 520) + 10 = 10.96 ≈ 11 ppg

2️⃣ Calculate ICP:
ICP = 500 + 400 = 900 psi

3️⃣ Calculate FCP:
FCP = 400 × (11 ÷ 10) = 440 psi

النتائج:

Start: 900 psi (ICP)
End: 440 psi (FCP)
Reduction: 460 psi


**🎯 متى يصل الضغط لـ FCP؟**

**في Driller's Method:**
- Circulation #2
- عندما يصل Kill Mud للريشة (bit)
- بعد ضخ حجم = Drill String Capacity

**في Wait & Weight:**
- نفس الوقت
- عندما يصل KMW للريشة
- تدريجياً حسب الجدول

**📈 Pressure Schedule من ICP إلى FCP:**
الموقع الضغط
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Surface → 900 psi (ICP)
25% depth → 785 psi
50% depth → 670 psi
75% depth → 555 psi
At Bit → 440 psi (FCP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━



**✅ بعد وصول KMW للريشة:**
1. **حافظ على FCP ثابت**
2. استمر بالضخ حتى:
   - يملأ KMW البئر كله
   - يخرج من Annulus
3. الحجم المطلوب = Annular Capacity

**⚠️ إذا لم يصل الضغط لـ FCP:**

**الأسباب المحتملة:**
1. ❌ KMW غير صحيح (أخف من المطلوب)
2. ❌ حسابات خاطئة
3. ❌ Lost circulation
4. ❌ Kick جديد

**الإجراء:**
- أوقف الضخ
- راجع الحسابات
- تحقق من Pit Level
- أعد التقييم

**⚠️ إذا انخفض الضغط تحت FCP:**

**الأسباب:**
1. ✅ KMW أثقل من اللازم (جيد!)
2. ✅ Safety margin working
3. ❌ أو Lost circulation (سيء!)

**الإجراء:**
- راقب Pit Level
- إذا ثابت = OK
- إذا ينقص = Lost circulation

**💡 القاعدة الذهبية:**
عند نهاية القتل:

أوقف الضخ
أغلق البئر
الضغط يجب أن يكون صفر ✅
إذا لم يكن صفر = البئر لم يُقتل كاملاً ❌


**📚 Pressure Relationship:**
SCR (Original) → 400 psi (10 ppg)
↓ (increase by 10%)
FCP (Kill) → 440 psi (11 ppg)



**🎓 للتذكر:**
- FCP = الهدف النهائي
- يعتمد على نسبة الأوزان
- علامة وصول KMW للريشة
- يجب الحفاظ عليه ثابت
        """,
        "related": ["icp", "scr", "kill mud weight", "pressure schedule"],
        "category": "Well Control"
    },
    
    "subsea": {
        "answer": """
**🌊 Subsea Well Control** - السيطرة على الآبار تحت الماء.

**الفروقات الرئيسية عن Surface:**

**1️⃣ Choke Line Friction (CLF):**

**المشكلة:**
خط الخنق طويل (يصل لآلاف الأقدام)
الاحتكاك يقلل الضغط المقروء
القراءة السطحية أقل من الحقيقية


**الحل:**
True SICP = Surface SICP + CLF

حيث:
CLF = Choke Line Friction Loss



**مثال:**
Surface SICP = 800 psi
CLF = 150 psi
True SICP = 800 + 150 = 950 psi


**💡 نصيحة:**
- احسب CLF قبل الحفر
- سجله في Well Control Sheet
- أضفه دائماً للقراءة السطحية

**2️⃣ Riser Margin:**

**ما هو؟**
هامش أمان لإبقاء الـ Riser ممتلئ بالطين
يمنع مشاكل عند الفصل الطارئ



**المعادلة:**
Riser Margin = (MW - Seawater Density) × 0.052 × Water Depth

حيث:

MW = Mud Weight (ppg)
Seawater = 8.6 ppg
Water Depth (ft)


**مثال:**
المعطيات:

MW = 10 ppg
Water Depth = 5,000 ft
الحل:
RM = (10 - 8.6) × 0.052 × 5,000
RM = 1.4 × 0.052 × 5,000
RM = 364 psi



**المعايير:**
الحد الأدنى: 200 psi
الموصى به: 400-600 psi
Maximum: حسب الـ formation strength


**⚠️ لماذا مهم؟**
1. يمنع U-tubing عند الفصل
2. يحافظ على الطين في الـ Riser
3. أمان إضافي

**3️⃣ Kill Line vs Choke Line:**

**Kill Line:**
الاستخدام: ضخ Kill Mud
المميزات:

✅ أقصر من Choke Line
✅ احتكاك أقل
✅ أفضل للضخ
المتى: في بعض الحالات بدل Standpipe



**Choke Line:**
الاستخدام: التحكم بالتدفق
المميزات:

✅ مخصص لـ Well Control
✅ متصل بـ Choke Manifold
المتى: دائماً في حالات الـ Kick



**الاختيار:**
Normal Kill: Standpipe + Choke Line
Alternative: Kill Line + Choke Line
Emergency: أي خط متاح!



**4️⃣ Weak Point Considerations:**

**في Surface Wells:**
Weak Point عادة = Casing Shoe



**في Subsea Wells:**
Weak Point ممكن يكون:

Wellhead (أضعف غالباً)
Casing Shoe
BOP Connection
⚠️ MAASP أقل بسبب عمق الماء



**MAASP Calculation:**
MAASP = Formation Pressure - Hydrostatic - Safety Margin

في Subsea:

Formation Pressure نفسه
لكن Hydrostatic أقل (seawater خفيف)
فالـ MAASP أقل


**5️⃣ BOP Stack Configuration:**

**الترتيب النموذجي (من أسفل لأعلى):**
LMRP (Lower Marine Riser Package)

Connector
Annular Preventer
BOP Stack

Pipe Rams (2 sets)
Blind/Shear Rams
Pipe Rams (additional)
Choke & Kill Lines



**6️⃣ Diverter System:**

**الاستخدام:**
في المياه الضحلة
للـ shallow gas kicks
يحول التدفق بعيداً عن الـ Rig


**⚠️ لا يغلق البئر - فقط يحول!**

**7️⃣ Emergency Disconnect:**

**متى؟**
Rig drift (انحراف الحفارة)
Weather deterioration
Equipment failure


**الإجراء:**
Unlatch LMRP
Move rig away
Well remains shut-in
Return later للقتل


**📊 مقارنة شاملة:**
Feature | Surface | Subsea
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOP Location | Surface | Seabed
Choke Line | Short | Long (CLF!)
Weak Point | Shoe | Wellhead
MAASP | Higher | Lower
Riser Margin | N/A | Required!
Emergency | None | Disconnect
Complexity | Simple | Complex
Cost | Low | High $$$$



**💡 Key Takeaways:**

1. ✅ **Always add CLF** to surface readings
2. ✅ **Maintain Riser Margin** (400-600 psi)
3. ✅ **Know your weak point** (usually wellhead)
4. ✅ **Practice emergency disconnect**
5. ✅ **Use appropriate line** (Kill vs Choke)

**🚨 Critical Mistakes to Avoid:**

❌ Ignoring CLF → wrong pressure control
❌ Low Riser Margin → U-tubing risk
❌ Exceeding MAASP → formation breakdown
❌ Slow response → bigger kick

**📚 Study Tips:**
- فهم الفروقات مهم للامتحان
- CLF & Riser Margin = أسئلة شائعة
- تدرب على الحسابات
- راجع Emergency Procedures
        """,
        "related": ["riser margin", "choke line friction", "maasp", "bop"],
        "category": "Subsea Operations"
    },
    
    "maasp": {
        "answer": """
**⚠️ MAASP (Maximum Allowable Annular Surface Pressure)**
الضغط السطحي الأقصى المسموح به في الـ Annulus.

**📐 المعادلة الأساسية:**
MAASP = (Formation Breakdown Pressure - Hydrostatic Pressure at Shoe) - Safety Margin



**أو:**
MAASP = (FG - MW) × 0.052 × Shoe Depth - Safety Margin

حيث:

FG = Formation Gradient (ppg)
MW = Current Mud Weight (ppg)
Shoe Depth (ft)
Safety Margin = 200-300 psi


**📊 مثال عملي:**
المعطيات:

Formation Gradient = 13.5 ppg
Current MW = 10 ppg
Casing Shoe Depth = 8,000 ft
Safety Margin = 200 psi
الحل:
Step 1: حساب الفرق
Difference = 13.5 - 10 = 3.5 ppg

Step 2: حساب الضغط
Pressure = 3.5 × 0.052 × 8,000
Pressure = 1,456 psi

Step 3: طرح Safety Margin
MAASP = 1,456 - 200
MAASP = 1,256 psi



**🎯 ما معنى MAASP؟**

**إذا تجاوزت MAASP:**
❌ Formation breakdown at shoe
❌ Lost circulation
❌ Underground blowout
❌ فقدان السيطرة على البئر



**✅ يجب أن تبقى:**
SICP < MAASP



**📋 Leak-Off Test (LOT):**

**الهدف:**
تحديد Formation Breakdown Pressure فعلياً



**الطريقة:**
احفر 10-20 ft تحت الـ Shoe
ارفع Drill String
أغلق Annular BOP
اضخ ببطء في الـ Annulus
راقب الضغط
عندما ينحرف الضغط = LOT Pressure


**مثال LOT:**
Leak-Off at: 1,500 psi
Current MW: 10 ppg
Safety Margin: 200 psi

MAASP = 1,500 - 200 = 1,300 psi



**🌊 في Subsea Wells:**

**الفرق:**
MAASP أقل بسبب:

Seawater خفيف (8.6 ppg)
الضغط الهيدروستاتيكي أقل
Weak Point عادة Wellhead


**المعادلة المعدلة:**
MAASP = Formation Pressure - (Seawater HP + Mud HP) - Safety Margin

حيث:
Seawater HP = 0.052 × 8.6 × Water Depth
Mud HP = 0.052 × MW × (TVD - Water Depth)



**مثال Subsea:**
المعطيات:

Water Depth = 5,000 ft
TVD = 15,000 ft
MW = 10 ppg
Formation Pressure = 9,000 psi
Safety Margin = 200 psi
الحل:
Seawater HP = 0.052 × 8.6 × 5,000 = 2,236 psi
Mud HP = 0.052 × 10 × 10,000 = 5,200 psi
Total HP = 2,236 + 5,200 = 7,436 psi

MAASP = 9,000 - 7,436 - 200
MAASP = 1,364 psi



**⚠️ في حالة Kick:**

**السيناريو:**
SICP = 1,500 psi
MAASP = 1,300 psi

❌ المشكلة: SICP > MAASP



**الحلول:**

**1️⃣ Weight Up Mud (الأفضل):**
زيادة MW
يقلل الـ Kick Pressure
يزيد MAASP


**2️⃣ Bleed Off (مؤقت):**
تنفيس بعض الضغط
⚠️ حل مؤقت فقط
يجب متابعة بـ Weight Up


**3️⃣ Bullheading (طوارئ):**
دفع الـ Kick للتكوين
⚠️ قد يسبب Underground Blowout
آخر حل


**📊 MAASP في سيناريوهات مختلفة:**
Scenario | MAASP Effect
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Increase MW | ↑ Increases
Deeper Shoe | ↑ Increases
Weak Formation | ↓ Decreases
Subsea (vs Surface) | ↓ Decreases
After LOT | = Known (accurate)



**🎯 Kick Tolerance:**

**التعريف:**
Kick Tolerance = حجم الـ Kick الذي يمكن التعامل معه قبل الوصول لـ MAASP



**المعادلة:**
Kick Tolerance (bbl) = MAASP ÷ (Kick Gradient × 0.052)

تقريباً: للـ Gas Kick
KT (bbl) ≈ MAASP ÷ 5



**مثال:**
MAASP = 1,500 psi
Gas Gradient ≈ 0.1 psi/ft

KT = 1,500 ÷ (0.1 × 0.052) ≈ 300 bbl



**💡 نصائح للامتحان:**

**أسئلة شائعة:**
1. ✅ حساب MAASP من FG & MW
2. ✅ هل SICP < MAASP?
3. ✅ Subsea MAASP calculations
4. ✅ ماذا تفعل إذا SICP > MAASP?

**أخطاء شائعة:**
❌ نسيان Safety Margin
❌ استخدام MD بدل TVD
❌ خلط Hydrostatic مع MAASP
❌ عدم طرح Seawater في Subsea

**✅ للتذكر:**
MAASP = الحد الأقصى للضغط السطحي
إذا تجاوزته = مشكلة خطيرة
دائماً تأكد: SICP < MAASP



**📚 Related Topics:**
- Formation Integrity Test (FIT)
- Leak-Off Test (LOT)
- Formation Breakdown
- Underground Blowout
- Kick Tolerance
        """,
        "related": ["formation pressure", "leak off test", "kick tolerance"],
        "category": "Well Control"
    }
}

# Suggested questions (expanded)
SUGGESTED_QUESTIONS = [
    "What is hydrostatic pressure?",
    "How to calculate kill mud weight?",
    "Explain Driller's Method step by step",
    "What is the difference between ICP and FCP?",
    "What causes a kick and how to detect it?",
    "Explain BOP components in detail",
    "What is subsea well control?",
    "How to calculate riser margin?",
    "What is MAASP and how to calculate it?",
    "Difference between Wait & Weight and Driller's Method",
    "What are the signs of a kick?",
    "Explain shut-in procedure",
    "What is choke line friction?",
    "How to perform leak-off test?"
]

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

if 'helpful_count' not in st.session_state:
    st.session_state.helpful_count = 0

if 'show_typing' not in st.session_state:
    st.session_state.show_typing = False

# ═══════════════════════════════════════════════════════
# 🧠 ENHANCED AI RESPONSE FUNCTION
# ═══════════════════════════════════════════════════════

def get_ai_response(question):
    """Enhanced AI response with better matching"""
    
    question_lower = question.lower()
    
    # Search in knowledge base with partial matching
    best_match = None
    max_score = 0
    
    for key, data in KNOWLEDGE_BASE.items():
        # Calculate matching score
        score = 0
        keywords = key.split()
        
        for keyword in keywords:
            if keyword in question_lower:
                score += 1
        
        # Check in answer too
        if any(word in question_lower for word in ['what is', 'explain', 'define']):
            if key in question_lower:
                score += 10
        
        if score > max_score:
            max_score = score
            best_match = data
    
    # If good match found
    if max_score >= 1:
        return {
            'answer': best_match['answer'],
            'related': best_match.get('related', []),
            'category': best_match.get('category', 'General'),
            'source': 'Knowledge Base'
        }
    
    # Pattern-based responses
    if any(word in question_lower for word in ["how to calculate", "formula for", "equation"]):
        return {
            'answer': """
🧮 **لم أجد هذه المعادلة المحددة في قاعدة المعرفة.**

**يمكنك استخدام:**

1. 🧮 **Calculator Page** - يحتوي على 7 آلات حاسبة:
   - Hydrostatic Pressure
   - Kill Mud Weight
   - ICP & FCP
   - Riser Margin
   - MAASP
   - Volume Calculations
   - Pressure Conversions

2. 📖 **Formulas Page** - مرجع شامل لكل المعادلات

3. 📚 **Learn Page** - شرح تفصيلي مع أمثلة

**أو جرب إعادة صياغة سؤالك بطريقة مختلفة.**
            """,
            'related': ['calculator', 'formulas', 'learn'],
            'category': 'Calculations',
            'source': 'Pattern Match'
        }
    
    elif any(word in question_lower for word in ["what is", "explain", "define", "tell me about"]):
        return {
            'answer': """
📚 **لم أجد هذا الموضوع في قاعدة المعرفة الحالية.**

**اقتراحات:**

1. **استخدم الأسئلة المقترحة أدناه** 💡
   - مواضيع مهمة مغطاة بالكامل
   - شرح تفصيلي مع أمثلة

2. **زر صفحة Learn** 📚
   - شرح شامل لكل المواضيع
   - ترتيب منطقي حسب الصعوبة
   - أمثلة عملية

3. **جرب Quiz** ❓
   - أسئلة مع إجابات تفصيلية
   - تغطية شاملة للمنهج

4. **أعد صياغة السؤال**
   - استخدم كلمات مفتاحية مختلفة
   - حاول تحديد السؤال أكثر

**مواضيع متاحة:**
- Well Control & Kick Detection
- Kill Methods (Driller's, W&W)
- BOP Equipment
- Pressure Calculations
- Subsea Operations
- MAASP & Formation Integrity
            """,
            'related': ['learn', 'quiz', 'formulas'],
            'category': 'General',
            'source': 'Pattern Match'
        }
    
    # Default fallback
    else:
        return {
            'answer': """
🤔 **لم أفهم سؤالك تماماً.**

**للحصول على أفضل إجابة:**

**✅ جرب:**
1. استخدم الأسئلة المقترحة أدناه
2. اسأل عن موضوع محدد:
   - "What is hydrostatic pressure?"
   - "Explain Driller's Method"
   - "How to calculate kill mud weight?"

**📚 أو استكشف الصفحات الأخرى:**
- **Learn** → شرح تفصيلي
- **Quiz** → تمارين مع حلول
- **Calculator** → حسابات تفاعلية
- **Formulas** → مرجع شامل

**💡 نصيحة:**
- كن محدداً في سؤالك
- استخدم كلمات مفتاحية واضحة
- اسأل عن شيء واحد في المرة

**🎯 أمثلة على أسئلة جيدة:**
✅ "What causes a kick?"
✅ "Explain BOP components"
✅ "Calculate riser margin"
✅ "Difference between ICP and FCP"
            """,
            'related': [],
            'category': 'Help',
            'source': 'Fallback'
        }

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="tutor-header">
    <h1>🤖 AI Tutor - Your Personal IWCF Assistant</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Ask me anything about Well Control - I'm here to help 24/7! 💪
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Powered by Elshamy AI Technology™
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 STATS
# ═══════════════════════════════════════════════════════

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #8B5CF6; margin: 0;">💬 {st.session_state.question_count}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem; font-size: 0.9rem;">Questions Asked</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    kb_topics = len(KNOWLEDGE_BASE)
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #3B82F6; margin: 0;">📚 {kb_topics}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem; font-size: 0.9rem;">Topics Available</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    satisfaction = (st.session_state.helpful_count / max(st.session_state.question_count, 1)) * 100
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #10B981; margin: 0;">🎯 {satisfaction:.0f}%</h3>
        <p style="color: #6B7280; margin-top: 0.5rem; font-size: 0.9rem;">Satisfaction Rate</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# ℹ️ HOW TO USE (Collapsible)
# ═══════════════════════════════════════════════════════

with st.expander("ℹ️ How to use AI Tutor", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 What I can help you with:**
        
        ✅ Explain well control concepts in detail
        ✅ Show formulas and calculation steps
        ✅ Provide real-world examples
        ✅ Answer exam-related questions
        ✅ Clarify procedures and methods
        ✅ Compare different techniques
        
        **📚 Topics I know:**
        - Pressure Calculations (HP, KMW, ICP, FCP)
        - Kill Methods (Driller's, Wait & Weight)
        - BOP Equipment & Components
        - Subsea Operations & Riser Margin
        - Kick Detection & Control
        - MAASP & Formation Integrity
        - Well Control Procedures
        - And much more!
        """)
    
    with col2:
        st.markdown("""
        **✅ How to ask good questions:**
        
        **Do:**
        - ✅ Be specific: "What is hydrostatic pressure?"
        - ✅ Use keywords: "Calculate kill mud weight"
        - ✅ Ask one topic at a time
        - ✅ Request examples: "Explain with example"
        
        **Don't:**
        - ❌ Be too vague: "Tell me everything"
        - ❌ Combine multiple topics
        - ❌ Use unclear terminology
        
        **💡 Pro Tips:**
        - Use the suggested questions below
        - Check related topics in responses
        - Explore other pages for practice
        - Give feedback (👍👎) to help me improve
        """)

# ═══════════════════════════════════════════════════════
# 💬 CHAT INTERFACE
# ═══════════════════════════════════════════════════════

st.markdown("## 💬 Chat with AI Tutor")

# Chat container
chat_container = st.container()

with chat_container:
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for idx, chat in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 You:</strong><br>
                {chat['question']}
                <div style="text-align: right; font-size: 0.75rem; color: #6B7280; margin-top: 0.5rem; opacity: 0.7;">
                    {chat['timestamp']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # AI message
            st.markdown(f"""
            <div class="ai-message">
                <strong>🤖 AI Tutor:</strong>
                <span style="background: #EDE9FE; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.75rem; margin-left: 0.5rem;">
                    {chat.get('category', 'General')}
                </span>
                <br><br>
                {chat['answer'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
            # Related topics
            if chat.get('related'):
                related_html = "".join([f'<span class="related-badge">{r}</span>' for r in chat['related']])
                st.markdown(f"""
                <div style="margin: 0.5rem 0 1rem 0;">
                    <strong style="font-size: 0.9rem;">📌 Related topics:</strong><br>
                    {related_html}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feedback & Clear buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("👍 Helpful", use_container_width=True):
                st.session_state.helpful_count += 1
                st.success("Thanks for your feedback! 🙏")
                time.sleep(1)
                st.rerun()
        
        with col2:
            if st.button("👎 Not Helpful", use_container_width=True):
                st.info("We'll improve! Try rephrasing your question.")
        
        with col3:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.success("Chat cleared! 🎉")
                time.sleep(0.5)
                st.rerun()
    
    else:
        st.markdown("""
        <div class="info-card">
            <h3 style="margin: 0; color: #92400E;">👋 Welcome to AI Tutor!</h3>
            <p style="color: #78350F; margin-top: 0.5rem;">
                I'm your personal IWCF assistant, ready to help you understand Well Control concepts, 
                solve calculations, and prepare for your exam.
            </p>
            <p style="color: #78350F; margin-top: 0.5rem;">
                <strong>Start by:</strong><br>
                • Typing your question below ⬇️<br>
                • Or clicking on a suggested question 💡<br>
                • Or exploring topics in the Learn page 📚
            </p>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ✍️ QUESTION INPUT
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("### ✍️ Ask Your Question")

col1, col2 = st.columns([4, 1])

with col1:
    user_question = st.text_input(
        "💬 Your question:",
        placeholder="e.g., What is hydrostatic pressure? How to calculate kill mud weight?",
        key="question_input",
        label_visibility="collapsed"
    )

with col2:
    ask_button = st.button("🚀 Ask", use_container_width=True, type="primary")

# Process question
if ask_button and user_question:
    # Show typing indicator
    with st.spinner("🤖 AI is thinking..."):
        time.sleep(0.8)  # Simulate thinking
        
        # Get response
        response = get_ai_response(user_question)
        
        # Add to chat history
        st.session_state.chat_history.append({
            'question': user_question,
            'answer': response['answer'],
            'related': response.get('related', []),
            'category': response.get('category', 'General'),
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        st.session_state.question_count += 1
    
    st.rerun()

# ═══════════════════════════════════════════════════════
# 💡 SUGGESTED QUESTIONS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 💡 Suggested Questions")
st.markdown("*Click on any question to get instant answer*")

# Display in 2 columns
cols = st.columns(2)

for idx, suggestion in enumerate(SUGGESTED_QUESTIONS):
    with cols[idx % 2]:
        if st.button(f"💬 {suggestion}", key=f"suggest_{idx}", use_container_width=True):
            # Get response
            response = get_ai_response(suggestion)
            
            # Add to chat history
            st.session_state.chat_history.append({
                'question': suggestion,
                'answer': response['answer'],
                'related': response.get('related', []),
                'category': response.get('category', 'General'),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            
            st.session_state.question_count += 1
            st.rerun()

# ═══════════════════════════════════════════════════════
# 🔗 QUICK LINKS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🔗 Need More Help?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Learn\n\nDetailed Explanations", use_container_width=True):
        st.switch_page("pages/01_📚_Learn.py")

with col2:
    if st.button("❓ Quiz\n\nPractice Questions", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")

with col3:
    if st.button("🧮 Calculator\n\nSolve Problems", use_container_width=True):
        st.switch_page("pages/04_🧮_Calculator.py")

with col4:
    if st.button("📖 Formulas\n\nQuick Reference", use_container_width=True):
        st.switch_page("pages/06_📖_Formulas.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0; font-size: 1.1rem;">
        🎓 <strong>Elshamy IWCF Mastery Method™ - AI Tutor</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Powered by intelligent knowledge base | Always learning, always helping 🤖
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.8;">
        Created by Eng. Ahmed Elshamy | © 2026 All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)