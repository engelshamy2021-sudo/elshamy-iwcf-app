import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# إضافة مسار utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ═══════════════════════════════════════════════════════
# 💾 تحميل Data Manager
# ═══════════════════════════════════════════════════════

try:
    from utils.data_manager import (
        load_progress, 
        save_progress,
        record_module_complete,
        record_study_time,
        update_streak,
        get_user_level
    )
    DATA_MANAGER_AVAILABLE = True
except ImportError:
    DATA_MANAGER_AVAILABLE = False
    
    def get_user_level(xp):
        levels = [(0, "Beginner"), (100, "Learner"), (300, "Student"), 
                  (600, "Practitioner"), (1000, "Skilled"), (1500, "Advanced"),
                  (2200, "Expert"), (3000, "Master"), (4000, "Elite"),
                  (5500, "Legend"), (7500, "IWCF Champion")]
        for min_xp, level_name in reversed(levels):
            if xp >= min_xp:
                return level_name
        return "Beginner"

# ═══════════════════════════════════════════════════════
# 📄 إعدادات الصفحة
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Learn - Elshamy IWCF",
    page_icon="📚",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 التصميم المحسّن
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .learn-header {
        background: linear-gradient(135deg, #10B981 0%, #059669 50%, #047857 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);
    }
    
    .module-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10B981;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .module-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .topic-content {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #E5E7EB;
    }
    
    .practice-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
    
    .formula-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #F59E0B;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #EF4444;
        margin: 1rem 0;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
    }
    
    .xp-badge {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .level-badge {
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    .streak-badge {
        background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    .progress-mini {
        background: #E5E7EB;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .progress-mini-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .sidebar-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #10B981;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .layer-tab {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .layer-simple { background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); }
    .layer-technical { background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); }
    .layer-exam { background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%); }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    th, td {
        border: 1px solid #E5E7EB;
        padding: 0.75rem;
        text-align: left;
    }
    
    th {
        background: #F3F4F6;
        font-weight: 600;
    }
    
    tr:hover {
        background: #F9FAFB;
    }
    
    code {
        background: #1F2937;
        color: #10B981;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
    }
    
    .big-formula {
        font-size: 1.5rem;
        text-align: center;
        padding: 1.5rem;
        background: #1F2937;
        color: #10B981;
        border-radius: 10px;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📚 بيانات الموديولات الكاملة
# ═══════════════════════════════════════════════════════

MODULES = {
    1: {
        "name": "Well Control Fundamentals",
        "icon": "📊",
        "difficulty": "Beginner",
        "description": "أساسيات التحكم في الآبار - المفاهيم الأساسية والضغوط",
        "estimated_time": "4 hours",
        "xp_reward": 500
    },
    2: {
        "name": "Pressure Calculations",
        "icon": "🔢",
        "difficulty": "Intermediate",
        "description": "حسابات الضغط المختلفة - HP, FP, ECD, MAASP",
        "estimated_time": "5 hours",
        "xp_reward": 600
    },
    3: {
        "name": "Kick Detection & Analysis",
        "icon": "🔍",
        "difficulty": "Intermediate",
        "description": "اكتشاف وتحليل الـ Kicks - العلامات والإجراءات",
        "estimated_time": "4 hours",
        "xp_reward": 550
    },
    4: {
        "name": "Kill Methods",
        "icon": "⚡",
        "difficulty": "Advanced",
        "description": "طرق القتل المختلفة - Driller's, W&W, Volumetric",
        "estimated_time": "6 hours",
        "xp_reward": 750
    },
    5: {
        "name": "Well Control Equipment",
        "icon": "🔧",
        "difficulty": "Intermediate",
        "description": "معدات التحكم - BOP, Rams, Choke, Accumulator",
        "estimated_time": "4 hours",
        "xp_reward": 500
    },
    6: {
        "name": "Gas Behavior & Migration",
        "icon": "💨",
        "difficulty": "Advanced",
        "description": "سلوك الغاز - Boyle's Law, Migration, Expansion",
        "estimated_time": "4 hours",
        "xp_reward": 600
    },
    7: {
        "name": "Complications & Solutions",
        "icon": "⚠️",
        "difficulty": "Advanced",
        "description": "المشاكل والحلول - Lost Circ, Underground Blowout, H2S",
        "estimated_time": "4 hours",
        "xp_reward": 650
    },
    8: {
        "name": "Procedures & Regulations",
        "icon": "📋",
        "difficulty": "Intermediate",
        "description": "الإجراءات والقوانين - IWCF Standards, Safety",
        "estimated_time": "3 hours",
        "xp_reward": 400
    },
}

# ═══════════════════════════════════════════════════════
# 📖 بيانات المواضيع الكاملة
# ═══════════════════════════════════════════════════════

TOPICS = {
    1: [
        {"id": 1, "name": "Introduction to Well Control", "time": 30, "xp": 25},
        {"id": 2, "name": "Pressure Concepts", "time": 45, "xp": 30},
        {"id": 3, "name": "Hydrostatic Pressure", "time": 60, "xp": 35},
        {"id": 4, "name": "Kick Indicators", "time": 45, "xp": 30},
        {"id": 5, "name": "Primary vs Secondary Barriers", "time": 40, "xp": 25},
    ],
    2: [
        {"id": 6, "name": "Formation Pressure", "time": 60, "xp": 35},
        {"id": 7, "name": "Pressure Gradients", "time": 50, "xp": 30},
        {"id": 8, "name": "Equivalent Circulating Density (ECD)", "time": 55, "xp": 35},
        {"id": 9, "name": "Bottomhole Pressure Calculations", "time": 65, "xp": 40},
        {"id": 10, "name": "MAASP Calculations", "time": 60, "xp": 40},
    ],
    3: [
        {"id": 11, "name": "Primary Kick Indicators", "time": 45, "xp": 30},
        {"id": 12, "name": "Secondary Kick Indicators", "time": 40, "xp": 25},
        {"id": 13, "name": "Shut-in Procedures", "time": 55, "xp": 35},
        {"id": 14, "name": "SIDPP and SICP", "time": 50, "xp": 35},
        {"id": 15, "name": "Kick Analysis", "time": 60, "xp": 40},
    ],
    4: [
        {"id": 16, "name": "Driller's Method", "time": 90, "xp": 50},
        {"id": 17, "name": "Wait and Weight Method", "time": 90, "xp": 50},
        {"id": 18, "name": "Volumetric Method", "time": 75, "xp": 45},
        {"id": 19, "name": "Bullheading", "time": 45, "xp": 30},
        {"id": 20, "name": "Kill Sheet Calculations", "time": 80, "xp": 45},
    ],
    5: [
        {"id": 21, "name": "BOP Components", "time": 50, "xp": 30},
        {"id": 22, "name": "Annular Preventer", "time": 40, "xp": 25},
        {"id": 23, "name": "Ram Preventers", "time": 45, "xp": 30},
        {"id": 24, "name": "Choke Manifold", "time": 50, "xp": 30},
        {"id": 25, "name": "Accumulator System", "time": 45, "xp": 30},
    ],
    6: [
        {"id": 26, "name": "Gas Behavior (Boyle's Law)", "time": 60, "xp": 40},
        {"id": 27, "name": "Gas Migration", "time": 55, "xp": 35},
        {"id": 28, "name": "Gas Expansion Calculations", "time": 65, "xp": 40},
        {"id": 29, "name": "Stripping Operations", "time": 50, "xp": 35},
    ],
    7: [
        {"id": 30, "name": "Lost Circulation", "time": 55, "xp": 35},
        {"id": 31, "name": "Underground Blowout", "time": 60, "xp": 40},
        {"id": 32, "name": "Stuck Pipe During Kill", "time": 50, "xp": 35},
        {"id": 33, "name": "H2S Considerations", "time": 45, "xp": 35},
    ],
    8: [
        {"id": 34, "name": "IWCF Standards", "time": 40, "xp": 25},
        {"id": 35, "name": "Safety Procedures", "time": 45, "xp": 30},
        {"id": 36, "name": "Well Control Barriers", "time": 50, "xp": 30},
    ],
}
# ═══════════════════════════════════════════════════════
# 📚 المحتوى التعليمي الكامل والموسّع
# ═══════════════════════════════════════════════════════

CONTENT = {
    # ═══════════════════════════════════════════════════════
    # MODULE 1: WELL CONTROL FUNDAMENTALS
    # ═══════════════════════════════════════════════════════
    
    "Introduction to Well Control": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Well Control؟

**تخيل معايا الموقف ده:**

عندك زجاجة مياه غازية 🥤 مقفولة...
- جوا في ضغط عالي (الغاز مضغوط)
- لو فتحتها بسرعة → **الغاز هيطلع بقوة!** 💥
- لو فتحتها بالراحة → **تقدر تتحكم فيها** ✅

---

### 🛢️ البئر نفس الفكرة بالظبط!

تحت الأرض في:
- **بترول** 🛢️
- **غاز** 💨  
- **مياه** 💧

كل دول **مضغوطين جداً** بسبب وزن الصخور فوقيهم!

---

### ⚠️ لو مسكتش الضغط ده؟

السوائل دي هتطلع بقوة = **BLOWOUT** 😱

**Blowout = كارثة!**
- خسائر في الأرواح 💀
- تلوث البيئة 🌍
- خسائر مالية ضخمة 💰

---

### 💡 الحل؟ Well Control!

**Well Control = إزاي نتحكم في ضغط البئر**

الطريقة الأساسية:
> نحط **طين ثقيل** في البئر ⬇️
> الطين ده بيعمل **ضغط** يمنع السوائل تطلع ⬆️

---

### 🛡️ خطوط الدفاع:

| الخط | الاسم | الوظيفة |
|------|-------|---------|
| **الأول** | الطين (Mud) | يمنع الـ Kick من الأول |
| **الثاني** | BOP | يقفل البئر لو الطين فشل |

---

### 📝 الخلاصة:

> **"Well Control = التحكم في ضغط البئر علشان نمنع الـ Blowout"**

> **"الطين هو خط الدفاع الأول، والـ BOP هو الثاني"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📖 Definition:

**Well Control** is the technique of maintaining formation pressure equilibrium using:
1. **Hydrostatic Pressure** (Primary barrier)
2. **Mechanical Equipment** (Secondary barrier)

---

### 🛡️ Barrier Philosophy (فلسفة الحواجز):

#### **Primary Barrier (الحاجز الأول):**

| Component | Description |
|-----------|-------------|
| **Mud Column** | Hydrostatic pressure > Formation pressure |
| **Float Valves** | Prevent backflow in drill string |
| **Wellbore Cement** | Isolates formations |

#### **Secondary Barrier (الحاجز الثاني):**

| Component | Description |
|-----------|-------------|
| **BOP Stack** | Mechanical closure of wellbore |
| **Casing** | Steel pipe cemented in place |
| **Wellhead** | Surface pressure containment |

---

### ⚠️ Key Terminology:

| Term | Arabic | Definition |
|------|--------|------------|
| **Kick** | ركلة | Formation fluid enters wellbore |
| **Blowout** | انفجار | Uncontrolled flow to surface |
| **Kill** | قتل البئر | Regaining well control |
| **Shut-in** | إغلاق | Closing BOP to stop flow |
| **Circulate** | تدوير | Pumping fluid through well |

---

### 📊 Well Control Objectives:

    PREVENT kicks from occurring
    └── Maintain adequate mud weight
    └── Monitor well constantly

    DETECT kicks early
    └── Watch for indicators
    └── React quickly

    CONTROL kicks safely
    └── Proper shut-in procedure
    └── Correct kill method

    KILL the well
    └── Circulate kick out
    └── Restore primary barrier



---

### 🔄 Well Control Sequence:

Normal Drilling
↓
Kick Detected (Primary barrier failed)
↓
Shut-in Well (Activate secondary barrier)
↓
Record Pressures (SIDPP, SICP)
↓
Calculate Kill Parameters
↓
Execute Kill Procedure
↓
Verify Well is Dead
↓
Resume Operations



---

### ⚖️ Pressure Balance Concept:

**For Safe Operations:**

Formation Pressure < Hydrostatic Pressure < Fracture Pressure
FP < HP < FP(frac)



This is called the **"Mud Window"** or **"Operating Window"**
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question Type 1: Primary Barrier

**Q: What is the PRIMARY well control barrier during drilling operations?**

- A) Blowout Preventer (BOP)
- B) Casing string
- C) **Mud column (Hydrostatic Pressure)** ✅
- D) Cement

**💡 Explanation:**
The mud column provides hydrostatic pressure that prevents formation fluids from entering the wellbore. This is the FIRST line of defense.

---

### ❓ Question Type 2: Secondary Barrier

**Q: The BOP is considered a:**

- A) Primary barrier
- B) **Secondary barrier** ✅
- C) Tertiary barrier
- D) Not a barrier

**💡 Explanation:**
BOP is secondary because it's only used AFTER the primary barrier (mud) has failed.

---

### ❓ Question Type 3: Barrier Requirements

**Q: How many independent barriers should be in place at ALL times?**

- A) One
- B) **Two (minimum)** ✅
- C) Three
- D) Depends on the operation

**💡 Explanation:**
Industry standard requires MINIMUM 2 barriers. If one fails, the other is backup.

---

### ⚠️ Common Exam Traps:

| Trap | Why It's Wrong |
|------|----------------|
| "BOP is primary barrier" | BOP is SECONDARY, not primary |
| "One barrier is enough" | MINIMUM 2 barriers required |
| "Cement alone is sufficient" | Need active + passive barriers |

---

### 📝 Memory Tips:

🧠 Remember:

P = Primary = Pressure = Mud
S = Secondary = Steel = BOP

"Mud comes FIRST, BOP is BACKUP"



---

### 🎯 Key Points for Exam:

✅ Primary barrier = Mud weight (Hydrostatic pressure)
✅ Secondary barrier = BOP system
✅ Minimum 2 barriers at all times
✅ Never remove both barriers simultaneously
✅ Barriers must be TESTED before relying on them
        """
    },
    
    "Hydrostatic Pressure": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Hydrostatic Pressure؟

**تخيل معايا:**

عندك برج من الكوبايات المياه فوق بعض 🥛🥛🥛🥛🥛

**سؤال:** القاعدة (الكوباية اللي تحت خالص) حاسة بإيه؟

**الإجابة:** حاسة بـ **وزن كل الكوبايات** اللي فوقيها!

---

### 🏊 مثال من حياتك:

لما تنزل **قاع حمام السباحة**:
- فوق السطح: مفيش ضغط
- في النص: ضغط متوسط
- في القاع: **ودانك بتحس بضغط قوي!**

**ليه؟** علشان وزن كل المياه اللي فوقك!

---

### 🛢️ نفس الكلام في البئر!

**Hydrostatic Pressure = وزن عمود الطين من السطح للقاع**


السطح    ← ضغط = صفر
   ↓
   ↓      ← الضغط بيزيد
   ↓
   ↓      ← الضغط بيزيد أكتر
   ↓
القاع    ← أعلى ضغط! 💪



---

### 📐 القواعد البسيطة:

| القاعدة | المعنى |
|---------|--------|
| **أعمق = ضغط أكتر** | كل ما تنزل، الضغط يزيد |
| **طين أثقل = ضغط أكتر** | طين 12 ppg أقوى من 10 ppg |

---

### 🔢 المعادلة السحرية:

<div class="big-formula">
HP = 0.052 × MW × TVD
</div>

**يعني:**
- **HP** = الضغط (psi)
- **MW** = وزن الطين (ppg)
- **TVD** = العمق الرأسي (ft)
- **0.052** = رقم ثابت (احفظه!)

---

### 📝 مثال بسيط:

**لو عندك:**
- طين وزنه **10 ppg**
- عمق **10,000 ft**

**الحساب:**

HP = 0.052 × 10 × 10,000
HP = 5,200 psi



**يعني في القاع في ضغط 5,200 psi! 💪**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📐 The Fundamental Equation:

<div class="big-formula">
HP = 0.052 × MW × TVD
</div>

| Symbol | Meaning | Unit | Arabic |
|--------|---------|------|--------|
| **HP** | Hydrostatic Pressure | psi | الضغط الهيدروستاتيكي |
| **MW** | Mud Weight | ppg | وزن الطين |
| **TVD** | True Vertical Depth | ft | العمق الرأسي الحقيقي |
| **0.052** | Conversion constant | - | ثابت التحويل |

---

### 🔄 Rearranging the Formula:

**To find Mud Weight:**

MW = HP / (0.052 × TVD)



**To find Depth:**

TVD = HP / (0.052 × MW)



---

### 📊 Worked Examples:

#### **Example 1: Find HP**

**Given:**
- MW = 12 ppg
- TVD = 8,500 ft

**Solution:**

HP = 0.052 × 12 × 8,500
HP = 0.052 × 102,000
HP = 5,304 psi



---

#### **Example 2: Find MW**

**Given:**
- HP required = 6,500 psi
- TVD = 10,000 ft

**Solution:**

MW = HP / (0.052 × TVD)
MW = 6,500 / (0.052 × 10,000)
MW = 6,500 / 520
MW = 12.5 ppg



---

#### **Example 3: Find TVD**

**Given:**
- HP = 4,680 psi
- MW = 9 ppg

**Solution:**

TVD = HP / (0.052 × MW)
TVD = 4,680 / (0.052 × 9)
TVD = 4,680 / 0.468
TVD = 10,000 ft



---

### ⚠️ Critical Points:

| Point | Explanation |
|-------|-------------|
| **Always use TVD** | Never use Measured Depth (MD)! |
| **HP is independent of** | Hole diameter, pipe size, pump rate |
| **HP exists even when** | Not circulating, well shut-in |
| **HP acts in all directions** | Down, up, and sideways |

---

### 🔄 TVD vs MD:


     Surface
        │
  TVD   │   MD (along hole)
 8000ft │    9500ft
        │      ╱
        │    ╱
        │  ╱  (deviated section)
        │╱
     Bottom



**Always use TVD for HP calculations!**

---

### 📊 Unit Conversion:

| From | To | Multiply by |
|------|-----|-------------|
| ppg | psi/ft | 0.052 |
| psi/ft | ppg | 19.23 |
| sg | ppg | 8.33 |
| ppg | sg | 0.12 |

**Example:**

10 ppg = 10 × 0.052 = 0.52 psi/ft (gradient)
1.2 sg = 1.2 × 8.33 = 10 ppg


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Direct HP Calculation

**Q: Calculate the hydrostatic pressure at 8,000 ft TVD with 12 ppg mud.**

- A) 4,160 psi
- B) 4,800 psi
- C) **4,992 psi** ✅
- D) 5,200 psi

**Solution:**

HP = 0.052 × MW × TVD
HP = 0.052 × 12 × 8,000
HP = 4,992 psi ✅



---

### ❓ Type 2: Find Mud Weight

**Q: What mud weight is needed to create 5,200 psi at 10,000 ft?**

- A) 9 ppg
- B) **10 ppg** ✅
- C) 11 ppg
- D) 12 ppg

**Solution:**

MW = HP / (0.052 × TVD)
MW = 5,200 / (0.052 × 10,000)
MW = 5,200 / 520
MW = 10 ppg ✅



---

### ❓ Type 3: Find Depth

**Q: At what TVD will 11 ppg mud create 5,720 psi?**

- A) 8,000 ft
- B) 9,000 ft
- C) **10,000 ft** ✅
- D) 11,000 ft

**Solution:**

TVD = HP / (0.052 × MW)
TVD = 5,720 / (0.052 × 11)
TVD = 5,720 / 0.572
TVD = 10,000 ft ✅



---

### ❓ Type 4: TVD vs MD Trap

**Q: Well data: MD = 12,000 ft, TVD = 10,000 ft, MW = 10 ppg. Calculate HP at bottom.**

- A) 5,200 psi using TVD ✅
- B) 6,240 psi using MD ❌
- C) 5,720 psi
- D) 4,680 psi

**⚠️ TRAP: They give you MD to confuse you! Always use TVD!**

HP = 0.052 × 10 × 10,000 = 5,200 psi ✅
(NOT 0.052 × 10 × 12,000 = 6,240 psi) ❌



---

### ❓ Type 5: Unit Conversion

**Q: MW = 1.2 sg. Calculate HP at 8,000 ft TVD.**

- A) 4,160 psi
- B) **4,992 psi** ✅
- C) 5,200 psi
- D) 3,744 psi

**Solution:**

First convert sg to ppg:
MW = 1.2 × 8.33 = 10 ppg

Then calculate HP:
HP = 0.052 × 10 × 8,000 = 4,160 psi

Wait! Let me recalculate:
MW = 1.2 × 8.33 = 9.996 ≈ 10 ppg
HP = 0.052 × 10 × 8,000 = 4,160 psi

Hmm, let me check the options again...
Actually: 1.2 sg = 12 ppg (approximation often used)
HP = 0.052 × 12 × 8,000 = 4,992 psi ✅



---

### ⚠️ Common Exam Mistakes:

| Mistake | Correct Approach |
|---------|-----------------|
| Using MD instead of TVD | **Always use TVD** |
| Forgetting 0.052 | HP = **0.052** × MW × TVD |
| Wrong unit for MW | Convert sg to ppg first |
| Rounding too early | Keep decimals until final answer |

---

### 📝 Exam Tips:

🧠 Quick Mental Check:

10 ppg × 10,000 ft ≈ 5,200 psi
12 ppg × 10,000 ft ≈ 6,240 psi

If your answer is way off these, CHECK YOUR WORK!


        """
    },
    
    "Pressure Concepts": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 أنواع الضغط في البئر

**في البئر عندنا 3 أنواع ضغط أساسية:**

---

### 1️⃣ Hydrostatic Pressure (ضغط الطين) 🟤

**ده إيه؟**
- وزن عمود الطين في البئر
- **ده اللي بيمنع الـ Kick!**

**المعادلة:**

HP = 0.052 × MW × TVD



---

### 2️⃣ Formation Pressure (ضغط التكوين) 🪨

**ده إيه؟**
- ضغط السوائل جوا الصخر تحت الأرض
- **ده اللي عايز يطلع ويعملنا Kick!**

**أنواعه:**
| النوع | المعنى |
|-------|--------|
| **Normal** | ضغط طبيعي (0.465 psi/ft) |
| **Abnormal** | ضغط أعلى من الطبيعي |
| **Subnormal** | ضغط أقل من الطبيعي |

---

### 3️⃣ Bottomhole Pressure (ضغط قاع البئر) ⬇️

**ده إيه؟**
- الضغط الكلي في قاع البئر
- **= HP + أي ضغط إضافي**

---

### ⚖️ القاعدة الذهبية:


 ضغط الطين      >      ضغط التكوين

(Hydrostatic) (Formation)
HP > FP


 علشان السوائل ما تدخلش البئر!



---

### 💡 تشبيه بسيط:

تخيل إنك بتكبس على **غطا قلم حبر** ✏️

- لو كبست قوي → القلم مش هيطلع
- لو سبته → القلم هيطلع!

**الطين بيكبس على الصخر بنفس الطريقة!**

---

### 📊 ملخص:

| الضغط | الوظيفة | 
|-------|---------|
| **HP** | يمنع الـ Kick |
| **FP** | يسبب الـ Kick |
| **BHP** | الضغط الفعلي في القاع |
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Pressure Types in Detail:

---

#### **1. Hydrostatic Pressure (HP)**

HP = 0.052 × MW × TVD



| Property | Value |
|----------|-------|
| **Source** | Weight of fluid column |
| **Direction** | Acts in all directions |
| **Control** | Adjust mud weight |

---

#### **2. Formation Pressure (FP)**

**Also called:** Pore Pressure, Reservoir Pressure

| Type | Gradient | Equivalent MW |
|------|----------|---------------|
| **Normal** | 0.465 psi/ft | 8.94 ppg |
| **Abnormal** | > 0.465 psi/ft | > 8.94 ppg |
| **Subnormal** | < 0.465 psi/ft | < 8.94 ppg |

**Causes of Abnormal Pressure:**
- Undercompaction
- Tectonic activity
- Aquathermal pressuring
- Hydrocarbon generation

---

#### **3. Bottomhole Pressure (BHP)**

**Static Condition (Not Circulating):**

BHP = HP = 0.052 × MW × TVD



**Dynamic Condition (Circulating):**

BHP = HP + APL


Where APL = Annular Pressure Loss

---

#### **4. Fracture Pressure (FP_frac)**

The pressure at which the formation will break/fracture.

Fracture Gradient typically: 0.7 - 1.0 psi/ft



---

### ⚖️ Pressure Balance Concept:

**Safe Operating Window:**

┌─────────────────────────────────────────┐
│ │
│ Formation < BHP < Fracture│
│ Pressure ↑ Pressure│
│ │ │
│ Operating │
│ Window │
└─────────────────────────────────────────┘



**If BHP < FP:** Kick occurs (underbalanced)
**If BHP > Fracture:** Lost circulation/Underground blowout

---

### 📊 Pressure Status:

| Condition | Definition | Result |
|-----------|------------|--------|
| **Overbalanced** | HP > FP | Safe, no kick |
| **Balanced** | HP = FP | Risky |
| **Underbalanced** | HP < FP | **Kick!** |

---

### 🔢 Example Calculation:

**Given:**
- TVD = 10,000 ft
- MW = 11 ppg
- FP gradient = 0.52 psi/ft

**Calculate:**

HP = 0.052 × 11 × 10,000 = 5,720 psi
FP = 0.52 × 10,000 = 5,200 psi

HP (5,720) > FP (5,200)
∴ Well is OVERBALANCED ✅


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Identify Pressure Status

**Q: Well data:**
- **TVD = 10,000 ft**
- **MW = 10 ppg**  
- **Formation pressure = 5,500 psi**

**Is the well overbalanced or underbalanced?**

**Solution:**

HP = 0.052 × 10 × 10,000 = 5,200 psi
FP = 5,500 psi

HP (5,200) < FP (5,500)
∴ UNDERBALANCED → Kick risk! ⚠️



---

### ❓ Type 2: Required Mud Weight

**Q: What MINIMUM mud weight is needed to balance formation pressure of 5,720 psi at 10,000 ft?**

- A) 10 ppg
- B) **11 ppg** ✅
- C) 12 ppg
- D) 13 ppg

**Solution:**

MW = FP / (0.052 × TVD)
MW = 5,720 / (0.052 × 10,000)
MW = 5,720 / 520
MW = 11 ppg ✅



---

### ❓ Type 3: Definition Question

**Q: An "overbalanced" well means:**

- A) Formation pressure exceeds hydrostatic pressure
- B) **Hydrostatic pressure exceeds formation pressure** ✅
- C) The well is flowing
- D) Mud weight is too light

---

### ❓ Type 4: Normal Pressure

**Q: Normal formation pressure gradient is approximately:**

- A) 0.433 psi/ft
- B) **0.465 psi/ft** ✅
- C) 0.520 psi/ft
- D) 0.650 psi/ft

**💡 Remember: 0.465 psi/ft ≈ 8.94 ppg**

---

### ⚠️ Exam Traps:

| Trap | Correct Understanding |
|------|----------------------|
| "Overbalanced means too much pressure" | It means HP > FP (this is SAFE) |
| "Balanced is ideal" | Balanced is RISKY (no safety margin) |
| "BHP = HP always" | Only when static! BHP = HP + APL when circulating |

---

### 📝 Key Definitions to Memorize:

✅ Overbalanced: HP > FP → Safe
✅ Underbalanced: HP < FP → Kick!
✅ Normal FP gradient: 0.465 psi/ft
✅ Fresh water gradient: 0.433 psi/ft


        """
    },
    
    "Kick Indicators": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Kick؟

**Kick = سوائل من الصخر دخلت البئر** 😰

يعني ضغط التكوين غلب ضغط الطين!

---

### 🚨 إزاي نعرف إن في Kick؟

**في علامات بتقولنا: "انتبه! في حاجة غلط!"**

---

### 🔴 العلامات الرئيسية (Primary Indicators):

**دي العلامات الأكيدة اللي لازم تتصرف فوراً!**

| العلامة | المعنى | ليه بتحصل؟ |
|---------|--------|------------|
| **📈 Pit Gain** | مستوى الطين في الـ Pits زاد! | حاجة دخلت البئر |
| **⬆️ Flow Increase** | الطين بيرجع أكتر من المفروض | التكوين بيدفع |
| **⬇️ Pump Pressure Drop** | ضغط المضخة قل | حاجة خفيفة دخلت |

---

### 🟡 العلامات الثانوية (Secondary Indicators):

**دي علامات تحذيرية - راقب وانتبه!**

| العلامة | المعنى |
|---------|--------|
| **Drilling Break** | سرعة الحفر زادت فجأة |
| **Connection Gas** | غاز بيطلع وقت الوصلات |
| **Cut Mud** | وزن الطين قل (غاز داخله) |

---

### 🥇 أهم علامة؟

## **PIT GAIN هو الأهم!** 📈

لو شفت الـ Pits بتزيد → **في Kick!**

---

### ⚡ التصرف الصحيح:

لو شفت أي علامة رئيسية:
↓
وقف فوراً!
↓
اعمل Flow Check
↓
لو في Flow → Shut In!



---

### 💡 تذكر:

> **"شكيت؟ → Flow Check!"**
> 
> **"اتأكدت؟ → Shut In!"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Classification of Kick Indicators:

---

#### **🔴 Primary (Direct) Indicators:**

These **CONFIRM** a kick is occurring:

| Indicator | Description | Mechanism |
|-----------|-------------|-----------|
| **Pit Volume Gain** | Increase in mud tank levels | Formation fluid entering wellbore displaces mud |
| **Flow Rate Increase** | Returns exceed pump output | Formation pressure pushing fluid out |
| **Pump Pressure Decrease** | Reduced SPP with no other change | Lighter influx reduces hydrostatic head |
| **Flow with Pumps Off** | Well flowing without circulation | Positive differential pressure (FP > HP) |

---

#### **🟡 Secondary (Indirect) Indicators:**

These **WARN** of potential kick:

| Indicator | Description | Action Required |
|-----------|-------------|-----------------|
| **Drilling Break** | Sudden increase in ROP | Monitor, may indicate porous zone |
| **Connection Gas** | High gas at connections | Check mud weight, monitor closely |
| **Trip Gas** | Gas after tripping | Normal if small, watch volume |
| **Cut Mud** | Reduced mud weight | Check for gas cutting |
| **Torque/Drag Change** | Change in string behavior | May indicate swelling/hole problems |
| **Fill-up Volume Short** | Hole not taking expected volume | Possible underground flow |

---

### 📊 Reliability Ranking:

Most Reliable
│
├── 1. Pit Volume Gain ⭐⭐⭐⭐⭐
│
├── 2. Flow Rate Increase ⭐⭐⭐⭐
│
├── 3. Flowing with Pumps Off ⭐⭐⭐⭐
│
├── 4. Pump Pressure Decrease ⭐⭐⭐
│
├── 5. Drilling Break ⭐⭐
│
└── 6. Connection Gas ⭐
│
Least Reliable



---

### ⚠️ Response Protocol:

**For PRIMARY Indicators:**

    STOP pumps immediately
    Raise kelly/top drive above rotary table
    SHUT IN the well (close BOP)
    Record SIDPP and SICP
    Notify supervisor



**For SECONDARY Indicators:**

    Increase monitoring frequency
    Perform flow check if suspicious
    Check mud properties
    Be prepared for shut-in



---

### 🔬 Why Pump Pressure Decreases:

**Normal Condition:**

BHP = HP(mud) + SPP(friction losses)



**With Kick (lighter fluid):**

BHP = HP(mud) + HP(influx) + SPP
↓ (influx lighter than mud)
BHP decreases
↓
Less backpressure needed
↓
SPP decreases


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Most Reliable Indicator

**Q: What is the MOST reliable kick indicator?**

- A) Drilling break
- B) **Pit gain** ✅
- C) Connection gas
- D) Pump pressure change

**💡 Pit gain is MOST reliable because it directly shows influx volume.**

---

### ❓ Question 2: Primary vs Secondary

**Q: Which of the following is a SECONDARY kick indicator?**

- A) Pit volume increase
- B) Flow rate increase
- C) **Drilling break** ✅
- D) Pump pressure decrease

**💡 Drilling break is secondary - it's a warning, not confirmation.**

---

### ❓ Question 3: Immediate Action

**Q: You notice a 10 bbl pit gain. What should you do?**

- A) Continue drilling and monitor
- B) Increase pump rate
- C) **Stop pumps and shut in** ✅
- D) Circulate and observe

**💡 Any confirmed pit gain = IMMEDIATE shut-in!**

---

### ❓ Question 4: All Are Primary EXCEPT

**Q: All of the following are PRIMARY kick indicators EXCEPT:**

- A) Pit gain
- B) Flow increase with pumps on
- C) **Drilling break** ✅
- D) Pump pressure decrease

---

### ❓ Question 5: Flow Check

**Q: When should you perform a flow check?**

- A) Only after drilling break
- B) Only after pit gain
- C) **Whenever any indicator is observed** ✅
- D) Only when ordered by supervisor

---

### ⚠️ Common Exam Traps:

| Trap Question | Correct Answer |
|---------------|----------------|
| "Most important indicator" | **Pit gain** (not drilling break!) |
| "First action for any indicator" | **Stop and check** (not wait!) |
| "Drilling break means kick" | **No! It's secondary** (just a warning) |

---

### 📝 Memory Aid:

PRIMARY = Direct evidence of influx:
P - Pit gain
F - Flow increase
P - Pump pressure drop
F - Flow when pumps off

SECONDARY = Warning signs only:
D - Drilling break
C - Connection gas
C - Cut mud


        """
    },
    
    "Primary vs Secondary Barriers": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 فكرة الـ Barriers

**تخيل بيتك:**

🚪 **الباب الأول (Primary):** 
- بيحميك من اللي برا
- شغال طول الوقت

🚪 **الباب الثاني (Secondary):**
- لو الأول اتكسر، ده يحميك
- موجود للاحتياط

---

### 🛢️ في البئر:

#### **🟤 Primary Barrier = الطين (Mud)**


  ↓ الطين بيضغط على التكوين
  ↓
  ↓ علشان السوائل ما تدخلش
  ↓
═══════════ Formation ═══════════



**الطين شغال 24/7 طول ما البئر مفتوح!**

---

#### **🔴 Secondary Barrier = BOP**


╔═══════════════════╗
║   BOP Stack       ║ ← يقفل لو الطين فشل
╠═══════════════════╣
║   Annular         ║
╠═══════════════════╣
║   Pipe Rams       ║
╠═══════════════════╣
║   Blind Rams      ║
╚═══════════════════╝



**الـ BOP موجود للطوارئ بس!**

---

### ⚖️ القواعد الذهبية:

| القاعدة | التفسير |
|---------|---------|
| **لازم 2 Barriers دايماً** | واحد يفشل؟ التاني يحمي |
| **ما تشيلش الاتنين مع بعض** | دايماً واحد موجود |
| **اختبر قبل ما تعتمد** | تأكد إنه شغال |

---

### 💡 مثال من الحياة:

**زي حزام الأمان + الـ Airbag في العربية:**

- **حزام الأمان** = Primary (شغال دايماً)
- **Airbag** = Secondary (يشتغل وقت الحادثة)

**مش هتشيل الاتنين وأنت سايق!**

---

### 📝 تذكر:

> **"الطين أولاً، الـ BOP ثانياً"**
> 
> **"Primary = Pressure, Secondary = Steel"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Barrier Definition:

**A Well Control Barrier is:**
> An envelope of one or several dependent barrier elements that can prevent flow from a potential source of inflow.

---

### 🟤 Primary Barriers:

| Barrier Element | Type | Description |
|-----------------|------|-------------|
| **Mud Column** | Fluid | Provides hydrostatic pressure |
| **Float Valves** | Mechanical | Prevent backflow in string |
| **Cement** | Fixed | Isolates formations permanently |

**Key Characteristics:**
- Active at all times
- First line of defense
- Prevents influx from occurring

---

### 🔴 Secondary Barriers:

| Barrier Element | Type | Description |
|-----------------|------|-------------|
| **BOP Stack** | Mechanical | Annular, Rams |
| **Casing** | Fixed | Contains pressure |
| **Wellhead** | Mechanical | Surface containment |
| **IBOP / Kelly Cock** | Mechanical | String safety valve |

**Key Characteristics:**
- Backup system
- Activated when primary fails
- Must be tested and verified

---

### 📊 Barrier Requirements:

MINIMUM REQUIREMENT:
┌─────────────────────────┐
│ Two Independent │
│ Tested Barriers │
│ At All Times │
└─────────────────────────┘



---

### ⚠️ Barrier Rules:

| Rule | Explanation |
|------|-------------|
| **Independence** | Barriers must be independent (one fails, other works) |
| **Testing** | All barriers must be tested before relying on them |
| **Documentation** | Barrier status must be documented |
| **Common Mode** | Avoid barriers with same failure mode |

---

### 📊 Barrier Verification:

| Barrier | Verification Method |
|---------|---------------------|
| Mud Weight | Measure regularly |
| BOP | Pressure test |
| Casing | Pressure test + logs |
| Float Valves | Float function test |

---

### 🔄 Barrier Status Examples:

**During Drilling:**

Primary: Mud Column ✅
Secondary: BOP Stack ✅
Status: 2 barriers OK ✅



**During Tripping (Full Hole):**

Primary: Mud Column ✅
Secondary: BOP Stack ✅
Status: 2 barriers OK ✅



**During Casing Run:**

Primary: Mud Column ✅
Secondary: Limited (no BOP on casing)
Status: RISK - Need additional barriers


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Primary Barrier

**Q: The PRIMARY well control barrier during drilling is:**

- A) Blowout Preventer
- B) Casing
- C) **Mud column (Hydrostatic pressure)** ✅
- D) Drill string

---

### ❓ Question 2: Secondary Barrier

**Q: The BOP is classified as a:**

- A) Primary barrier
- B) **Secondary barrier** ✅
- C) Tertiary barrier
- D) Not a barrier

---

### ❓ Question 3: Minimum Barriers

**Q: The minimum number of well control barriers required at any time is:**

- A) One
- B) **Two** ✅
- C) Three
- D) Depends on operation

---

### ❓ Question 4: Barrier Independence

**Q: Why must barriers be independent?**

- A) To save money
- B) For easier testing
- C) **So if one fails, the other still works** ✅
- D) To meet regulations only

---

### ❓ Question 5: Barrier Testing

**Q: Barriers should be:**

- A) Assumed to be working
- B) **Tested and verified before relying on them** ✅
- C) Tested only when problems occur
- D) Checked visually only

---

### ❓ Question 6: Which is NOT a Secondary Barrier?

**Q: Which of the following is NOT a secondary barrier?**

- A) BOP
- B) Casing
- C) **Mud column** ✅
- D) Wellhead

---

### ⚠️ Common Exam Traps:

| Trap | Correct Understanding |
|------|----------------------|
| "BOP is most important barrier" | Primary (mud) is first line of defense |
| "One good barrier is enough" | MINIMUM 2 required |
| "Secondary means less important" | Secondary means BACKUP, equally critical |

---

### 📝 Memory Tips:

🧠 Easy to Remember:

PRIMARY = PRESSURE = MUD
(The mud creates hydrostatic pressure)

SECONDARY = STEEL = BOP
(The BOP is made of steel)

"Mud is #1, BOP is #2"



---

### 🎯 Exam Key Points:

✅ Primary barrier = Mud weight (hydrostatic pressure)
✅ Secondary barrier = BOP system
✅ Minimum 2 barriers ALWAYS
✅ Barriers must be TESTED
✅ Never remove both simultaneously
        """
    },
        # ═══════════════════════════════════════════════════════
    # MODULE 2: PRESSURE CALCULATIONS
    # ═══════════════════════════════════════════════════════
    
    "Formation Pressure": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Formation Pressure؟

**Formation Pressure = ضغط السوائل جوا الصخور** 🪨

تحت الأرض، في سوائل (بترول، غاز، مياه) محبوسة في الصخور.
هذه السوائل **مضغوطة** بسبب وزن الصخور فوقيها!

---

### 📊 أنواع ضغط التكوين:

| النوع | المعنى | الـ Gradient |
|-------|--------|--------------|
| **Normal** 🟢 | ضغط طبيعي | 0.465 psi/ft |
| **Abnormal** 🔴 | ضغط أعلى من الطبيعي | > 0.465 psi/ft |
| **Subnormal** 🔵 | ضغط أقل من الطبيعي | < 0.465 psi/ft |

---

### 🔢 إزاي نحسب Formation Pressure؟

**لو عندنا SIDPP (بعد الـ Shut-in):**

<div class="formula-box">
FP = HP + SIDPP
</div>

**أو بالتفصيل:**

FP = (0.052 × MW × TVD) + SIDPP



---

### 📝 مثال:

**المعطيات:**
- MW = 10 ppg
- TVD = 10,000 ft
- SIDPP = 400 psi

**الحل:**

HP = 0.052 × 10 × 10,000 = 5,200 psi
FP = 5,200 + 400 = 5,600 psi



---

### 💡 تذكر:

> **"SIDPP بيقولك قد إيه التكوين أقوى من الطين"**
> 
> **"FP = HP + الفرق (SIDPP)"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📐 Formation Pressure Calculation:

**Method 1: Using SIDPP (After Shut-in)**

FP = HP + SIDPP
FP = (0.052 × MW × TVD) + SIDPP



**Method 2: Using Gradient**

FP = FP_gradient × TVD



---

### 📊 Pressure Gradients Reference:

| Fluid/Condition | Gradient (psi/ft) | Equivalent MW (ppg) |
|-----------------|-------------------|---------------------|
| Fresh Water | 0.433 | 8.33 |
| **Normal Pore Pressure** | **0.465** | **8.94** |
| Seawater | 0.444 | 8.55 |
| Oil (typical) | 0.35 - 0.40 | 6.7 - 7.7 |
| Gas | 0.05 - 0.15 | 1 - 3 |

---

### 🔬 Causes of Abnormal Pressure:

| Cause | Mechanism |
|-------|-----------|
| **Undercompaction** | Rapid burial, fluids can't escape |
| **Tectonic Activity** | Compression forces |
| **Aquathermal** | Temperature increase expands fluid |
| **Hydrocarbon Generation** | Kerogen → Oil/Gas creates pressure |
| **Osmosis** | Fluid migration through shales |
| **Charging** | Connected to deeper high-pressure zone |

---

### 📊 Worked Examples:

#### **Example 1: Calculate FP**

**Given:**
- TVD = 12,000 ft
- MW = 11 ppg
- SIDPP = 350 psi

**Solution:**

HP = 0.052 × 11 × 12,000 = 6,864 psi
FP = HP + SIDPP
FP = 6,864 + 350 = 7,214 psi



---

#### **Example 2: Calculate FP Gradient**

**Given:**
- FP = 7,214 psi
- TVD = 12,000 ft

**Solution:**

FP Gradient = FP / TVD
FP Gradient = 7,214 / 12,000
FP Gradient = 0.601 psi/ft

Equivalent MW = 0.601 / 0.052 = 11.56 ppg



This is ABNORMAL pressure (> 0.465 psi/ft)

---

### ⚠️ Important Notes:

| Point | Explanation |
|-------|-------------|
| **Use SIDPP** | Not SICP for FP calculation |
| **TVD only** | Never use MD |
| **Stabilized pressures** | Wait for pressures to stabilize |
| **FP gradient** | Helps compare with normal |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Direct FP Calculation

**Q: Calculate formation pressure given:**
- **TVD = 12,000 ft**
- **MW = 11 ppg**
- **SIDPP = 350 psi**

- A) 6,864 psi
- B) 7,000 psi
- C) **7,214 psi** ✅
- D) 7,500 psi

**Solution:**

HP = 0.052 × 11 × 12,000 = 6,864 psi
FP = 6,864 + 350 = 7,214 psi ✅



---

### ❓ Type 2: Normal Pressure Definition

**Q: Normal formation pressure gradient is:**

- A) 0.433 psi/ft
- B) **0.465 psi/ft** ✅
- C) 0.520 psi/ft
- D) 0.624 psi/ft

---

### ❓ Type 3: Which Pressure to Use?

**Q: To calculate formation pressure after shut-in, use:**

- A) SICP
- B) **SIDPP** ✅
- C) Both SIDPP and SICP
- D) Pump pressure

**💡 SIDPP reflects pressure at bit depth = formation pressure!**

---

### ❓ Type 4: Identify Pressure Type

**Q: FP gradient = 0.55 psi/ft. This is:**

- A) Normal pressure
- B) **Abnormal pressure** ✅
- C) Subnormal pressure
- D) Cannot determine

**💡 0.55 > 0.465 = Abnormal!**

---

### ⚠️ Common Traps:

| Trap | Correct Approach |
|------|------------------|
| Using SICP for FP | Use **SIDPP only** |
| Using MD instead of TVD | **Always use TVD** |
| Forgetting to add SIDPP | FP = HP **+ SIDPP** |

---

### 📝 Quick Reference:

Normal: 0.465 psi/ft = 8.94 ppg
Freshwater: 0.433 psi/ft = 8.33 ppg

If gradient > 0.465 → ABNORMAL
If gradient < 0.465 → SUBNORMAL


        """
    },
    
    "Pressure Gradients": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Gradient؟

**Gradient = معدل تغير الضغط مع العمق**

يعني كل ما تنزل **1 قدم**، الضغط بيزيد بكام؟

---

### 🔢 المعادلة:

<div class="formula-box">
Gradient = 0.052 × MW
</div>

**الوحدة:** psi/ft (رطل لكل بوصة مربعة لكل قدم)

---

### 📊 أمثلة سريعة:

| وزن الطين | الـ Gradient |
|-----------|--------------|
| 8.33 ppg (مياه) | 0.433 psi/ft |
| 10 ppg | 0.52 psi/ft |
| 12 ppg | 0.624 psi/ft |
| 14 ppg | 0.728 psi/ft |

---

### 📝 مثال حسابي:

**طين وزنه 13 ppg، إيه الـ Gradient؟**

Gradient = 0.052 × 13
Gradient = 0.676 psi/ft



**يعني كل قدم بتنزله، الضغط بيزيد 0.676 psi!**

---

### 🔄 العكس: من Gradient لـ MW

**لو الـ Gradient = 0.572 psi/ft، إيه الـ MW؟**

MW = Gradient / 0.052
MW = 0.572 / 0.052
MW = 11 ppg



---

### 💡 تذكر:

> **"الـ Gradient هو 0.052 × وزن الطين"**
> 
> **"كل ما الطين أثقل، الـ Gradient أعلى"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📐 Gradient Formulas:

**Calculate Gradient from MW:**

Gradient (psi/ft) = 0.052 × MW (ppg)



**Calculate MW from Gradient:**

MW (ppg) = Gradient (psi/ft) / 0.052



---

### 📊 Standard Gradients:

| Material | Gradient (psi/ft) | MW (ppg) |
|----------|-------------------|----------|
| Fresh Water | 0.433 | 8.33 |
| Normal Pore Pressure | 0.465 | 8.94 |
| Seawater | 0.444 | 8.55 |
| Light Oil | 0.35 | 6.73 |
| Heavy Oil | 0.40 | 7.69 |
| Gas (typical) | 0.10 | 1.92 |

---

### 🔢 Conversion Table:

| ppg | psi/ft | sg |
|-----|--------|-----|
| 8.33 | 0.433 | 1.00 |
| 9 | 0.468 | 1.08 |
| 10 | 0.520 | 1.20 |
| 11 | 0.572 | 1.32 |
| 12 | 0.624 | 1.44 |
| 13 | 0.676 | 1.56 |
| 14 | 0.728 | 1.68 |
| 15 | 0.780 | 1.80 |
| 16 | 0.832 | 1.92 |
| 17 | 0.884 | 2.04 |
| 18 | 0.936 | 2.16 |

---

### 📊 Using Gradients:

**Calculate Pressure at Depth:**

Pressure = Gradient × TVD



**Example:**

Gradient = 0.52 psi/ft
TVD = 10,000 ft

Pressure = 0.52 × 10,000 = 5,200 psi



---

### ⚠️ Key Points:

| Concept | Explanation |
|---------|-------------|
| **Gradient is constant** | Same gradient at all depths for same fluid |
| **Pressure increases** | Linearly with depth |
| **Heavier fluid** | Higher gradient, more pressure per foot |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Calculate Gradient

**Q: What gradient does 13 ppg mud create?**

- A) 0.520 psi/ft
- B) 0.624 psi/ft
- C) **0.676 psi/ft** ✅
- D) 0.728 psi/ft

**Solution:**

Gradient = 0.052 × 13 = 0.676 psi/ft ✅



---

### ❓ Type 2: Calculate MW from Gradient

**Q: What mud weight creates a gradient of 0.572 psi/ft?**

- A) 10 ppg
- B) **11 ppg** ✅
- C) 12 ppg
- D) 13 ppg

**Solution:**

MW = 0.572 / 0.052 = 11 ppg ✅



---

### ❓ Type 3: Pressure from Gradient

**Q: Mud gradient = 0.52 psi/ft, TVD = 8,000 ft. Calculate HP.**

- A) 4,000 psi
- B) **4,160 psi** ✅
- C) 4,500 psi
- D) 5,200 psi

**Solution:**

HP = Gradient × TVD
HP = 0.52 × 8,000 = 4,160 psi ✅



---

### ❓ Type 4: Compare Gradients

**Q: Formation gradient = 0.52 psi/ft. MW = 10 ppg. The well is:**

- A) **Balanced** ✅
- B) Overbalanced
- C) Underbalanced
- D) Cannot determine

**Solution:**

Mud gradient = 0.052 × 10 = 0.52 psi/ft
Formation gradient = 0.52 psi/ft

They are EQUAL → Balanced



---

### 📝 Quick Mental Math:

🧠 Memorize these:
10 ppg = 0.52 psi/ft
12 ppg = 0.624 psi/ft
14 ppg = 0.728 psi/ft
16 ppg = 0.832 psi/ft

Rule: Each 1 ppg ≈ 0.052 psi/ft increase


        """
    },
    
    "Equivalent Circulating Density (ECD)": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ ECD؟

**ECD = كثافة الطين الفعلية أثناء الضخ** 🔄

---

### 🤔 ليه الـ ECD مختلف عن الـ MW؟

لما المضخة شغالة:
- الطين **بيتحرك** في البئر
- الحركة دي بتعمل **احتكاك**
- الاحتكاك ده **بيزود الضغط**!

---

### 📐 المعادلة:

<div class="formula-box">
ECD = MW + (APL / 0.052 / TVD)
</div>

**حيث:**
- **ECD** = الكثافة الفعلية (ppg)
- **MW** = وزن الطين الحقيقي (ppg)
- **APL** = Annular Pressure Loss (psi)
- **TVD** = العمق الرأسي (ft)

---

### ⚠️ القاعدة الذهبية:

## **ECD دايماً > MW** 📈

**مستحيل يكون ECD أقل من MW!**

---

### 📝 مثال:

**المعطيات:**
- MW = 11 ppg
- APL = 312 psi
- TVD = 12,000 ft

**الحل:**

ECD = 11 + (312 / 0.052 / 12,000)
ECD = 11 + (312 / 624)
ECD = 11 + 0.5
ECD = 11.5 ppg



---

### 💡 إيه اللي بيأثر على ECD؟

| العامل | التأثير |
|--------|---------|
| **سرعة الضخ ↑** | ECD ↑ |
| **Annulus ضيق** | ECD ↑ |
| **طين ثقيل/لزج** | ECD ↑ |
| **بئر عميق** | ECD ↑ |

---

### 🚨 ليه ده مهم؟

لو الـ ECD أعلى من **Fracture Pressure**:
> **هتكسر التكوين = Lost Circulation!** 😱
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📐 ECD Formula:

ECD = MW + (APL / (0.052 × TVD))



**Alternative form:**

ECD = MW + (Annular Friction / TVD in ppg)



---

### 🔬 Components of ECD:

┌─────────────────────────────────────────┐
│ ECD │
│ ┌───────────────┬───────────────┐ │
│ │ Static MW │ Dynamic │ │
│ │ (Base) │ Addition │ │
│ │ │ (APL) │ │
│ └───────────────┴───────────────┘ │
└─────────────────────────────────────────┘



---

### 📊 Factors Affecting ECD:

| Factor | Effect on ECD | Reason |
|--------|---------------|--------|
| **Higher Flow Rate** | Increases | More friction |
| **Smaller Annulus** | Increases | Higher velocity |
| **Higher Mud Weight** | Increases | Base MW higher |
| **Higher Viscosity** | Increases | More friction |
| **Longer Well** | May increase | More cumulative friction |

---

### 📊 Worked Examples:

#### **Example 1: Basic ECD**

**Given:**
- MW = 11 ppg
- APL = 312 psi
- TVD = 12,000 ft

**Solution:**

ECD = MW + (APL / (0.052 × TVD))
ECD = 11 + (312 / (0.052 × 12,000))
ECD = 11 + (312 / 624)
ECD = 11 + 0.5
ECD = 11.5 ppg



---

#### **Example 2: Find APL from ECD**

**Given:**
- ECD = 12.3 ppg
- MW = 11.8 ppg
- TVD = 10,000 ft

**Solution:**

APL = (ECD - MW) × 0.052 × TVD
APL = (12.3 - 11.8) × 0.052 × 10,000
APL = 0.5 × 520
APL = 260 psi



---

### ⚠️ ECD vs Fracture Gradient:

Safe Operating Condition:

Formation < ECD < Fracture
Pressure ↑ Pressure
Must stay
in this
window!



**If ECD > Fracture Pressure:**
- Formation breaks
- Lost circulation occurs
- Possible underground blowout

---

### 📊 Comparison Table:

| Condition | MW | ECD | Status |
|-----------|-----|-----|--------|
| Static (not pumping) | 11.0 ppg | 11.0 ppg | Equal |
| Circulating (slow) | 11.0 ppg | 11.3 ppg | ECD > MW |
| Circulating (fast) | 11.0 ppg | 11.8 ppg | ECD >> MW |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Calculate ECD

**Q: Calculate ECD given MW=11 ppg, APL=312 psi, TVD=12,000 ft**

- A) 11.0 ppg
- B) **11.5 ppg** ✅
- C) 12.0 ppg
- D) 12.5 ppg

**Solution:**

ECD = 11 + (312 / 0.052 / 12,000)
ECD = 11 + 0.5 = 11.5 ppg ✅



---

### ❓ Type 2: ECD vs MW Relationship

**Q: ECD is ALWAYS:**

- A) Less than MW
- B) Equal to MW
- C) **Greater than MW** ✅
- D) Zero when not circulating

**💡 When not circulating, ECD = MW (no friction)**

---

### ❓ Type 3: Calculate APL

**Q: ECD = 12.5 ppg, MW = 12 ppg, TVD = 10,000 ft. Find APL.**

- A) 200 psi
- B) **260 psi** ✅
- C) 300 psi
- D) 350 psi

**Solution:**

APL = (ECD - MW) × 0.052 × TVD
APL = (12.5 - 12) × 0.052 × 10,000
APL = 0.5 × 520 = 260 psi ✅



---

### ❓ Type 4: Effect of Flow Rate

**Q: Increasing pump rate will cause ECD to:**

- A) Decrease
- B) Stay the same
- C) **Increase** ✅
- D) Become zero

---

### ❓ Type 5: When ECD = MW

**Q: ECD equals MW when:**

- A) Pumping at high rate
- B) **Not circulating (static)** ✅
- C) In a horizontal well
- D) Using water-based mud

---

### ⚠️ Key Exam Points:

✅ ECD > MW (always when circulating)
✅ ECD = MW (only when static)
✅ Higher pump rate = Higher ECD
✅ Narrow annulus = Higher ECD
✅ ECD must not exceed fracture pressure


        """
    },
    
    "Bottomhole Pressure Calculations": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ BHP؟

**BHP = Bottomhole Pressure = الضغط في قاع البئر** ⬇️

ده الضغط اللي التكوين بيحس بيه!

---

### 📊 نوعين من BHP:

| الحالة | الاسم | المعادلة |
|--------|-------|----------|
| **واقف (مش بتضخ)** | Static BHP | BHP = HP |
| **شغال (بتضخ)** | Dynamic BHP | BHP = HP + APL |

---

### 🔢 المعادلات:

**Static (مفيش ضخ):**

BHP = 0.052 × MW × TVD



**Dynamic (في ضخ):**

BHP = (0.052 × MW × TVD) + APL



---

### 📝 مثال:

**المعطيات:**
- MW = 12 ppg
- TVD = 10,000 ft
- APL = 200 psi (لما بتضخ)

**Static BHP:**

BHP = 0.052 × 12 × 10,000
BHP = 6,240 psi



**Dynamic BHP:**

BHP = 6,240 + 200
BHP = 6,440 psi



---

### 💡 القاعدة:

> **"لما بتضخ، الضغط بيزيد بسبب الاحتكاك"**
> 
> **"Dynamic BHP دايماً > Static BHP"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📐 BHP Formulas:

**Static BHP (Not Circulating):**

BHP = HP = 0.052 × MW × TVD



**Dynamic BHP (Circulating):**

BHP = HP + APL = (0.052 × MW × TVD) + APL



**Using ECD:**

BHP = 0.052 × ECD × TVD



---

### 📊 Components of Dynamic BHP:

┌─────────────────────────────────────────┐
│ Dynamic BHP │
│ ┌─────────────────┬─────────────────┐ │
│ │ Hydrostatic │ Annular │ │
│ │ Pressure │ Pressure Loss │ │
│ │ HP │ APL │ │
│ │ │ │ │
│ │ 0.052×MW×TVD │ (friction) │ │
│ └─────────────────┴─────────────────┘ │
└─────────────────────────────────────────┘



---

### 🔢 Worked Examples:

#### **Example 1: Static BHP**

**Given:**
- MW = 11.5 ppg
- TVD = 12,000 ft

**Solution:**

BHP = 0.052 × 11.5 × 12,000
BHP = 7,176 psi



---

#### **Example 2: Dynamic BHP**

**Given:**
- MW = 11.5 ppg
- TVD = 12,000 ft
- APL = 350 psi

**Solution:**

BHP = (0.052 × 11.5 × 12,000) + 350
BHP = 7,176 + 350
BHP = 7,526 psi



---

### ⚖️ BHP vs Formation Pressure:

| Condition | Result |
|-----------|--------|
| BHP > FP | Overbalanced (safe) |
| BHP = FP | Balanced (risky) |
| BHP < FP | **Underbalanced (KICK!)** |

---

### ⚠️ Critical Concept:

**During well kill, maintain CONSTANT BHP!**

If BHP drops → More kick influx
If BHP rises → Possible fracture

GOAL: Keep BHP constant and slightly > FP


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Static BHP

**Q: Calculate static BHP: MW=12 ppg, TVD=10,000 ft**

- A) 5,200 psi
- B) **6,240 psi** ✅
- C) 7,280 psi
- D) 8,320 psi

**Solution:**

BHP = 0.052 × 12 × 10,000 = 6,240 psi ✅



---

### ❓ Type 2: Dynamic BHP

**Q: Calculate dynamic BHP: MW=11 ppg, TVD=10,000 ft, APL=200 psi**

- A) 5,720 psi
- B) **5,920 psi** ✅
- C) 6,240 psi
- D) 6,440 psi

**Solution:**

BHP = (0.052 × 11 × 10,000) + 200
BHP = 5,720 + 200 = 5,920 psi ✅



---

### ❓ Type 3: Comparison

**Q: Dynamic BHP compared to Static BHP is:**

- A) Less
- B) Equal
- C) **Greater** ✅
- D) Depends on mud type

---

### ❓ Type 4: Well Kill Principle

**Q: During well kill operations, BHP should be:**

- A) Maximized
- B) Minimized
- C) **Constant and ≥ Formation Pressure** ✅
- D) Zero

---

### 📝 Key Points:

✅ Static BHP = HP only
✅ Dynamic BHP = HP + APL
✅ Dynamic > Static (always)
✅ During kill: Keep BHP constant!


        """
    },
    
    "MAASP Calculations": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ MAASP؟

**MAASP = Maximum Allowable Annular Surface Pressure**

**بالعربي:** أقصى ضغط مسموح على السطح في الـ Annulus!

---

### 🤔 ليه ده مهم؟

لو الضغط على السطح زاد عن الـ MAASP:
> **هيكسر التكوين عند الـ Shoe!** 💥
> 
> **= Lost Circulation أو Underground Blowout!**

---

### 📐 المعادلة:

<div class="formula-box">
MAASP = (LOT - MW) × 0.052 × Shoe TVD
</div>

**حيث:**
- **LOT** = Leak Off Test (الضغط اللي بيكسر التكوين) - ppg
- **MW** = Current Mud Weight - ppg
- **Shoe TVD** = عمق الـ Casing Shoe - ft

---

### 📝 مثال:

**المعطيات:**
- LOT = 14.5 ppg
- MW = 11 ppg
- Shoe TVD = 6,000 ft

**الحل:**

MAASP = (14.5 - 11) × 0.052 × 6,000
MAASP = 3.5 × 0.052 × 6,000
MAASP = 3.5 × 312
MAASP = 1,092 psi



**يعني لو الضغط على السطح زاد عن 1,092 psi، هتكسر التكوين!**

---

### ⚠️ قاعدة مهمة:

| إذا... | MAASP... |
|--------|----------|
| **زودت الـ MW** | **يقل!** ↓ |
| **قللت الـ MW** | **يزيد!** ↑ |

**ليه؟** علشان الفرق بين LOT و MW بيقل!
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📐 MAASP Formula:

MAASP = (LOT - MW) × 0.052 × Shoe TVD



**Or using FIT (Formation Integrity Test):**

MAASP = (FIT EMW - MW) × 0.052 × Shoe TVD



---

### 📊 Key Concepts:

| Term | Definition |
|------|------------|
| **LOT** | Leak-Off Test - pressure at which formation breaks |
| **FIT** | Formation Integrity Test - confirms formation can hold specific pressure |
| **Shoe TVD** | True Vertical Depth of casing shoe |
| **EMW** | Equivalent Mud Weight |

---

### 🔬 Why Shoe TVD?

The casing shoe is the **weakest point** in the open hole section.


     Surface
        │
Casing  │████████████
        │████████████

Shoe TVD → ╠════════════ ← Weakest point!
│
│ Open hole
│
Bottom



---

### 📊 Worked Examples:

#### **Example 1: Calculate MAASP**

**Given:**
- LOT = 14.5 ppg
- MW = 11 ppg
- Shoe TVD = 6,000 ft

**Solution:**

MAASP = (14.5 - 11) × 0.052 × 6,000
MAASP = 3.5 × 0.052 × 6,000
MAASP = 1,092 psi



---

#### **Example 2: Effect of Increasing MW**

**Same well, but now MW = 12 ppg:**

MAASP = (14.5 - 12) × 0.052 × 6,000
MAASP = 2.5 × 0.052 × 6,000
MAASP = 780 psi



**MAASP decreased from 1,092 to 780 psi!**

---

### ⚠️ Important Rules:

| Rule | Explanation |
|------|-------------|
| **Higher MW = Lower MAASP** | Less margin before fracture |
| **Use current MW** | Not original MW |
| **Use Shoe TVD** | Not current bit depth |
| **Never exceed MAASP** | Risk of underground blowout |

---

### 🚨 During Well Kill:

**MAASP changes as you pump kill mud!**

Time 0: Light mud → Higher MAASP
↓
Kill mud reaching shoe → MAASP decreasing
↓
Kill mud past shoe → MAASP at minimum



**Must recalculate MAASP when MW changes!**
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Type 1: Calculate MAASP

**Q: Calculate MAASP: LOT=14.5 ppg, MW=11 ppg, Shoe TVD=6,000 ft**

- A) 780 psi
- B) **1,092 psi** ✅
- C) 1,200 psi
- D) 1,500 psi

**Solution:**

MAASP = (14.5 - 11) × 0.052 × 6,000
MAASP = 3.5 × 312 = 1,092 psi ✅



---

### ❓ Type 2: Effect of MW Change

**Q: If mud weight increases, MAASP will:**

- A) Increase
- B) **Decrease** ✅
- C) Stay the same
- D) Double

**💡 Higher MW → Smaller (LOT - MW) → Lower MAASP**

---

### ❓ Type 3: Which Depth?

**Q: For MAASP calculation, use:**

- A) Total depth
- B) **Casing shoe TVD** ✅
- C) Measured depth
- D) Bit depth

---

### ❓ Type 4: Exceeding MAASP

**Q: If surface pressure exceeds MAASP during a kill operation:**

- A) Nothing happens
- B) **Formation may fracture at shoe** ✅
- C) Kick will stop
- D) BOP will fail

---

### ❓ Type 5: Calculate New MAASP

**Q: Original MAASP=1,092 psi with MW=11 ppg. New MW=13 ppg, LOT=14.5 ppg, Shoe=6,000 ft. New MAASP?**

- A) **468 psi** ✅
- B) 780 psi
- C) 1,092 psi
- D) 1,500 psi

**Solution:**

MAASP = (14.5 - 13) × 0.052 × 6,000
MAASP = 1.5 × 312 = 468 psi ✅



---

### ⚠️ Exam Traps:

| Trap | Correct Approach |
|------|------------------|
| Using bit depth | Use **SHOE TVD** |
| Using original MW | Use **CURRENT MW** |
| Thinking MAASP is fixed | **MAASP changes with MW** |

---

### 📝 Memory Aid:

🧠 MAASP = (LOT - MW) × 0.052 × Shoe

Think of it as:
"How much EXTRA pressure can the shoe take?"

LOT - MW = Safety margin in ppg
× 0.052 × Shoe = Convert to psi


        """
    },
    
    # ═══════════════════════════════════════════════════════
    # MODULE 3: KICK DETECTION
    # ═══════════════════════════════════════════════════════
    
    "Primary Kick Indicators": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هي الـ Primary Indicators؟

**Primary = العلامات الأكيدة المباشرة اللي بتأكد إن في Kick!**

لما تشوف أي واحدة منهم → **تصرف فوراً!**

---

### 🚨 العلامات الأربعة الرئيسية:

---

#### **1️⃣ Pit Gain (زيادة مستوى الطين)** 📈

**إيه اللي بيحصل؟**
- مستوى الطين في الـ Tanks بيزيد
- يعني حاجة دخلت البئر!

**⭐ ده أهم وأوضح علامة!**

---

#### **2️⃣ Flow Rate Increase (زيادة معدل الرجوع)** ⬆️

**إيه اللي بيحصل؟**
- الطين بيرجع أكتر من اللي بتضخه
- المضخة على نفس السرعة، بس الـ Returns زادت!

---

#### **3️⃣ Pump Pressure Decrease (نقص ضغط المضخة)** ⬇️

**إيه اللي بيحصل؟**
- ضغط المضخة قل فجأة
- ليه؟ علشان حاجة خفيفة (غاز) دخلت البئر

---

#### **4️⃣ Flow with Pumps Off (تدفق والمضخة واقفة)** 💧

**إيه اللي بيحصل؟**
- وقفت المضخة بس البئر لسه بيطلع طين!
- ده أخطر علامة!

---

### ⚡ التصرف:

أي علامة من دول:
↓

    وقف المضخة!
    ↓
    ارفع الـ Kelly
    ↓
    اقفل الـ BOP!
    ↓
    سجل SIDPP و SICP



---

### 💡 تذكر:

> **"شفت Primary → Shut In فوراً!"**
> 
> **"Pit Gain هو الملك! 👑"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Primary Indicators Detailed:

| Indicator | Physical Sign | Mechanism |
|-----------|---------------|-----------|
| **Pit Gain** | Tank levels increase | Formation fluid displaces mud |
| **Flow Increase** | Returns > Pump output | Formation pressure pushing fluid |
| **Pump Pressure Drop** | Sudden SPP decrease | Lighter influx reduces HP |
| **Flow when Static** | Returns with pumps off | FP > HP (positive kick) |

---

### 🔬 Why Each Happens:

#### **Pit Gain:**

Before Kick:
Pit Volume = 500 bbl

After 20 bbl Kick:
Pit Volume = 520 bbl ← 20 bbl increase!



#### **Flow Rate Increase:**

Pump Output: 400 gpm
Normal Returns: 400 gpm

With Kick:
Returns: 450+ gpm ← Formation adding fluid!



#### **Pump Pressure Decrease:**

Normal: BHP supported by mud column
With gas: Lighter column = Less BHP needed
Result: Pump works less hard = Lower SPP



---

### 📊 Sensitivity Comparison:

| Indicator | Detection Speed | Reliability |
|-----------|-----------------|-------------|
| Pit Gain | Immediate | ⭐⭐⭐⭐⭐ Highest |
| Flow Increase | Immediate | ⭐⭐⭐⭐ High |
| Pump Pressure | Slight delay | ⭐⭐⭐ Medium |
| Static Flow | Immediate | ⭐⭐⭐⭐⭐ Highest |

---

### ⚠️ Required Response:

**Immediate Actions (< 2 minutes):**

    STOP → Stop rotary, stop pumps
    RAISE → Raise kelly above rotary table
    CLOSE → Close BOP (hard shut-in preferred)
    RECORD → Note SIDPP and SICP
    NOTIFY → Call supervisor



---

### 📊 Monitoring Requirements:

| Parameter | Accuracy | Frequency |
|-----------|----------|-----------|
| Pit Volume | ± 1 bbl | Continuous |
| Flow Rate | ± 10% | Continuous |
| Pump Pressure | ± 50 psi | Continuous |
| Returns Flow | Visual | Continuous |

---

### 🔴 Critical: Don't Ignore Small Signs!

⚠️ Even 1-2 bbl pit gain:
→ Should trigger investigation
→ Flow check required
→ Better safe than sorry!


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Most Reliable

**Q: The MOST reliable primary kick indicator is:**

- A) Drilling break
- B) **Pit volume gain** ✅
- C) Connection gas
- D) Mud weight decrease

---

### ❓ Question 2: Identify Primary

**Q: All are PRIMARY kick indicators EXCEPT:**

- A) Pit gain
- B) Flow increase
- C) Pump pressure decrease
- D) **Drilling break** ✅

---

### ❓ Question 3: Pump Pressure

**Q: Pump pressure decreases during a kick because:**

- A) Pump is failing
- B) **Lighter influx reduces hydrostatic pressure** ✅
- C) Hole is getting bigger
- D) Mud weight increased

---

### ❓ Question 4: First Action

**Q: Upon noticing a 15 bbl pit gain, FIRST action is:**

- A) Increase pump rate
- B) Continue drilling
- C) **Stop pumps** ✅
- D) Call the supervisor

---

### ❓ Question 5: Flow Check

**Q: Well is flowing with pumps off. This indicates:**

- A) Normal circulation
- B) **Kick (positive flow)** ✅
- C) U-tube effect
- D) Pump malfunction

---

### 📝 Key Exam Points:

PRIMARY INDICATORS (memorize!):
P - Pit gain ← MOST RELIABLE
F - Flow increase
P - Pump pressure drop
F - Flow with pumps off

Action: IMMEDIATE SHUT-IN!



---

### ⚠️ Exam Trap Alert:

| They might say... | Correct answer... |
|-------------------|-------------------|
| "Most important" | Pit gain |
| "First action" | Stop pumps |
| "Drilling break confirms kick" | NO! It's secondary |
        """
    },
    
    "Secondary Kick Indicators": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هي الـ Secondary Indicators؟

**Secondary = علامات تحذيرية - بتقولك "انتبه!"**

**مش بتأكد إن في Kick، بس بتحذرك!**

---

### 🟡 العلامات الثانوية:

---

#### **1️⃣ Drilling Break (زيادة سرعة الحفر)** ⚡

**إيه اللي بيحصل؟**
- سرعة الحفر زادت فجأة
- يعني دخلت في صخر لين أو مسامي

**ده بيحصل ليه؟**
- صخر مسامي = ممكن يكون فيه بترول أو غاز
- **انتبه واراقب!**

---

#### **2️⃣ Connection Gas (غاز وقت الوصلات)** 💨

**إيه اللي بيحصل؟**
- غاز بيطلع لما توقف تضيف Pipe
- السبب: الـ Swab effect

---

#### **3️⃣ Cut Mud (طين مقطوع)** 🔻

**إيه اللي بيحصل؟**
- وزن الطين قل
- السبب: غاز دخل الطين وخففه

---

#### **4️⃣ Torque/Drag Changes** 🔄

**إيه اللي بيحصل؟**
- تغير في مقاومة الدوران أو السحب
- ممكن يكون علامة على مشاكل في الحفرة

---

### 📊 الفرق بين Primary و Secondary:

| Primary | Secondary |
|---------|-----------|
| **أكيد في Kick** | **ممكن يكون في Kick** |
| **Shut in فوراً!** | **راقب واعمل Flow Check** |

---

### ⚡ التصرف الصحيح:

شفت Secondary Indicator:
↓
راقب باهتمام
↓
اعمل Flow Check
↓
لو في Flow → Shut In!


        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Secondary Indicators Classification:

| Indicator | Description | Possible Cause |
|-----------|-------------|----------------|
| **Drilling Break** | Sudden ROP increase | Porous/fractured zone |
| **Connection Gas** | Gas peaks at connections | Swab effect, gas zone |
| **Trip Gas** | Gas after tripping | Swab, underbalanced |
| **Cut Mud** | Reduced MW | Gas contamination |
| **Torque Change** | Changed string resistance | Hole swelling, sloughing |
| **Fill Shortage** | Hole not taking full volume | Possible flow |

---

### 🔬 Why These Are Secondary:

**They don't CONFIRM a kick, they SUGGEST possible conditions:**

Drilling Break:
├── Could be: Porous zone with kick potential
├── Could be: Normal softer formation
└── Action: Monitor, flow check

Connection Gas:
├── Could be: Gas zone penetrated
├── Could be: Normal background gas
└── Action: Monitor levels, check mud

Cut Mud:
├── Could be: Gas contamination
├── Could be: Solids settling
└── Action: Check MW, degas if needed



---

### 📊 Response Protocols:

| Indicator | Immediate Action | Follow-up |
|-----------|------------------|-----------|
| Drilling Break | Slow ROP, monitor | Flow check |
| Connection Gas | Check gas levels | Monitor trend |
| Trip Gas | Check volumes | Calculate swab |
| Cut Mud | Check true MW | Degas mud |

---

### ⚠️ When to Escalate:

**Convert to Primary Response if:**
- Multiple secondary indicators occur together
- Trend is worsening
- Flow check shows positive flow
- Pit gain observed

Secondary + Secondary + Worsening Trend
↓
Treat as Primary!
↓
Shut In!


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Identify Secondary

**Q: Which is a SECONDARY kick indicator?**

- A) Pit gain
- B) Flow increase
- C) **Drilling break** ✅
- D) Flow with pumps off

---

### ❓ Question 2: Definition

**Q: Secondary indicators are:**

- A) More reliable than primary
- B) **Warning signs requiring increased monitoring** ✅
- C) Ignored during drilling
- D) Only important during tripping

---

### ❓ Question 3: All Are Secondary EXCEPT

**Q: All are SECONDARY indicators EXCEPT:**

- A) Drilling break
- B) Connection gas
- C) Cut mud
- D) **Pit gain** ✅

---

### ❓ Question 4: Response

**Q: Appropriate response to drilling break:**

- A) Shut in immediately
- B) Ignore and continue
- C) **Monitor closely and flow check** ✅
- D) Increase ROP

---

### ❓ Question 5: Conversion

**Q: When should secondary indicators be treated as primary?**

- A) Never
- B) Only at night
- C) **When multiple occur or flow check is positive** ✅
- D) Only during tripping

---

### 📝 Memory Aid:

SECONDARY = WARNING SIGNS

D - Drilling break
C - Connection gas
C - Cut mud
T - Torque changes
F - Fill shortage

Response: MONITOR + FLOW CHECK
(Not immediate shut-in unless confirmed)


        """
    },
    
    "Shut-in Procedures": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Shut-in؟

**Shut-in = قفل البئر بالـ BOP لما يحصل Kick!** 🔴

---

### 📋 الخطوات (احفظها!):

## **S.R.C.R**

| الخطوة | المعنى | التفاصيل |
|--------|--------|----------|
| **S - STOP** | وقف! | وقف الدوران + المضخة |
| **R - RAISE** | ارفع! | ارفع الـ Kelly فوق الـ Rotary |
| **C - CLOSE** | اقفل! | اقفل الـ BOP |
| **R - RECORD** | سجل! | سجل SIDPP و SICP |

---

### ⏱️ الوقت المستهدف:

## **أقل من دقيقتين!** ⚡

من أول ما تشك في Kick
↓
لحد ما تقفل البئر
↓
أقل من 2 دقيقة!



---

### 🔴 نوعين من الـ Shut-in:

#### **1️⃣ Hard Shut-in (الأسرع) ⚡**

اقفل الـ BOP أولاً
↓
بعدين افتح الـ Choke



**ده الـ Standard - استخدمه دايماً!**

---

#### **2️⃣ Soft Shut-in (أبطأ) 🐢**

افتح الـ Choke أولاً
↓
اقفل الـ BOP
↓
اقفل الـ Choke



**نادراً ما يستخدم - بس لو الـ Formation ضعيفة جداً**

---

### 💡 تذكر:

> **"STOP - RAISE - CLOSE - RECORD"**
> 
> **"Hard shut-in is STANDARD!"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📋 Complete Shut-in Procedure:

**Step-by-Step:**

    STOP
    ├── Stop rotary table
    ├── Stop pumps
    └── Set slips if needed

    RAISE
    ├── Pick up off bottom
    ├── Raise kelly above rotary
    └── Space out from tool joint

    CLOSE
    ├── Close BOP (annular first)
    ├── Verify closed position
    └── Open HCR (Hydraulic Control Remote) line

    RECORD
    ├── Note SIDPP (stabilized)
    ├── Note SICP (stabilized)
    ├── Note pit gain
    └── Note time of shut-in



---

### 🔴 Hard vs Soft Shut-in:

| Aspect | Hard Shut-in | Soft Shut-in |
|--------|--------------|--------------|
| **Sequence** | Close BOP → Open choke | Open choke → Close BOP → Close choke |
| **Speed** | Faster | Slower |
| **When Used** | Standard (most cases) | Weak formation only |
| **Risk** | Pressure spike | Larger kick volume |

---

### 📊 Hard Shut-in Procedure:

    Close BOP (annular)
    Open choke line valve (HCR)
    Monitor SIDPP and SICP
    Wait for pressures to stabilize



---

### 📊 Soft Shut-in Procedure:

    Open choke fully
    Close BOP (annular)
    Slowly close choke
    Monitor pressures during closure
    Record stabilized SIDPP and SICP



---

### ⏱️ Time Requirements:

| Phase | Target Time |
|-------|-------------|
| Detection to pumps off | < 30 seconds |
| Kelly raised | < 30 seconds |
| BOP closed | < 30 seconds |
| **Total shut-in** | **< 2 minutes** |

---

### ⚠️ Critical Points:

| Point | Explanation |
|-------|-------------|
| **Space out** | Keep tool joint away from rams |
| **Hard shut-in preferred** | Faster, limits kick size |
| **Wait for stabilization** | Pressures may take 5-15 min |
| **Verify closure** | Check position indicators |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: First Action

**Q: FIRST action when kick is detected:**

- A) Close BOP
- B) **Stop pumps** ✅
- C) Record pressures
- D) Call supervisor

---

### ❓ Question 2: Sequence

**Q: Correct shut-in sequence is:**

- A) Close BOP, Record pressures, Stop pumps
- B) **Stop pumps, Raise kelly, Close BOP, Record pressures** ✅
- C) Record pressures, Stop pumps, Close BOP
- D) Call supervisor, Stop pumps, Close BOP

---

### ❓ Question 3: Hard vs Soft

**Q: In hard shut-in, the sequence is:**

- A) Open choke, then close BOP
- B) **Close BOP, then open choke** ✅
- C) Close both simultaneously
- D) Open both, then close

---

### ❓ Question 4: Standard Method

**Q: Which shut-in method is considered STANDARD?**

- A) Soft shut-in
- B) **Hard shut-in** ✅
- C) Both equally
- D) Depends on crew preference

---

### ❓ Question 5: Target Time

**Q: Target time for complete shut-in is:**

- A) 5 minutes
- B) **Less than 2 minutes** ✅
- C) 10 minutes
- D) As fast as possible, no target

---

### ❓ Question 6: Space Out

**Q: Why is it important to space out before shutting in?**

- A) To save time
- B) To increase pit gain
- C) **To position tool joint away from rams** ✅
- D) To reduce pressure

---

### 📝 Memory Aid:

🧠 S.R.C.R = "Sir, Can Roger?"

S - STOP pumps
R - RAISE kelly
C - CLOSE BOP
R - RECORD pressures

Hard = Hard first (close BOP first)
Soft = Soft first (open choke first)


        """
    },
    
    "SIDPP and SICP": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هما SIDPP و SICP؟

بعد ما تقفل البئر (Shut-in)، هتلاحظ ضغطين على الـ Gauges:

---

#### **SIDPP = Shut-In Drill Pipe Pressure** 📊

**ضغط الـ Drill Pipe وأنت مقفل**

- ده الضغط على جهة الـ Drill String
- **بيقولك قد إيه ضغط التكوين أعلى من ضغط الطين**
- **بنستخدمه في الحسابات!** ✅

---

#### **SICP = Shut-In Casing Pressure** 📈

**ضغط الـ Casing/Annulus وأنت مقفل**

- ده الضغط على جهة الـ Annulus
- فيه الـ Kick (غاز/سائل) في المنطقة دي
- **عادة أعلى من SIDPP لو الـ kick غاز**

---

### 📊 المقارنة:

| لو... | يعني... |
|-------|---------|
| **SICP > SIDPP** | Kick غاز 💨 (خطر!) |
| **SICP ≈ SIDPP** | Kick سائل (بترول/مياه) |
| **SICP < SIDPP** | نادر جداً |

---

### 🔢 استخدام SIDPP:

**حساب ضغط التكوين:**

FP = HP + SIDPP



**حساب وزن طين القتل:**

KMW = OMW + (SIDPP / 0.052 / TVD)



---

### 💡 تذكر:

> **"SIDPP = للحسابات"** 📐
> 
> **"SICP = لمعرفة نوع الـ Kick"** 🔍
> 
> **"SICP > SIDPP = غاز = خطر!"** ⚠️
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Understanding SIDPP and SICP:


      Surface
┌─────────┬─────────┐
│  SIDPP  │  SICP   │
│   ↓     │   ↓     │
│ Drill   │ Annulus │
│ String  │         │
│         │  ████   │ ← Kick (influx)
│         │  ████   │
│         │         │
└─────────┴─────────┘
      Bit → Formation Pressure



---

### 📐 Key Formulas Using SIDPP:

**Formation Pressure:**

FP = HP + SIDPP
FP = (0.052 × MW × TVD) + SIDPP



**Kill Mud Weight:**

KMW = OMW + (SIDPP / (0.052 × TVD))



---

### 🔬 Why SICP ≠ SIDPP?

**In Drill Pipe (SIDPP side):**

BHP = HP(mud) + SIDPP



**In Annulus (SICP side):**

BHP = HP(mud) + HP(influx) + SICP



**Since influx is lighter than mud:**

HP(influx) < HP(mud) for same height
Therefore: SICP > SIDPP to balance BHP



---

### 📊 Kick Type Identification:

| Observation | Likely Kick Type |
|-------------|------------------|
| **SICP >> SIDPP** | Gas kick (large difference) |
| **SICP > SIDPP** | Gas or gas-cut oil |
| **SICP ≈ SIDPP** | Liquid (oil or water) |
| **High pit gain + SICP >> SIDPP** | Severe gas kick |

---

### 📊 Stabilization Time:

After Shut-in:
├── Gas kick: May take 5-15 min to stabilize
├── Liquid kick: Usually stabilizes faster
└── Large kick: May take longer

⚠️ Wait for both SIDPP and SICP to stabilize
before recording final values!



---

### ⚠️ Important Rules:

| Rule | Reason |
|------|--------|
| **Use SIDPP for calculations** | Direct path to BHP |
| **Never use SICP for FP** | Contaminated by influx |
| **Wait for stabilization** | Initial readings may be wrong |
| **Monitor both pressures** | Detect problems (plugged, etc.) |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Which Pressure?

**Q: To calculate formation pressure, use:**

- A) SICP
- B) **SIDPP** ✅
- C) Both SIDPP and SICP
- D) Pump pressure

---

### ❓ Question 2: Gas Kick Identification

**Q: SICP = 800 psi, SIDPP = 400 psi. This suggests:**

- A) Water kick
- B) Oil kick
- C) **Gas kick** ✅
- D) No kick

**💡 SICP > SIDPP indicates lighter fluid (gas)!**

---

### ❓ Question 3: Stabilization

**Q: After shut-in, you should:**

- A) Record pressures immediately
- B) **Wait for pressures to stabilize** ✅
- C) Start kill immediately
- D) Open the choke

---

### ❓ Question 4: Calculate FP

**Q: SIDPP = 350 psi, MW = 11 ppg, TVD = 12,000 ft. Calculate FP.**

- A) 6,864 psi
- B) 7,000 psi
- C) **7,214 psi** ✅
- D) 7,500 psi

**Solution:**

HP = 0.052 × 11 × 12,000 = 6,864 psi
FP = HP + SIDPP = 6,864 + 350 = 7,214 psi ✅



---

### ❓ Question 5: Why SICP Higher?

**Q: SICP is higher than SIDPP because:**

- A) Annulus is smaller
- B) **Lighter influx in annulus requires more surface pressure** ✅
- C) Drill pipe is blocked
- D) BOP is leaking

---

### 📝 Key Points:

✅ SIDPP = for calculations
✅ SICP = for kick identification
✅ SICP > SIDPP = gas kick
✅ Wait for stabilization
✅ FP = HP + SIDPP


        """
    },
    
    "Kick Analysis": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Kick Analysis؟

**بعد ما تقفل البئر، محتاج تعرف:**

1. **نوع الـ Kick** (غاز؟ بترول؟ مياه؟)
2. **حجم الـ Kick** (صغير؟ كبير؟)
3. **ضغط التكوين** (علشان تعرف وزن الطين المطلوب)

---

### 📊 نوع الـ Kick:

**من المقارنة بين SICP و SIDPP:**

| لو... | النوع |
|-------|-------|
| **SICP أعلى بكتير من SIDPP** | غاز 💨 (خطر!) |
| **SICP أعلى شوية من SIDPP** | غاز + بترول |
| **SICP ≈ SIDPP** | بترول أو مياه 💧 |

---

### 📊 حجم الـ Kick:

**من الـ Pit Gain:**

| Pit Gain | الحجم |
|----------|-------|
| 1-5 bbl | صغير ✅ |
| 5-20 bbl | متوسط ⚠️ |
| > 20 bbl | كبير 🔴 |

---

### 📊 ضغط التكوين:

**المعادلة:**

FP = HP + SIDPP



**أو:**

FP = (0.052 × MW × TVD) + SIDPP



---

### 📊 مثال كامل:

**المعطيات:**
- SIDPP = 400 psi
- SICP = 850 psi
- Pit Gain = 15 bbl
- MW = 10 ppg
- TVD = 10,000 ft

**التحليل:**

    نوع الـ Kick:
    SICP (850) >> SIDPP (400)
    الفرق = 450 psi
    ← ده غاز! ⚠️

    حجم الـ Kick:
    15 bbl = متوسط

    ضغط التكوين:
    FP = (0.052 × 10 × 10,000) + 400
    FP = 5,200 + 400 = 5,600 psi


        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📊 Complete Kick Analysis Process:

Step 1: Determine Kick Type
↓
Step 2: Calculate Kick Volume/Height
↓
Step 3: Calculate Formation Pressure
↓
Step 4: Calculate Kill Mud Weight
↓
Step 5: Plan Kill Operation



---

### 🔬 Kick Type Analysis:

**Using SICP vs SIDPP:**

| SICP - SIDPP | Likely Influx | Gravity (ppg) |
|--------------|---------------|---------------|
| Large (>300 psi) | Gas | 1-3 ppg |
| Moderate (100-300) | Gas + Oil | 3-6 ppg |
| Small (<100 psi) | Oil/Water | 6-9 ppg |

---

### 📐 Influx Gradient Calculation:

Influx Gradient = (SICP - SIDPP) / Influx Height

Influx Height = Pit Gain / Annular Capacity



**Example:**

SICP = 800 psi, SIDPP = 400 psi
Pit Gain = 20 bbl
Annular Capacity = 0.05 bbl/ft

Influx Height = 20 / 0.05 = 400 ft
Influx Gradient = (800 - 400) / 400 = 1.0 psi/ft

Influx MW = 1.0 / 0.052 = 19.2 ppg



Wait, that's too heavy. Let me recalculate...

Actually, the formula is:

Influx Gradient = Mud Gradient - ((SICP - SIDPP) / Influx Height)



---

### 📊 Formation Pressure Calculation:

FP = HP(mud) + SIDPP
FP = (0.052 × MW × TVD) + SIDPP



---

### 📊 Kill Mud Weight Calculation:

KMW = OMW + (SIDPP / (0.052 × TVD))



**With safety margin (+0.5 ppg trip margin):**

KMW = OMW + (SIDPP / (0.052 × TVD)) + 0.5



---

### 📊 Complete Analysis Example:

**Given:**
- SIDPP = 400 psi (stabilized)
- SICP = 850 psi (stabilized)
- Pit Gain = 20 bbl
- MW = 10 ppg
- TVD = 10,000 ft

**Analysis:**

    Kick Type:
    SICP - SIDPP = 850 - 400 = 450 psi
    Large difference → GAS KICK ⚠️

    Formation Pressure:
    FP = (0.052 × 10 × 10,000) + 400
    FP = 5,200 + 400 = 5,600 psi

    Kill Mud Weight:
    KMW = 10 + (400 / (0.052 × 10,000))
    KMW = 10 + (400 / 520)
    KMW = 10 + 0.77
    KMW = 10.77 ppg → Round to 10.8 ppg

    Severity Assessment:
        20 bbl gas kick = SIGNIFICANT
        Requires careful kill procedure
        Monitor MAASP carefully


        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Kick Type

**Q: SICP = 900 psi, SIDPP = 400 psi. The kick is most likely:**

- A) Water
- B) Oil
- C) **Gas** ✅
- D) Mud

**💡 Large difference = Light influx = Gas!**

---

### ❓ Question 2: Calculate KMW

**Q: SIDPP = 400 psi, OMW = 10 ppg, TVD = 10,000 ft. Calculate KMW.**

- A) 10.50 ppg
- B) **10.77 ppg** ✅
- C) 11.00 ppg
- D) 11.50 ppg

**Solution:**

KMW = 10 + (400 / (0.052 × 10,000))
KMW = 10 + (400 / 520)
KMW = 10 + 0.77 = 10.77 ppg ✅



---

### ❓ Question 3: Which Pressure?

**Q: For kick analysis calculations, which pressure is used?**

- A) SICP
- B) **SIDPP** ✅
- C) Pump pressure
- D) Casing burst pressure

---

### ❓ Question 4: Liquid Kick Sign

**Q: SICP approximately equals SIDPP. This indicates:**

- A) Gas kick
- B) **Liquid kick (oil or water)** ✅
- C) No kick
- D) BOP failure

---

### ❓ Question 5: Calculate FP

**Q: SIDPP = 350 psi, MW = 11 ppg, TVD = 12,000 ft. Find FP.**

- A) 6,864 psi
- B) **7,214 psi** ✅
- C) 7,500 psi
- D) 8,000 psi

**Solution:**

FP = (0.052 × 11 × 12,000) + 350
FP = 6,864 + 350 = 7,214 psi ✅



---

### 📝 Analysis Checklist:

    Type: Compare SICP vs SIDPP
    Size: Note pit gain (bbls)
    FP: Calculate from SIDPP
    KMW: Calculate required mud weight
    MAASP: Check limit before starting kill


        """
    },
        # ═══════════════════════════════════════════════════════
    # MODULE 4: KILL METHODS
    # ═══════════════════════════════════════════════════════
    
    "Driller's Method": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هي Driller's Method؟

**Driller's Method = طريقة الحفار = دورتين!** 🔄🔄

---

### 📋 الفكرة ببساطة:

الدورة الأولى: طلّع الـ Kick بالطين القديم
↓
الدورة الثانية: دوّر الطين الجديد (الثقيل)



---

### 🔄 الدورة الأولى:

**الهدف:** نطلّع الـ Kick من البئر

    ابدأ بالضخ بضغط ICP
    خلي الضغط ثابت على الـ Casing
    استمر لحد ما الـ Kick يطلع
    الـ Casing pressure هيرجع = SIDPP



**ICP = Initial Circulating Pressure**

ICP = SIDPP + SCR



---

### 🔄 الدورة الثانية:

**الهدف:** ندخّل الطين الثقيل

    جهّز الطين الجديد (KMW)
    ابدأ ضخ بضغط ICP
    قلل الضغط تدريجياً لحد FCP
    استمر بـ FCP لحد ما الطين الثقيل يوصل السطح



**FCP = Final Circulating Pressure**

FCP = SCR × (KMW / OMW)



---

### 📊 مثال:

**المعطيات:**
- SIDPP = 600 psi
- SCR = 500 psi
- OMW = 10 ppg
- KMW = 11 ppg

**الحسابات:**

ICP = 600 + 500 = 1,100 psi
FCP = 500 × (11/10) = 550 psi



---

### ✅ مميزات:

| الميزة |
|--------|
| سهلة وبسيطة |
| ما تحتاج تستنى تحضير الطين |
| أقل أخطاء في الحسابات |

### ❌ عيوب:

| العيب |
|-------|
| وقت أطول (دورتين) |
| ضغط أعلى على الـ Casing |
| استهلاك طاقة أكتر |

---

### 💡 تذكر:

> **"Driller's = دورتين = 2 Circulations"**
> 
> **"ICP = SIDPP + SCR"**
> 
> **"FCP = SCR × (KMW/OMW)"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📋 Driller's Method Overview:

┌─────────────────────────────────────────┐
│ DRILLER'S METHOD │
│ │
│ Circulation 1: Remove kick with OMW │
│ ↓ │
│ Circulation 2: Displace with KMW │
└─────────────────────────────────────────┘



---

### 📐 Key Formulas:

**Initial Circulating Pressure (ICP):**

ICP = SIDPP + SCR (at kill rate)



**Final Circulating Pressure (FCP):**

FCP = SCR × (KMW / OMW)



**Kill Mud Weight (KMW):**

KMW = OMW + (SIDPP / (0.052 × TVD))



---

### 📊 First Circulation Procedure:

| Step | Action | Pressure |
|------|--------|----------|
| 1 | Start pumps slowly | Build to ICP |
| 2 | Bring to kill rate | Maintain ICP |
| 3 | Circulate | Hold DP pressure at ICP |
| 4 | Gas at surface | Watch MAASP! |
| 5 | Kick out | Casing P = SIDPP |

**During First Circulation:**
- Drillpipe pressure = **CONSTANT at ICP**
- Casing pressure = **Varies** (increases as gas rises, decreases when out)

---

### 📊 Second Circulation Procedure:

| Step | Action | Pressure |
|------|--------|----------|
| 1 | Start pumping KMW | ICP |
| 2 | KMW in drillstring | Reduce to FCP |
| 3 | KMW at bit | FCP |
| 4 | KMW up annulus | Hold FCP |
| 5 | KMW at surface | FCP, well dead |

**During Second Circulation:**
- Follow **Drillpipe Pressure Schedule**
- Reduce from ICP to FCP over one string volume
- After bit: Hold **CONSTANT FCP**

---

### 📊 Pressure Schedule Example:

**Given:**
- ICP = 1,100 psi
- FCP = 550 psi
- Strokes to bit = 1,000

| Strokes | DP Pressure |
|---------|-------------|
| 0 | 1,100 psi |
| 250 | 962 psi |
| 500 | 825 psi |
| 750 | 687 psi |
| 1,000 | 550 psi |

Pressure drop per stroke = (ICP - FCP) / Strokes
= (1100 - 550) / 1000
= 0.55 psi/stroke



---

### ⚠️ Critical Points:

| Point | Action |
|-------|--------|
| **Maintain BHP** | Always ≥ Formation Pressure |
| **Watch MAASP** | Especially when gas at surface |
| **Constant DP pressure** | During first circulation |
| **Follow schedule** | During second circulation |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Calculate ICP

**Q: SIDPP = 600 psi, SCR = 500 psi. Calculate ICP.**

- A) 500 psi
- B) 600 psi  
- C) 1,000 psi
- D) **1,100 psi** ✅

**Solution:**

ICP = SIDPP + SCR = 600 + 500 = 1,100 psi ✅



---

### ❓ Question 2: Calculate FCP

**Q: SCR = 400 psi, KMW = 11 ppg, OMW = 10 ppg. Calculate FCP.**

- A) 400 psi
- B) **440 psi** ✅
- C) 500 psi
- D) 550 psi

**Solution:**

FCP = SCR × (KMW / OMW)
FCP = 400 × (11 / 10) = 400 × 1.1 = 440 psi ✅



---

### ❓ Question 3: Number of Circulations

**Q: Driller's Method requires how many circulations?**

- A) One
- B) **Two** ✅
- C) Three
- D) Four

---

### ❓ Question 4: First Circulation

**Q: During first circulation of Driller's Method:**

- A) Pump kill mud
- B) **Circulate out kick with original mud** ✅
- C) Wait for mud to be mixed
- D) Shut in the well

---

### ❓ Question 5: Pressure Held Constant

**Q: During first circulation, which pressure is held constant?**

- A) Casing pressure
- B) **Drillpipe pressure (ICP)** ✅
- C) Both pressures
- D) Neither

---

### ❓ Question 6: Calculate KMW

**Q: OMW = 10 ppg, SIDPP = 520 psi, TVD = 10,000 ft. Find KMW.**

- A) 10.5 ppg
- B) **11.0 ppg** ✅
- C) 11.5 ppg
- D) 12.0 ppg

**Solution:**

KMW = 10 + (520 / (0.052 × 10,000))
KMW = 10 + (520 / 520) = 10 + 1 = 11 ppg ✅



---

### 📝 Memory Aid:

🧠 DRILLER'S METHOD:

D - Double circulation (2 times around)
R - Remove kick first
I - ICP = SIDPP + SCR
L - Later pump kill mud
L - Linear pressure reduction
E - End at FCP
R - Reach FCP when KMW at bit
S - Simple method!


        """
    },
    
    "Wait and Weight Method": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هي Wait and Weight Method؟

**Wait and Weight = استنى وثقّل = دورة واحدة!** 🔄

---

### 📋 الفكرة ببساطة:

    استنى (Wait) ← لحد ما الطين الثقيل يجهز
    ثقّل (Weight) ← ضخ الطين الثقيل
    دورة واحدة بس! ← طلّع الـ Kick ودخّل الطين الثقيل في نفس الوقت



---

### 🔄 الخطوات:

    احسب KMW
    ↓
    جهّز الطين الثقيل
    ↓
    ابدأ ضخ بضغط ICP
    ↓
    قلل الضغط تدريجياً
    ↓
    وصلت للـ FCP لما الطين وصل الـ Bit
    ↓
    استمر بـ FCP لحد ما الطين يوصل السطح



---

### 📊 مقارنة مع Driller's:

| الموضوع | Driller's | Wait & Weight |
|---------|-----------|---------------|
| **عدد الدورات** | 2 | 1 |
| **الوقت** | أطول | أقصر |
| **ضغط الـ Casing** | أعلى | أقل ✅ |
| **التعقيد** | بسيط | أصعب شوية |

---

### ✅ مميزات:

| الميزة |
|--------|
| دورة واحدة = وقت أقل |
| ضغط أقل على الـ Casing |
| مناسب للتكوينات الضعيفة |

### ❌ عيوب:

| العيب |
|-------|
| لازم تستنى تحضير الطين |
| حسابات أكتر |
| احتمال أخطاء أعلى |

---

### 💡 تذكر:

> **"Wait & Weight = دورة واحدة = 1 Circulation"**
> 
> **"أفضل للتكوينات الضعيفة (أقل ضغط)"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📋 Wait and Weight Overview:

┌─────────────────────────────────────────┐
│ WAIT AND WEIGHT METHOD │
│ │
│ Single circulation: │
│ - Pump KMW from start │
│ - Remove kick simultaneously │
│ - Lower casing pressure exposure │
└─────────────────────────────────────────┘



---

### 📐 Same Formulas as Driller's:

ICP = SIDPP + SCR
FCP = SCR × (KMW / OMW)
KMW = OMW + (SIDPP / (0.052 × TVD))



---

### 📊 Procedure:

| Phase | Action | Pressure Control |
|-------|--------|------------------|
| **Wait** | Mix kill mud to KMW | Monitor pressures |
| **Start** | Begin pumping | Build to ICP |
| **DS** | KMW down drillstring | ICP → FCP (follow schedule) |
| **Bit** | KMW reaches bit | At FCP |
| **Ann** | KMW up annulus | Hold FCP constant |
| **Surface** | KMW at surface | Well dead |

---

### 📊 Pressure Schedule:

**Drillpipe pressure reduces from ICP to FCP as KMW travels down the string:**

Surface ─────── ICP (1,100 psi)
│
│ KMW displacing OMW
│ Pressure reducing
│
Bit ────────── FCP (550 psi)
│
│ Hold FCP constant
│
Surface ─────── FCP (well dead)



---

### 📊 Why Lower Casing Pressure?

**In Driller's Method:**

First circ: Kick rises with light mud above it
→ High surface pressure needed



**In Wait & Weight:**

Single circ: Heavy mud follows kick up
→ Less surface pressure needed



---

### 📊 Comparison Table:

| Aspect | Driller's | W&W |
|--------|-----------|-----|
| Circulations | 2 | 1 |
| Time | Longer | Shorter |
| Max Casing P | Higher | **Lower** |
| Complexity | Simple | Complex |
| Error Risk | Lower | Higher |
| Preferred when | Simple situation | Weak formation |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Number of Circulations

**Q: Wait and Weight Method requires:**

- A) **One circulation** ✅
- B) Two circulations
- C) Three circulations
- D) No circulation

---

### ❓ Question 2: Advantage

**Q: Main advantage of Wait and Weight over Driller's:**

- A) Simpler procedure
- B) **Lower casing pressure** ✅
- C) No calculations needed
- D) Faster to start

---

### ❓ Question 3: When to Use

**Q: Wait and Weight is preferred when:**

- A) Quick action needed
- B) **Formation is weak** ✅
- C) No mud available
- D) Large kick volume

**💡 Lower casing pressure protects weak formations!**

---

### ❓ Question 4: First Action

**Q: First action in Wait and Weight is:**

- A) Start pumping immediately
- B) **Wait for kill mud to be mixed** ✅
- C) Increase mud weight while circulating
- D) Bleed off pressure

---

### ❓ Question 5: Same Formulas

**Q: ICP formula for Wait and Weight is:**

- A) Different from Driller's
- B) **Same: ICP = SIDPP + SCR** ✅
- C) ICP = SICP + SCR
- D) ICP = FCP + SIDPP

---

### 📝 Comparison Memory:

DRILLER'S METHOD:

    2 circulations
    Higher casing pressure
    Start immediately
    Simple

WAIT & WEIGHT:

    1 circulation
    Lower casing pressure
    Wait for kill mud
    Complex (but faster overall)


        """
    },
    
    "Volumetric Method": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هي Volumetric Method؟

**Volumetric = طريقة حجمية = بدون ضخ!** 🚫💧

---

### 🤔 امتى نستخدمها؟

**لما ما نقدرش نضخ!**

- ✅ الـ Pipe stuck (معلق)
- ✅ المضخات عاطلة
- ✅ مفيش Drillstring في البئر

---

### 📋 الفكرة ببساطة:

الغاز بيطلع لوحده (migration)
↓
الضغط على السطح بيزيد
↓
نسيب طين يخرج من الـ Choke
↓
كده نحافظ على ضغط ثابت في القاع



---

### 🔄 الخطوات:

    الغاز بيطلع → الضغط بيزيد
    ↓
    لما الضغط يزيد بمقدار معين
    ↓
    افتح الـ Choke وسيب طين يخرج
    ↓
    سيب كمية طين = الزيادة في الضغط
    ↓
    كرر لحد ما الغاز يوصل السطح



---

### 📐 الحساب:

**كمية الطين اللي نسيبها تخرج:**

Mud to bleed = Pressure increase / Mud gradient

مثال:
لو الضغط زاد 100 psi
والـ gradient = 0.52 psi/ft

المسافة = 100 / 0.52 = 192 ft
الحجم = 192 × Annular capacity



---

### 💡 تذكر:

> **"Volumetric = مفيش ضخ"**
> 
> **"الغاز يطلع لوحده، وإحنا نسيب طين"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📋 Volumetric Method Overview:

┌─────────────────────────────────────────┐
│ VOLUMETRIC METHOD │
│ │
│ No circulation possible │
│ Allow gas to migrate │
│ Bleed mud to maintain BHP │
└─────────────────────────────────────────┘



---

### 🔬 How It Works:

Initial State:
├── Gas at bottom
├── Well shut in
└── BHP = HP + Surface Pressure

As Gas Migrates Up:
├── Gas expands (lower pressure)
├── Surface pressure increases
├── If no action: BHP increases!

Solution:
├── Bleed mud to reduce surface pressure
├── Maintain constant BHP
└── Repeat until gas at surface



---

### 📐 Key Calculation:

**Volume to bleed for pressure reduction:**

Volume = (ΔP / Mud Gradient) × Annular Capacity

Where:
ΔP = Pressure increase to allow before bleeding
Mud Gradient = 0.052 × MW
Annular Capacity = bbl/ft



---

### 📊 Procedure Steps:

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Record initial SICP | Baseline |
| 2 | Allow pressure to increase (e.g., 100 psi) | Gas rising |
| 3 | Calculate mud volume for 100 psi | Bleed amount |
| 4 | Bleed calculated volume | Reduce pressure |
| 5 | Verify pressure dropped ~100 psi | Confirm BHP constant |
| 6 | Repeat until gas at surface | Complete migration |

---

### 📊 Example:

**Given:**
- MW = 10 ppg (gradient = 0.52 psi/ft)
- Annular capacity = 0.05 bbl/ft
- Allow 100 psi increase before bleeding

**Calculate:**

Height equivalent = 100 / 0.52 = 192 ft
Volume to bleed = 192 × 0.05 = 9.6 bbl

For each 100 psi increase:
Bleed approximately 10 bbl



---

### ⚠️ Critical Points:

| Point | Explanation |
|-------|-------------|
| **Patience required** | Gas migrates slowly (~1000 ft/hr) |
| **Accurate volumes** | Must measure precisely |
| **BHP constant** | Goal is constant bottomhole pressure |
| **Never exceed MAASP** | Bleed before reaching limit |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: When Used

**Q: Volumetric Method is used when:**

- A) Kick is too large
- B) Mud is too heavy
- C) **Circulation is not possible** ✅
- D) Gas kick only

---

### ❓ Question 2: No Pumping

**Q: In Volumetric Method:**

- A) Pump at high rate
- B) Pump at kill rate
- C) **No pumping is done** ✅
- D) Pump intermittently

---

### ❓ Question 3: Principle

**Q: Volumetric Method maintains constant:**

- A) Surface pressure
- B) Drillpipe pressure
- C) **Bottomhole pressure** ✅
- D) Pump pressure

---

### ❓ Question 4: Action Required

**Q: As gas migrates in Volumetric Method, you must:**

- A) Increase mud weight
- B) **Bleed mud from annulus** ✅
- C) Pump mud into well
- D) Close the choke

---

### ❓ Question 5: Cause

**Q: Why does surface pressure increase during gas migration?**

- A) Pump is running
- B) **Gas expansion as it rises** ✅
- C) Mud getting heavier
- D) BOP leaking

---

### 📝 Key Points:

VOLUMETRIC = NO PUMPING

Used when:
✗ Stuck pipe
✗ No pumps
✗ No drillstring

Action:
→ Gas rises naturally
→ Pressure increases
→ Bleed mud
→ Maintain BHP


        """
    },
    
    "Bullheading": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Bullheading؟

**Bullheading = ادفع كل حاجة راجع للتكوين!** 💪

---

### 📋 الفكرة:

بدل ما نطلّع الـ Kick
↓
ندفعه راجع للتكوين من غير ما يطلع السطح!



---

### 🤔 امتى نستخدمه؟

**بشكل أساسي مع H2S (غاز سام)!** ☠️

لأن:
- H2S خطير جداً على السطح
- أفضل ندفعه راجع للأرض
- ما نخليهوش يطلع خالص

---

### ⚠️ المخاطر:

| الخطر | السبب |
|-------|-------|
| **كسر التكوين** | الضغط العالي |
| **Underground Blowout** | لو التكوين انكسر |
| **عدم نجاح العملية** | لو التكوين ما قبلش السوائل |

---

### 📋 الإجراء:

    تأكد إن ده الحل الوحيد
    ↓
    احسب الضغط المطلوب
    ↓
    ابدأ الضخ ببطء
    ↓
    زوّد الضغط تدريجياً
    ↓
    ادفع الـ Kick راجع للتكوين
    ↓
    راقب الضغط وحجم الضخ



---

### 💡 تذكر:

> **"Bullheading = للـ H2S بشكل أساسي"**
> 
> **"خطر كسر التكوين!"**
> 
> **"آخر حل، مش أول حل!"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📋 Bullheading Overview:

┌─────────────────────────────────────────┐
│ BULLHEADING │
│ │
│ Force influx back into formation │
│ No circulation to surface │
│ Used for H2S or specific situations │
└─────────────────────────────────────────┘



---

### 🔬 When to Use:

| Situation | Reason |
|-----------|--------|
| **H2S kick** | Too dangerous to bring to surface |
| **Surface equipment issues** | Can't handle the kick |
| **Shallow gas** | Quick response needed |
| **No pipe in hole** | Can't circulate |

---

### 📊 Procedure:

| Step | Action |
|------|--------|
| 1 | Confirm decision with management |
| 2 | Calculate maximum allowable pressure |
| 3 | Line up through kill line |
| 4 | Start pumping slowly |
| 5 | Increase rate gradually |
| 6 | Monitor pressure vs volume |
| 7 | Continue until well stabilizes |

---

### ⚠️ Risks:

| Risk | Consequence |
|------|-------------|
| **Formation breakdown** | Underground blowout |
| **Stuck pipe** | Loss of well control |
| **Partial success** | Kick remains in wellbore |
| **High pressures** | Equipment failure |

---

### 📊 Pressure Considerations:

Maximum Surface Pressure ≤ MAASP
(Or formation will fracture at shoe)

Pumping Pressure =
Friction + Back pressure needed to
force fluid into formation



---

### 📊 When NOT to Use:

- Formation won't accept fluid (tight)
- Risk of underground blowout is high
- Better alternatives available
- Surface equipment can handle the kick
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Primary Use

**Q: Bullheading is most appropriate for:**

- A) Gas kick
- B) Water kick
- C) **H2S kick** ✅
- D) Oil kick

---

### ❓ Question 2: Main Risk

**Q: Main risk of bullheading is:**

- A) Slow process
- B) **Formation breakdown** ✅
- C) BOP failure
- D) Pump failure

---

### ❓ Question 3: Direction

**Q: In bullheading, the kick is:**

- A) Circulated to surface
- B) **Pushed back into formation** ✅
- C) Diluted with mud
- D) Allowed to migrate

---

### ❓ Question 4: When Not Used

**Q: Bullheading should NOT be used when:**

- A) H2S present
- B) No pipe in hole
- C) **Better alternatives available** ✅
- D) Shallow gas

---

### 📝 Key Points:

BULLHEADING:
✓ Push kick back into formation
✓ Primary use: H2S kicks
✓ Risk: Formation breakdown
✓ Not first choice usually


        """
    },
    
    "Kill Sheet Calculations": {
        "simple": """
## 🟢 ببساطة كده... (Simple Explanation)

### 🎯 إيه هو الـ Kill Sheet؟

**Kill Sheet = ورقة فيها كل الحسابات المطلوبة لقتل البئر!** 📋

---

### 📊 الحسابات الأساسية:

---

#### **1️⃣ Kill Mud Weight (KMW):**

KMW = OMW + (SIDPP / 0.052 / TVD)



**مثال:**

OMW = 10 ppg
SIDPP = 400 psi
TVD = 10,000 ft

KMW = 10 + (400 / 0.052 / 10,000)
KMW = 10 + (400 / 520)
KMW = 10 + 0.77
KMW = 10.77 ppg → Round to 10.8 ppg



---

#### **2️⃣ Initial Circulating Pressure (ICP):**

ICP = SIDPP + SCR



**مثال:**

SIDPP = 400 psi
SCR = 500 psi

ICP = 400 + 500 = 900 psi



---

#### **3️⃣ Final Circulating Pressure (FCP):**

FCP = SCR × (KMW / OMW)



**مثال:**

SCR = 500 psi
KMW = 10.8 ppg
OMW = 10 ppg

FCP = 500 × (10.8 / 10)
FCP = 500 × 1.08
FCP = 540 psi



---

### 📋 جدول الضغط (Pressure Schedule):

**من ICP إلى FCP عبر الـ Strokes to Bit:**

| Strokes | Pressure |
|---------|----------|
| 0 | ICP |
| 25% | ICP - 25% of (ICP-FCP) |
| 50% | ICP - 50% of (ICP-FCP) |
| 75% | ICP - 75% of (ICP-FCP) |
| 100% | FCP |

---

### 💡 تذكر:

> **"KMW = كم نحتاج من الوزن"**
> 
> **"ICP = ضغط البداية"**
> 
> **"FCP = ضغط النهاية"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge (المعرفة الفنية)

### 📋 Complete Kill Sheet Contents:

┌─────────────────────────────────────────┐
│ KILL SHEET │
├─────────────────────────────────────────┤
│ Well Information │
│ Mud Properties │
│ Pump Data │
│ Wellbore Volumes │
│ Pressure Readings │
│ Calculated Values │
│ Pressure Schedule │
└─────────────────────────────────────────┘



---

### 📐 All Formulas:

**Kill Mud Weight:**

KMW = OMW + (SIDPP / (0.052 × TVD))

With safety margin:
KMW = OMW + (SIDPP / (0.052 × TVD)) + 0.5 ppg



**Initial Circulating Pressure:**

ICP = SIDPP + SCR(at kill rate)



**Final Circulating Pressure:**

FCP = SCR × (KMW / OMW)



**Pressure Drop per Stroke:**

ΔP/stroke = (ICP - FCP) / Strokes to bit



---

### 📊 Volume Calculations:

Drillstring Volume:
= Σ(Capacity × Length) for each section

Annulus Volume:
= Σ(Annular Capacity × Length) for each section

Total Well Volume:
= Drillstring + Annulus



---

### 📊 Strokes Calculation:

Strokes = Volume / Pump Output

Example:
DS Volume = 200 bbl
Pump output = 0.1 bbl/stroke
Strokes to bit = 200 / 0.1 = 2,000 strokes



---

### 📊 Complete Example:

**Given:**
- SIDPP = 400 psi
- SICP = 650 psi
- OMW = 10 ppg
- TVD = 10,000 ft
- SCR = 500 psi at 30 spm
- Pit gain = 20 bbl
- Strokes to bit = 1,500

**Calculations:**

    KMW:
    KMW = 10 + (400/(0.052×10000))
    KMW = 10 + 0.77 = 10.77 ppg → 10.8 ppg

    ICP:
    ICP = 400 + 500 = 900 psi

    FCP:
    FCP = 500 × (10.8/10) = 540 psi

    Pressure Schedule:
    Drop = 900 - 540 = 360 psi over 1500 strokes
    = 0.24 psi/stroke



| Strokes | Pressure |
|---------|----------|
| 0 | 900 psi |
| 375 | 810 psi |
| 750 | 720 psi |
| 1125 | 630 psi |
| 1500 | 540 psi |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format (صيغة الامتحان)

### ❓ Question 1: Calculate KMW

**Q: OMW=10 ppg, SIDPP=520 psi, TVD=10,000 ft. Find KMW.**

- A) 10.5 ppg
- B) **11.0 ppg** ✅
- C) 11.5 ppg
- D) 12.0 ppg

**Solution:**

KMW = 10 + (520/(0.052×10000))
KMW = 10 + (520/520) = 11.0 ppg ✅



---

### ❓ Question 2: Calculate ICP

**Q: SIDPP=350 psi, SCR=450 psi. Find ICP.**

- A) 350 psi
- B) 450 psi
- C) **800 psi** ✅
- D) 900 psi

**Solution:**

ICP = SIDPP + SCR = 350 + 450 = 800 psi ✅



---

### ❓ Question 3: Calculate FCP

**Q: SCR=500 psi, KMW=11 ppg, OMW=10 ppg. Find FCP.**

- A) 500 psi
- B) **550 psi** ✅
- C) 600 psi
- D) 650 psi

**Solution:**

FCP = 500 × (11/10) = 550 psi ✅



---

### ❓ Question 4: Pressure Relationship

**Q: FCP is always:**

- A) Greater than ICP
- B) Equal to ICP
- C) **Less than ICP** ✅
- D) Zero

---

### ❓ Question 5: When FCP Reached

**Q: FCP is reached when:**

- A) Kill mud at surface
- B) **Kill mud at bit** ✅
- C) Kick at surface
- D) Well is dead

---

### 📝 Formula Summary:

🧮 KILL SHEET FORMULAS:

KMW = OMW + (SIDPP / 0.052 / TVD)
ICP = SIDPP + SCR
FCP = SCR × (KMW / OMW)

Always: FCP < ICP
FCP reached when: KMW at bit


        """
    },
    
    # ═══════════════════════════════════════════════════════
    # MODULE 5: EQUIPMENT (مختصر)
    # ═══════════════════════════════════════════════════════
    
    "BOP Components": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ BOP؟

**BOP = Blowout Preventer = مانع الانفجار!** 🛡️

---

### 📊 المكونات الرئيسية:

| المكون | الوظيفة |
|--------|---------|
| **Annular Preventer** | يقفل على أي شكل |
| **Pipe Rams** | يقفل على مقاس معين من الـ Pipe |
| **Blind Rams** | يقفل البئر الفاضي |
| **Shear Rams** | يقطع الـ Pipe! (طوارئ) |

---

### 🔧 ترتيب الـ Stack (من فوق لتحت):


 ┌─────────────┐
 │  Annular    │ ← الأول (فوق)
 ├─────────────┤
 │  Pipe Rams  │
 ├─────────────┤
 │  Blind Rams │
 ├─────────────┤
 │  Shear Rams │ ← الأخير (تحت)
 └─────────────┘
     Wellhead



---

### 💡 تذكر:

> **"Annular = مرن، يقفل على أي حاجة"**
> 
> **"Shear Rams = طوارئ فقط، يقطع الـ Pipe!"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 BOP Stack Configuration:

| Component | Pressure Rating | Function |
|-----------|-----------------|----------|
| Annular | 5,000-10,000 psi | Seals on any shape |
| Pipe Rams | 10,000-15,000 psi | Seals on specific OD |
| Blind Rams | 10,000-15,000 psi | Seals open hole |
| Shear Rams | 10,000-15,000 psi | Cuts pipe, seals |

---

### 📋 Testing Requirements:

| Test | Frequency |
|------|-----------|
| Function test | Weekly |
| Low pressure test | After installation |
| High pressure test | After installation |
| BOP drill | Weekly |

---

### ⚠️ Key Points:

- Rams have higher pressure rating than annular
- Shear rams are LAST RESORT only
- Always know pipe OD when closing rams
- Function test accumulator capacity
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Which BOP element seals on open hole (no pipe)?**

- A) Annular
- B) Pipe rams
- C) **Blind rams** ✅
- D) Shear rams

---

### ❓ Question 2:

**Q: Which can seal on ANY pipe size?**

- A) Pipe rams
- B) Blind rams
- C) **Annular preventer** ✅
- D) Shear rams

---

### ❓ Question 3:

**Q: Shear rams are used:**

- A) Routinely
- B) For stripping
- C) **As last resort emergency** ✅
- D) First response
        """
    },
    
    "Annular Preventer": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Annular Preventer؟

**Annular = المرن!** 🔄

عبارة عن عنصر مطاطي يقدر يقفل على أي شكل!

---

### ✅ مميزاته:

| الميزة |
|--------|
| يقفل على أي مقاس pipe |
| يقفل على kelly |
| يقفل على tool joints |
| يسمح بـ Stripping |

---

### ❌ عيوبه:

| العيب |
|-------|
| ضغط أقل من الـ Rams |
| العنصر المطاطي بيتآكل |
| ما يقدرش يقطع الـ Pipe |
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Annular Preventer Design:

- Rubber/steel packing element
- Hydraulically operated
- Can strip pipe through it
- Lower pressure rating than rams

### 📋 Uses:

| Use | Notes |
|-----|-------|
| Initial shut-in | First to close |
| Stripping | Move pipe through closed preventer |
| Irregular shapes | Seals on any profile |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Stripping pipe requires:**

- A) Blind rams
- B) **Annular preventer** ✅
- C) Shear rams
- D) Pipe rams only
        """
    },
    
    "Ram Preventers": {
        "simple": """
## 🟢 ببساطة كده...

### 📊 أنواع الـ Rams:

| النوع | الوظيفة |
|-------|---------|
| **Pipe Rams** | يقفل حول الـ Pipe |
| **Blind Rams** | يقفل البئر الفاضي |
| **Shear Rams** | يقطع الـ Pipe |
| **Variable Bore** | يقفل على مقاسات مختلفة |

---

### ⚠️ مهم:

**Shear Rams = آخر حل فقط!**

بيقطع الـ Pipe = مش هتقدر تستخدمه تاني!
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Ram Types Comparison:

| Type | Function | Limitation |
|------|----------|------------|
| Pipe | Seal around pipe | Specific size |
| Blind | Seal open hole | No pipe present |
| Shear | Cut pipe & seal | Destroys pipe |
| VBR | Multiple sizes | Limited range |

### 📋 Operating Procedure:

1. Space out (tool joint away from rams)
2. Close slowly
3. Lock rams
4. Test seal
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Before closing pipe rams, you should:**

- A) Increase pump rate
- B) **Space out pipe** ✅
- C) Open choke
- D) Record pressures
        """
    },
    
    "Choke Manifold": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Choke Manifold؟

**Choke Manifold = نظام التحكم في الضغط!** ⚙️

---

### 📊 المكونات:

| المكون | الوظيفة |
|--------|---------|
| **Adjustable Choke** | تتحكم في الضغط |
| **Fixed Choke** | للطوارئ |
| **Valves** | للتوجيه |
| **Gauges** | لقياس الضغط |

---

### 📋 القواعد:

| الفعل | النتيجة |
|-------|---------|
| **افتح الـ Choke** | الضغط يقل |
| **اقفل الـ Choke** | الضغط يزيد |
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Choke Operation During Kill:

| Objective | Action |
|-----------|--------|
| Increase casing P | Close choke |
| Decrease casing P | Open choke |
| Maintain constant BHP | Adjust as needed |

### ⚠️ Critical:

- Never fully close during kill
- Adjust slowly
- Watch pressure response
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Opening the choke will:**

- A) Increase casing pressure
- B) **Decrease casing pressure** ✅
- C) Have no effect
- D) Stop the pumps
        """
    },
    
    "Accumulator System": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Accumulator؟

**Accumulator = بطارية الـ BOP!** 🔋

نظام مشحون بضغط عالي علشان يقفل الـ BOP بسرعة!

---

### 📊 المكونات:

| المكون | الوظيفة |
|--------|---------|
| **Bottles** | تخزين الضغط |
| **Nitrogen** | غاز الشحن |
| **Hydraulic Fluid** | سائل التشغيل |
| **Pumps** | إعادة الشحن |

---

### 💡 تذكر:

> **"مشحون بـ Nitrogen (N₂)"**
> 
> **"لازم يقفل كل الـ BOPs ويفضل 200 psi"**
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Accumulator Requirements:

| Requirement | Value |
|-------------|-------|
| Precharge gas | Nitrogen (N₂) |
| Precharge pressure | ~1000 psi |
| Operating pressure | 3000 psi |
| Minimum remaining | 200 psi after closing all |

### 📋 Capacity Test:

Must close all BOPs + 200 psi remaining
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Accumulator bottles are precharged with:**

- A) Air
- B) Oxygen
- C) **Nitrogen** ✅
- D) Hydraulic fluid
        """
    },
    
    # ═══════════════════════════════════════════════════════
    # MODULE 6: GAS BEHAVIOR
    # ═══════════════════════════════════════════════════════
    
    "Gas Behavior (Boyle's Law)": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 قانون بويل:

**"لما الضغط يقل، الحجم يزيد!"** 📈

---

### 📐 المعادلة:

<div class="formula-box">
P₁ × V₁ = P₂ × V₂
</div>

---

### 📝 مثال:

**غاز في القاع:**
- الضغط = 4,000 psi
- الحجم = 10 bbls

**نفس الغاز على السطح:**
- الضغط = 400 psi
- الحجم = ؟؟؟

V₂ = P₁ × V₁ / P₂
V₂ = 4,000 × 10 / 400
V₂ = 100 bbls!



**الغاز تضاعف 10 مرات!** 😱

---

### ⚠️ الخطر:

**أسرع expansion بيحصل قرب السطح!**

آخر 2,000 قدم = أخطر جزء!
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📐 Boyle's Law:

At constant temperature:

P₁V₁ = P₂V₂

V₂ = V₁ × (P₁/P₂)



---

### 📊 Expansion Table:

| Depth (ft) | Pressure (psi) | Volume (bbl) |
|------------|----------------|--------------|
| 10,000 | 5,200 | 10 |
| 5,000 | 2,600 | 20 |
| 2,500 | 1,300 | 40 |
| 1,000 | 520 | 100 |
| Surface | ~50 | ~1,000 |

---

### ⚠️ Critical Zone:

Last 2,000-3,000 ft = Most rapid expansion!

Must control choke carefully!
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Gas at 4,000 psi = 10 bbls. Volume at 400 psi?**

- A) 10 bbls
- B) 50 bbls
- C) **100 bbls** ✅
- D) 1,000 bbls

**Solution:**

V₂ = 10 × (4000/400) = 100 bbls ✅



---

### ❓ Question 2:

**Q: Most rapid gas expansion occurs:**

- A) At bottom
- B) Mid-well
- C) **Near surface** ✅
- D) Equal everywhere
        """
    },
    
    "Gas Migration": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Gas Migration؟

**الغاز أخف من الطين، فبيطلع لوحده!** 💨⬆️

---

### 📊 السرعة:

**حوالي 1,000 قدم في الساعة** ⏱️

يعني بئر 10,000 قدم = ~10 ساعات للسطح

---

### ⚠️ المشكلة:

لما الغاز يطلع:
- الضغط على السطح **بيزيد!**
- لازم نراقب كويس
- ممكن نحتاج نسيب ضغط (Volumetric)
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Migration Rate:

| Condition | Rate |
|-----------|------|
| Typical | 500-2,000 ft/hr |
| Average estimate | 1,000 ft/hr |
| In high-viscosity mud | Slower |

### 📋 Effect on Pressures:

As gas migrates (well shut-in):
- Gas compresses less as it rises
- Volume increases
- Surface pressure increases
- BHP may increase if not controlled
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Typical gas migration rate is:**

- A) 100 ft/hour
- B) 500 ft/hour
- C) **1,000 ft/hour** ✅
- D) 5,000 ft/hour
        """
    },
    
    "Gas Expansion Calculations": {
        "simple": """
## 🟢 ببساطة كده...

### 📐 المعادلة:

V₂ = V₁ × (P₁ / P₂)



**أو بالعمق:**

V₂ ≈ V₁ × (Depth₁ / Depth₂)



---

### 📝 مثال:

20 bbl في 10,000 ft → كام في 2,000 ft؟

V₂ = 20 × (10,000 / 2,000)
V₂ = 20 × 5
V₂ = 100 bbl


        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📐 Formulas:

**Using Pressure:**

V₂ = V₁ × (P₁ / P₂)



**Using Depth (approximation):**

V₂ ≈ V₁ × (TVD₁ / TVD₂)



### ⚠️ Critical Zone:

Most expansion in last 2,000 ft!
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: 20 bbls at 10,000 ft. Volume at 2,000 ft?**

- A) 20 bbls
- B) 50 bbls
- C) **100 bbls** ✅
- D) 200 bbls
        """
    },
    
    "Stripping Operations": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Stripping؟

**Stripping = تحريك الـ Pipe والبئر مقفول!** 🔄

---

### 📋 امتى نستخدمه؟

- Kick حصل والـ Pipe مش في القاع
- محتاج تنزّل أو تطلّع Pipe
- البئر لازم يفضل مقفول

---

### 📊 الإجراء:

1. اقفل الـ Annular بضغط خفيف
2. حرّك الـ Pipe ببطء
3. راقب الضغط والحجم
4. عوّض displacement
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Stripping vs Snubbing:

| Stripping | Snubbing |
|-----------|----------|
| Pipe falls by gravity | Pipe pushed down |
| Weight > Well force | Weight < Well force |
| Through annular | Through annular + snub stack |

### 📋 Volume Control:

Must account for:
- Pipe displacement
- Steel volume entering/leaving
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Stripping uses which preventer?**

- A) Pipe rams
- B) **Annular preventer** ✅
- C) Blind rams
- D) Shear rams
        """
    },
    
    # ═══════════════════════════════════════════════════════
    # MODULE 7: COMPLICATIONS
    # ═══════════════════════════════════════════════════════
    
    "Lost Circulation": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Lost Circulation؟

**Lost Circulation = الطين بيروح في الأرض!** 🕳️

---

### 📊 الأنواع:

| النوع | الكمية |
|-------|--------|
| **Seepage** | < 10 bbl/hr |
| **Partial** | 10-50 bbl/hr |
| **Severe** | > 50 bbl/hr |
| **Total** | مفيش Returns خالص! |

---

### ⚠️ الخطر:

**لو فقدت طين = ممكن يحصل Kick!**

ضغط الطين هيقل!

---

### 📋 أثناء الـ Kill:

**لو حصل losses أثناء Kill:**
> **استمر بمعدل أقل!**
> 
> ما توقفش! هيحصل Kick أكبر!
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Response During Kill:

| Situation | Action |
|-----------|--------|
| Minor losses | Continue, reduce rate |
| Severe losses | Continue at minimum rate |
| Total losses | May need to bullhead |

### ⚠️ Never:

- Stop pumping completely
- Allow BHP to drop
- Ignore increasing losses
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: During well kill, losses occur. You should:**

- A) Shut in
- B) **Continue at reduced rate** ✅
- C) Increase pump rate
- D) Stop immediately
        """
    },
    
    "Underground Blowout": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ Underground Blowout؟

**Underground Blowout = الـ Kick راح لتكوين تاني!** 😱

بدل ما يطلع السطح، راح لتكوين ضعيف تحت!

---

### 📊 السبب الرئيسي:

**تجاوز الـ MAASP!**

الضغط كسر التكوين عند الـ Shoe!

---

### 📊 العلامات:

| العلامة |
|---------|
| SIDPP بيقل من غير سبب |
| Pit level ثابت |
| ضغط الضخ بيقل |
| Lost circulation |
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Causes:

1. Exceeding MAASP
2. Weak formation at shoe
3. Excessive choke pressure
4. Poor pressure control

### 📋 Indicators:

| Sign | Explanation |
|------|-------------|
| Dropping SIDPP | Formation taking fluid |
| Stable pit | Flow going underground |
| Decreasing pump P | Less resistance |

### ⚠️ Prevention:

Never exceed MAASP!
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Main cause of underground blowout during kill:**

- A) Low pump rate
- B) **Exceeding MAASP** ✅
- C) Heavy mud
- D) Slow response
        """
    },
    
    "Stuck Pipe During Kill": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 المشكلة:

**Kick + Stuck Pipe = مشكلة مزدوجة!** 😰

---

### 📋 الأولوية:

## **Well Control أولاً!** 🥇

الـ Pipe ممكن نفكه بعدين...
الـ Kick لازم نتحكم فيه دلوقتي!

---

### 📊 لو مفيش Circulation:

**استخدم Volumetric Method!**
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Priority:

1. Maintain well control (BHP ≥ FP)
2. Try to free pipe without losing control
3. If can't circulate: Volumetric
4. Consider fishing later

### ⚠️ Never:

- Sacrifice well control for pipe
- Make jarring attempts that reduce BHP
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Priority with stuck pipe during kick:**

- A) Free pipe first
- B) **Maintain well control** ✅
- C) Cut pipe
- D) Wait for help
        """
    },
    
    "H2S Considerations": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ H2S؟

**H2S = Hydrogen Sulfide = غاز البيض الفاسد** ☠️

**غاز سام جداً!**

---

### 📊 مستويات الخطر:

| التركيز | التأثير |
|---------|---------|
| 10 ppm | ريحة بيض فاسد |
| 100 ppm | **يقتل حاسة الشم!** ⚠️ |
| 300 ppm | خطر على الحياة |
| 1000 ppm | **موت فوري!** ☠️ |

---

### ⚠️ أخطر حاجة:

**عند 100 ppm مش هتحس بالريحة!**

الغاز بيشل حاسة الشم!

---

### 📋 الإجراء:

**استخدم Bullheading!**

ادفع الغاز راجع للتكوين!
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 H2S Properties:

| Property | Value |
|----------|-------|
| Color | Colorless |
| Smell | Rotten eggs (low conc.) |
| Density | Heavier than air |
| IDLH | 100 ppm |
| Lethal | 500-1000 ppm |

### 📋 Olfactory Fatigue:

At ~100 ppm, smell is paralyzed!
Cannot detect by smell anymore!

### 📋 Kill Method:

Bullheading preferred - keeps H2S downhole!
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: H2S at 100 ppm will:**

- A) Be easily smelled
- B) **Paralyze sense of smell** ✅
- C) Have no effect
- D) Cause headache only

---

### ❓ Question 2:

**Q: Best kill method for H2S:**

- A) Driller's Method
- B) Wait and Weight
- C) **Bullheading** ✅
- D) Volumetric
        """
    },
    
    # ═══════════════════════════════════════════════════════
    # MODULE 8: PROCEDURES
    # ═══════════════════════════════════════════════════════
    
    "IWCF Standards": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 إيه هو الـ IWCF؟

**IWCF = International Well Control Forum**

المنظمة الدولية لشهادات التحكم في الآبار!

---

### 📊 معلومات الشهادة:

| البند | القيمة |
|-------|--------|
| **الصلاحية** | سنتين (2 years) |
| **النجاح** | 70% |
| **الأسئلة** | 50 سؤال |
| **الوقت** | ساعتين |

---

### 📊 المستويات:

| Level | المسمى |
|-------|--------|
| Level 2 | Driller |
| Level 3 | Supervisor |
| Level 4 | Engineer |
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 IWCF Certification:

| Aspect | Details |
|--------|---------|
| Validity | 2 years |
| Pass mark | 70% (35/50) |
| Questions | 50 MCQ |
| Duration | 2 hours |
| Open book | Formula sheet only |

### 📋 Levels:

| Level | Position | Scope |
|-------|----------|-------|
| 2 | Drillers | Surface operations |
| 3 | Supervisors | Surface + decision |
| 4 | Engineers | All + planning |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: IWCF certificate is valid for:**

- A) 1 year
- B) **2 years** ✅
- C) 5 years
- D) Lifetime

---

### ❓ Question 2:

**Q: Pass mark for IWCF exam:**

- A) 50%
- B) 60%
- C) **70%** ✅
- D) 80%
        """
    },
    
    "Safety Procedures": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 قواعد السلامة:

---

#### **1️⃣ كن جاهز دايماً!**

- اعرف خطة الطوارئ
- اتدرب على الإجراءات
- تأكد من المعدات

---

#### **2️⃣ راقب باستمرار!**

| راقب | الدقة |
|------|-------|
| Pit Volume | ± 1 bbl |
| Flow Rate | مستمر |
| Pump Pressure | مستمر |

---

#### **3️⃣ تصرف بسرعة!**

**الهدف: Shut-in في أقل من دقيقتين!**
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Monitoring Requirements:

| Parameter | Accuracy | Method |
|-----------|----------|--------|
| Pit volume | ± 1 bbl | Continuous |
| Flow rate | ± 10% | Paddle/sensor |
| Pump pressure | ± 50 psi | Gauge |

### 📋 Drill Requirements:

| Drill | Frequency |
|-------|-----------|
| BOP drill | Weekly |
| Kick drill | Weekly |
| Muster drill | Monthly |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Pit volume monitoring accuracy:**

- A) ± 5 bbl
- B) **± 1 bbl** ✅
- C) ± 10 bbl
- D) Not important
        """
    },
    
    "Well Control Barriers": {
        "simple": """
## 🟢 ببساطة كده...

### 🎯 قواعد الـ Barriers:

---

#### **1️⃣ لازم 2 Barriers دايماً!**

Primary + Secondary

---

#### **2️⃣ لازم تختبرهم!**

مش بس موجودين، لازم يكونوا شغالين!

---

#### **3️⃣ ما تشيلهمش مع بعض!**

دايماً واحد موجود على الأقل!
        """,
        
        "technical": """
## 🟡 Technical Knowledge

### 📊 Barrier Requirements:

| Requirement | Explanation |
|-------------|-------------|
| Minimum 2 | Always have backup |
| Independent | Different failure modes |
| Tested | Verified working |
| Documented | Status recorded |

### 📋 Verification:

| Barrier | Test |
|---------|------|
| Mud | Weight checks |
| BOP | Pressure test |
| Casing | Pressure test |
        """,
        
        "exam": """
## 🔴 IWCF Exam Format

### ❓ Question 1:

**Q: Barriers must be:**

- A) Assumed working
- B) **Tested and verified** ✅
- C) Installed only
- D) Optional

---

### ❓ Question 2:

**Q: Minimum barriers required:**

- A) One
- B) **Two** ✅
- C) Three
- D) Depends
        """
    },
}
# ═══════════════════════════════════════════════════════
# ❓ PRACTICE QUESTIONS الموسّعة
# ═══════════════════════════════════════════════════════

PRACTICE_QUESTIONS = {
    "Introduction to Well Control": [
        {
            "question": "What is the PRIMARY well control barrier?",
            "options": ["BOP Stack", "Casing", "Mud column (Hydrostatic Pressure)", "Cement"],
            "correct": 2,
            "solution": "The mud column provides hydrostatic pressure that prevents formation fluids from entering the wellbore. This is the FIRST line of defense - the PRIMARY barrier."
        },
        {
            "question": "What is the SECONDARY well control barrier?",
            "options": ["Mud weight", "BOP System", "Drill string", "Kelly"],
            "correct": 1,
            "solution": "The BOP (Blowout Preventer) is the SECONDARY barrier. It's only used AFTER the primary barrier (mud) has failed."
        },
        {
            "question": "How many barriers should be in place at ALL times?",
            "options": ["One", "Two (minimum)", "Three", "Four"],
            "correct": 1,
            "solution": "Industry standard requires MINIMUM 2 barriers at all times. If one fails, the other provides backup protection."
        },
        {
            "question": "A 'kick' is defined as:",
            "options": ["Mud leaving the wellbore", "Formation fluid entering the wellbore", "Pipe stuck in hole", "Lost circulation"],
            "correct": 1,
            "solution": "A KICK occurs when formation fluid (gas, oil, or water) enters the wellbore due to formation pressure exceeding hydrostatic pressure."
        },
    ],
    
    "Hydrostatic Pressure": [
        {
            "question": "Calculate HP: MW = 12 ppg, TVD = 10,000 ft",
            "options": ["5,200 psi", "6,000 psi", "6,240 psi", "7,200 psi"],
            "correct": 2,
            "solution": "HP = 0.052 × MW × TVD\nHP = 0.052 × 12 × 10,000\nHP = 6,240 psi"
        },
        {
            "question": "What MW is needed to create 5,200 psi at 10,000 ft?",
            "options": ["8 ppg", "10 ppg", "12 ppg", "14 ppg"],
            "correct": 1,
            "solution": "MW = HP / (0.052 × TVD)\nMW = 5,200 / (0.052 × 10,000)\nMW = 5,200 / 520\nMW = 10 ppg"
        },
        {
            "question": "Calculate HP: MW = 11 ppg, TVD = 8,500 ft",
            "options": ["4,500 psi", "4,862 psi", "5,200 psi", "5,500 psi"],
            "correct": 1,
            "solution": "HP = 0.052 × MW × TVD\nHP = 0.052 × 11 × 8,500\nHP = 4,862 psi"
        },
        {
            "question": "HP is affected by:",
            "options": ["Hole diameter", "Mud weight and TVD only", "Pump rate", "Pipe size"],
            "correct": 1,
            "solution": "HP = 0.052 × MW × TVD\nOnly MW and TVD affect HP! Hole diameter, pipe size, and pump rate have NO effect."
        },
        {
            "question": "Well data: MD = 12,000 ft, TVD = 10,000 ft, MW = 11 ppg. Calculate HP.",
            "options": ["5,720 psi (using TVD)", "6,864 psi (using MD)", "5,200 psi", "6,500 psi"],
            "correct": 0,
            "solution": "ALWAYS use TVD, not MD!\nHP = 0.052 × 11 × 10,000 = 5,720 psi\n(NOT 0.052 × 11 × 12,000)"
        },
        {
            "question": "At what depth will 12 ppg mud create 6,240 psi?",
            "options": ["8,000 ft", "9,000 ft", "10,000 ft", "11,000 ft"],
            "correct": 2,
            "solution": "TVD = HP / (0.052 × MW)\nTVD = 6,240 / (0.052 × 12)\nTVD = 6,240 / 0.624\nTVD = 10,000 ft"
        },
    ],
    
    "Pressure Concepts": [
        {
            "question": "Well: TVD=10,000 ft, MW=10 ppg, FP=5,500 psi. Status?",
            "options": ["Overbalanced", "Balanced", "Underbalanced", "Cannot determine"],
            "correct": 2,
            "solution": "HP = 0.052 × 10 × 10,000 = 5,200 psi\nFP = 5,500 psi\nHP (5,200) < FP (5,500)\n∴ UNDERBALANCED = Kick risk!"
        },
        {
            "question": "Normal formation pressure gradient is approximately:",
            "options": ["0.433 psi/ft", "0.465 psi/ft", "0.520 psi/ft", "0.650 psi/ft"],
            "correct": 1,
            "solution": "Normal formation pressure gradient = 0.465 psi/ft\nThis is equivalent to approximately 8.94 ppg"
        },
        {
            "question": "'Overbalanced' means:",
            "options": ["FP > HP", "HP > FP", "HP = FP", "No mud in well"],
            "correct": 1,
            "solution": "Overbalanced means HP > FP (Hydrostatic Pressure exceeds Formation Pressure)\nThis is the SAFE condition - no kick will occur."
        },
    ],
    
    "Kick Indicators": [
        {
            "question": "Most RELIABLE kick indicator is:",
            "options": ["Drilling break", "Pit gain", "Connection gas", "Pump pressure drop"],
            "correct": 1,
            "solution": "PIT GAIN is the MOST reliable kick indicator!\nIt directly shows that formation fluid has entered the wellbore."
        },
        {
            "question": "All are PRIMARY kick indicators EXCEPT:",
            "options": ["Pit gain", "Flow increase", "Drilling break", "Pump pressure decrease"],
            "correct": 2,
            "solution": "Drilling break is a SECONDARY indicator!\nPrimary indicators: Pit gain, Flow increase, Pump pressure drop, Flow with pumps off"
        },
        {
            "question": "You notice 10 bbl pit gain. First action?",
            "options": ["Continue drilling", "Increase pump rate", "Stop pumps and shut in", "Call supervisor first"],
            "correct": 2,
            "solution": "Any confirmed pit gain requires IMMEDIATE action!\nFirst: STOP PUMPS, then shut in the well."
        },
        {
            "question": "Which is a SECONDARY indicator?",
            "options": ["Pit gain", "Flow increase", "Drilling break", "Flow with pumps off"],
            "correct": 2,
            "solution": "Drilling break is a SECONDARY indicator.\nIt's a warning sign that requires monitoring, not immediate shut-in."
        },
    ],
    
    "Primary vs Secondary Barriers": [
        {
            "question": "Primary barrier in a drilling well is:",
            "options": ["BOP", "Casing", "Mud column", "Cement"],
            "correct": 2,
            "solution": "Primary barrier = MUD COLUMN\nHydrostatic pressure prevents kicks from occurring."
        },
        {
            "question": "Minimum number of barriers required:",
            "options": ["One", "Two", "Three", "Four"],
            "correct": 1,
            "solution": "MINIMUM TWO barriers at all times!\nPrimary (mud) + Secondary (BOP)"
        },
        {
            "question": "The BOP is classified as:",
            "options": ["Primary barrier", "Secondary barrier", "Tertiary barrier", "Not a barrier"],
            "correct": 1,
            "solution": "BOP = SECONDARY barrier\nIt's the backup when the primary barrier (mud) fails."
        },
    ],
    
    "Formation Pressure": [
        {
            "question": "Calculate FP: TVD=12,000 ft, MW=11 ppg, SIDPP=350 psi",
            "options": ["6,500 psi", "6,864 psi", "7,214 psi", "7,500 psi"],
            "correct": 2,
            "solution": "FP = HP + SIDPP\nHP = 0.052 × 11 × 12,000 = 6,864 psi\nFP = 6,864 + 350 = 7,214 psi"
        },
        {
            "question": "Which pressure to use for FP calculation?",
            "options": ["SICP", "SIDPP", "Both", "Neither"],
            "correct": 1,
            "solution": "Use SIDPP only!\nFP = HP + SIDPP\nSICP is contaminated by the influx gradient."
        },
        {
            "question": "FP gradient = 0.55 psi/ft. This is:",
            "options": ["Normal", "Abnormal (higher than normal)", "Subnormal", "Cannot determine"],
            "correct": 1,
            "solution": "Normal gradient = 0.465 psi/ft\n0.55 > 0.465\n∴ ABNORMAL (higher than normal) pressure"
        },
    ],
    
    "Pressure Gradients": [
        {
            "question": "What gradient does 13 ppg mud create?",
            "options": ["0.520 psi/ft", "0.624 psi/ft", "0.676 psi/ft", "0.728 psi/ft"],
            "correct": 2,
            "solution": "Gradient = 0.052 × MW\nGradient = 0.052 × 13 = 0.676 psi/ft"
        },
        {
            "question": "What MW gives 0.572 psi/ft gradient?",
            "options": ["10 ppg", "11 ppg", "12 ppg", "13 ppg"],
            "correct": 1,
            "solution": "MW = Gradient / 0.052\nMW = 0.572 / 0.052 = 11 ppg"
        },
        {
            "question": "Calculate pressure at 8,000 ft with gradient 0.52 psi/ft:",
            "options": ["4,000 psi", "4,160 psi", "4,500 psi", "5,200 psi"],
            "correct": 1,
            "solution": "Pressure = Gradient × TVD\nPressure = 0.52 × 8,000 = 4,160 psi"
        },
    ],
    
    "Equivalent Circulating Density (ECD)": [
        {
            "question": "Calculate ECD: MW=11 ppg, APL=312 psi, TVD=12,000 ft",
            "options": ["11.0 ppg", "11.5 ppg", "12.0 ppg", "12.5 ppg"],
            "correct": 1,
            "solution": "ECD = MW + (APL / 0.052 / TVD)\nECD = 11 + (312 / 0.052 / 12,000)\nECD = 11 + (312 / 624)\nECD = 11 + 0.5 = 11.5 ppg"
        },
        {
            "question": "ECD is ALWAYS:",
            "options": ["Less than MW", "Equal to MW", "Greater than MW when circulating", "Zero when not circulating"],
            "correct": 2,
            "solution": "ECD > MW when circulating (due to friction/APL)\nECD = MW when static (not circulating)"
        },
        {
            "question": "Increasing pump rate will cause ECD to:",
            "options": ["Decrease", "Stay the same", "Increase", "Become zero"],
            "correct": 2,
            "solution": "Higher pump rate = More friction = Higher APL = Higher ECD"
        },
    ],
    
    "MAASP Calculations": [
        {
            "question": "Calculate MAASP: LOT=14.5 ppg, MW=11 ppg, Shoe TVD=6,000 ft",
            "options": ["780 psi", "1,092 psi", "1,200 psi", "1,500 psi"],
            "correct": 1,
            "solution": "MAASP = (LOT - MW) × 0.052 × Shoe TVD\nMAASP = (14.5 - 11) × 0.052 × 6,000\nMAASP = 3.5 × 0.052 × 6,000 = 1,092 psi"
        },
        {
            "question": "If you increase MW, MAASP will:",
            "options": ["Increase", "Decrease", "Stay same", "Double"],
            "correct": 1,
            "solution": "MAASP = (LOT - MW) × 0.052 × TVD\nHigher MW → Smaller (LOT - MW) → Lower MAASP"
        },
        {
            "question": "For MAASP calculation, use:",
            "options": ["Total depth", "Casing shoe TVD", "Measured depth", "Bit depth"],
            "correct": 1,
            "solution": "Always use CASING SHOE TVD!\nThis is the weakest point in the open hole section."
        },
        {
            "question": "MAASP with LOT=14 ppg, MW=12 ppg, Shoe=5,000 ft:",
            "options": ["420 psi", "520 psi", "624 psi", "728 psi"],
            "correct": 1,
            "solution": "MAASP = (14 - 12) × 0.052 × 5,000\nMAASP = 2 × 0.052 × 5,000 = 520 psi"
        },
    ],
    
    "Shut-in Procedures": [
        {
            "question": "First action when kick detected:",
            "options": ["Close BOP", "Stop pumps", "Record pressures", "Call supervisor"],
            "correct": 1,
            "solution": "First action: STOP PUMPS!\nSequence: Stop → Raise → Close → Record (S.R.C.R)"
        },
        {
            "question": "Hard shut-in means:",
            "options": ["Closing BOP slowly", "Close BOP first, then open choke", "Open choke first, then close BOP", "Using high pressure"],
            "correct": 1,
            "solution": "Hard shut-in: Close BOP FIRST, then open choke line.\nThis is the STANDARD method - faster response."
        },
        {
            "question": "Target time for complete shut-in:",
            "options": ["5 minutes", "Less than 2 minutes", "10 minutes", "No target"],
            "correct": 1,
            "solution": "Target: < 2 minutes from kick detection to BOP closed!"
        },
        {
            "question": "Correct shut-in sequence is:",
            "options": ["Close BOP, Stop pumps, Record", "Stop pumps, Raise kelly, Close BOP, Record", "Record, Stop, Close", "Call supervisor, Stop, Close"],
            "correct": 1,
            "solution": "S.R.C.R:\nStop pumps → Raise kelly → Close BOP → Record pressures"
        },
    ],
    
    "SIDPP and SICP": [
        {
            "question": "SICP > SIDPP indicates:",
            "options": ["Water kick", "Oil kick", "Gas kick", "No kick"],
            "correct": 2,
            "solution": "SICP > SIDPP = GAS kick!\nGas is lighter than mud, so more surface pressure is needed in the annulus to balance BHP."
        },
        {
            "question": "Which pressure to use for kill calculations?",
            "options": ["SICP", "SIDPP", "Both", "Neither"],
            "correct": 1,
            "solution": "Use SIDPP for all kill calculations!\nFP = HP + SIDPP\nKMW = OMW + (SIDPP / 0.052 / TVD)"
        },
        {
            "question": "SICP ≈ SIDPP indicates:",
            "options": ["Gas kick", "Liquid kick (oil/water)", "No kick", "BOP leak"],
            "correct": 1,
            "solution": "SICP ≈ SIDPP indicates a LIQUID kick (oil or water).\nLiquid has similar density to mud, so pressure difference is small."
        },
    ],
    
    "Driller's Method": [
        {
            "question": "Calculate ICP: SIDPP=600 psi, SCR=500 psi",
            "options": ["100 psi", "500 psi", "600 psi", "1,100 psi"],
            "correct": 3,
            "solution": "ICP = SIDPP + SCR\nICP = 600 + 500 = 1,100 psi"
        },
        {
            "question": "Calculate FCP: SCR=400 psi, KMW=11 ppg, OMW=10 ppg",
            "options": ["400 psi", "440 psi", "500 psi", "550 psi"],
            "correct": 1,
            "solution": "FCP = SCR × (KMW / OMW)\nFCP = 400 × (11 / 10)\nFCP = 400 × 1.1 = 440 psi"
        },
        {
            "question": "Driller's Method uses how many circulations?",
            "options": ["One", "Two", "Three", "Four"],
            "correct": 1,
            "solution": "Driller's Method = TWO circulations\n1st: Circulate out kick with original mud\n2nd: Pump kill mud"
        },
        {
            "question": "During first circulation, hold constant:",
            "options": ["Casing pressure", "Drillpipe pressure (ICP)", "Both", "Neither"],
            "correct": 1,
            "solution": "During first circulation: Hold DRILLPIPE pressure constant at ICP!"
        },
        {
            "question": "Calculate KMW: OMW=10 ppg, SIDPP=520 psi, TVD=10,000 ft",
            "options": ["10.5 ppg", "11.0 ppg", "11.5 ppg", "12.0 ppg"],
            "correct": 1,
            "solution": "KMW = OMW + (SIDPP / 0.052 / TVD)\nKMW = 10 + (520 / 520) = 11.0 ppg"
        },
    ],
    
    "Wait and Weight Method": [
        {
            "question": "Wait and Weight uses how many circulations?",
            "options": ["One", "Two", "Three", "Four"],
            "correct": 0,
            "solution": "Wait & Weight = ONE circulation only!\nKill mud is pumped from the start."
        },
        {
            "question": "Main advantage of Wait & Weight over Driller's:",
            "options": ["Simpler", "Lower casing pressure", "No calculations", "Faster to start"],
            "correct": 1,
            "solution": "Wait & Weight gives LOWER CASING pressure.\nThis is better for weak formations."
        },
        {
            "question": "Wait and Weight is preferred when:",
            "options": ["Quick action needed", "Formation is weak", "No mud available", "Gas kick only"],
            "correct": 1,
            "solution": "Wait & Weight is preferred for WEAK formations because it results in lower maximum casing pressure."
        },
    ],
    
    "Volumetric Method": [
        {
            "question": "Volumetric method is used when:",
            "options": ["Kick is too large", "MW is too light", "Circulation is not possible", "Gas kick only"],
            "correct": 2,
            "solution": "Volumetric is used when NO CIRCULATION is possible!\nExamples: Stuck pipe, no pumps, no drillstring"
        },
        {
            "question": "In Volumetric Method:",
            "options": ["Pump at high rate", "Pump at kill rate", "No pumping is done", "Alternate pumping"],
            "correct": 2,
            "solution": "Volumetric = NO PUMPING!\nGas migrates naturally, and mud is bled to maintain constant BHP."
        },
        {
            "question": "Volumetric Method maintains constant:",
            "options": ["Surface pressure", "Drillpipe pressure", "Bottomhole pressure", "Pump rate"],
            "correct": 2,
            "solution": "Goal of Volumetric: Maintain constant BOTTOMHOLE PRESSURE (BHP)!\nAs gas rises and expands, bleed mud to compensate."
        },
    ],
    
    "Bullheading": [
        {
            "question": "Bullheading is most appropriate for:",
            "options": ["Normal gas kick", "H2S kick", "All kicks", "Small kicks only"],
            "correct": 1,
            "solution": "Bullheading is best for H2S kicks!\nPushes the toxic gas back into the formation instead of bringing it to surface."
        },
        {
            "question": "Main risk of bullheading:",
            "options": ["Too slow", "Formation breakdown", "BOP failure", "Pump failure"],
            "correct": 1,
            "solution": "Main risk: FORMATION BREAKDOWN!\nHigh pressure may fracture the formation, causing underground blowout."
        },
    ],
    
    "Kill Sheet Calculations": [
        {
            "question": "Calculate KMW: OMW=10 ppg, SIDPP=400 psi, TVD=10,000 ft",
            "options": ["10.5 ppg", "10.77 ppg", "11.0 ppg", "11.5 ppg"],
            "correct": 1,
            "solution": "KMW = OMW + (SIDPP / 0.052 / TVD)\nKMW = 10 + (400 / 520)\nKMW = 10 + 0.77 = 10.77 ppg"
        },
        {
            "question": "FCP is reached when:",
            "options": ["Kill mud at surface", "Kill mud at bit", "Kick at surface", "Well is dead"],
            "correct": 1,
            "solution": "FCP is reached when KILL MUD arrives at the BIT.\nAfter this, maintain constant FCP until kill mud reaches surface."
        },
        {
            "question": "FCP compared to ICP is always:",
            "options": ["Greater", "Equal", "Less", "Zero"],
            "correct": 2,
            "solution": "FCP < ICP (always!)\nFCP = SCR × (KMW/OMW)\nICP = SIDPP + SCR"
        },
    ],
    
    "BOP Components": [
        {
            "question": "Which BOP element seals on open hole?",
            "options": ["Annular", "Pipe rams", "Blind rams", "Shear rams"],
            "correct": 2,
            "solution": "BLIND RAMS seal open hole (no pipe present).\nThey close completely across the wellbore."
        },
        {
            "question": "Which can seal on ANY pipe size?",
            "options": ["Pipe rams", "Blind rams", "Annular preventer", "Shear rams"],
            "correct": 2,
            "solution": "ANNULAR PREVENTER seals on ANY size!\nThe flexible rubber element conforms to any shape."
        },
        {
            "question": "Shear rams are used:",
            "options": ["Routinely", "For stripping", "As last resort emergency", "First response"],
            "correct": 2,
            "solution": "Shear rams = LAST RESORT only!\nThey cut and destroy the pipe - cannot be reversed."
        },
    ],
    
    "Accumulator System": [
        {
            "question": "Accumulator bottles are precharged with:",
            "options": ["Air", "Oxygen", "Nitrogen", "Hydraulic fluid"],
            "correct": 2,
            "solution": "Accumulators use NITROGEN (N₂) precharge.\nNitrogen is inert and won't ignite."
        },
        {
            "question": "After closing all BOPs, minimum accumulator pressure:",
            "options": ["0 psi", "100 psi", "200 psi", "500 psi"],
            "correct": 2,
            "solution": "Must have 200 psi remaining after closing all BOPs.\nThis ensures emergency reserve capacity."
        },
    ],
    
    "Gas Behavior (Boyle's Law)": [
        {
            "question": "Gas at 4,000 psi = 10 bbls. Volume at 400 psi?",
            "options": ["10 bbls", "50 bbls", "100 bbls", "1,000 bbls"],
            "correct": 2,
            "solution": "P₁V₁ = P₂V₂\nV₂ = P₁ × V₁ / P₂\nV₂ = 4,000 × 10 / 400 = 100 bbls"
        },
        {
            "question": "Most rapid gas expansion occurs:",
            "options": ["At bottom", "Mid-well", "Near surface", "Equal everywhere"],
            "correct": 2,
            "solution": "Near surface = FASTEST expansion!\nLow pressure = Big volume increase (Boyle's Law)"
        },
        {
            "question": "Gas at 5,000 psi = 20 bbls. Volume at 500 psi?",
            "options": ["20 bbls", "100 bbls", "200 bbls", "500 bbls"],
            "correct": 2,
            "solution": "V₂ = V₁ × (P₁/P₂)\nV₂ = 20 × (5,000/500)\nV₂ = 20 × 10 = 200 bbls"
        },
    ],
    
    "Gas Migration": [
        {
            "question": "Typical gas migration rate is:",
            "options": ["100 ft/hour", "500 ft/hour", "1,000 ft/hour", "5,000 ft/hour"],
            "correct": 2,
            "solution": "Typical gas migration rate: ~1,000 ft/hour\n10,000 ft well = approximately 10 hours to surface"
        },
        {
            "question": "Gas migrates because:",
            "options": ["Pump action", "It is lighter than mud", "Formation pressure", "BOP opening"],
            "correct": 1,
            "solution": "Gas migrates due to BUOYANCY - it's lighter than the surrounding mud.\nGas naturally rises through the mud column."
        },
    ],
    
    "Lost Circulation": [
        {
            "question": "During well kill, losses occur. You should:",
            "options": ["Shut in completely", "Continue at reduced rate", "Increase pump rate", "Stop all operations"],
            "correct": 1,
            "solution": "CONTINUE AT REDUCED RATE!\nStopping would let BHP drop, potentially causing a larger kick."
        },
        {
            "question": "Lost circulation increases risk of:",
            "options": ["Stuck pipe", "Kick", "Both", "Neither"],
            "correct": 2,
            "solution": "Lost circulation increases risk of BOTH!\nLosing mud reduces HP, which can cause kick AND stuck pipe."
        },
    ],
    
    "Underground Blowout": [
        {
            "question": "Main cause of underground blowout during kill:",
            "options": ["Low pump rate", "Exceeding MAASP", "Light mud", "Slow response"],
            "correct": 1,
            "solution": "EXCEEDING MAASP causes formation breakdown at the shoe!\nThe kick then flows into the fractured zone instead of to surface."
        },
        {
            "question": "Sign of underground blowout:",
            "options": ["Increasing SIDPP", "Stable SIDPP with dropping pit", "Stable pit, dropping SIDPP", "Increasing pit"],
            "correct": 2,
            "solution": "Underground blowout signs:\n- SIDPP dropping without explanation\n- Pit level stable (not gaining)\n- Kick going into formation, not up"
        },
    ],
    
    "H2S Considerations": [
        {
            "question": "H2S at 100 ppm will:",
            "options": ["Be easily smelled", "Paralyze sense of smell", "Have no effect", "Cause mild headache only"],
            "correct": 1,
            "solution": "At 100 ppm, H2S PARALYZES your sense of smell!\nYou CAN'T detect it by smell anymore - extremely dangerous!"
        },
        {
            "question": "Best kill method for H2S kick:",
            "options": ["Driller's Method", "Wait and Weight", "Bullheading", "Volumetric"],
            "correct": 2,
            "solution": "BULLHEADING is best for H2S!\nPushes the toxic gas back into formation - never comes to surface."
        },
        {
            "question": "IDLH (Immediately Dangerous to Life) for H2S:",
            "options": ["10 ppm", "50 ppm", "100 ppm", "500 ppm"],
            "correct": 2,
            "solution": "IDLH for H2S = 100 ppm\nAbove this concentration is immediately dangerous to life and health."
        },
    ],
    
    "IWCF Standards": [
        {
            "question": "IWCF certificate is valid for:",
            "options": ["1 year", "2 years", "5 years", "Lifetime"],
            "correct": 1,
            "solution": "IWCF validity = 2 years\nMust recertify before expiry to maintain certification."
        },
        {
            "question": "Pass mark for IWCF exam:",
            "options": ["50%", "60%", "70%", "80%"],
            "correct": 2,
            "solution": "IWCF pass mark = 70%\n(35 correct out of 50 questions)"
        },
        {
            "question": "IWCF exam has how many questions?",
            "options": ["25", "40", "50", "100"],
            "correct": 2,
            "solution": "IWCF exam = 50 questions\n2 hours duration, multiple choice format."
        },
    ],
    
    "Well Control Barriers": [
        {
            "question": "Barriers must be:",
            "options": ["Assumed working", "Tested and verified", "Installed only", "Optional"],
            "correct": 1,
            "solution": "Barriers must be TESTED AND VERIFIED!\nNever assume a barrier works without testing."
        },
        {
            "question": "Primary barrier for a drilling well:",
            "options": ["BOP", "Casing", "Mud column", "Cement"],
            "correct": 2,
            "solution": "Primary barrier = MUD COLUMN\nProvides hydrostatic pressure to prevent kicks."
        },
    ],
}

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════

if 'selected_module_id' not in st.session_state:
    st.session_state.selected_module_id = None

if 'selected_topic_name' not in st.session_state:
    st.session_state.selected_topic_name = None

if 'completed_topics' not in st.session_state:
    # Load from Data Manager if available
    if DATA_MANAGER_AVAILABLE:
        try:
            data = load_progress()
            st.session_state.completed_topics = [t['topic'] for t in data['modules'].get('topics_completed', [])]
        except:
            st.session_state.completed_topics = []
    else:
        st.session_state.completed_topics = []

if 'bookmarked_topics' not in st.session_state:
    st.session_state.bookmarked_topics = []

if 'current_topic_start' not in st.session_state:
    st.session_state.current_topic_start = None

if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = []

if 'total_xp' not in st.session_state:
    if DATA_MANAGER_AVAILABLE:
        try:
            data = load_progress()
            st.session_state.total_xp = data['achievements']['xp_total']
        except:
            st.session_state.total_xp = 0
    else:
        st.session_state.total_xp = 0

if 'study_streak' not in st.session_state:
    if DATA_MANAGER_AVAILABLE:
        try:
            data = load_progress()
            st.session_state.study_streak = data['user'].get('study_streak', 0)
        except:
            st.session_state.study_streak = 0
    else:
        st.session_state.study_streak = 0

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="learn-header">
    <h1>📚 Interactive Learning Center</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Master IWCF Concepts with the Elshamy 3-Layer Method™</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        🟢 Simple → 🟡 Technical → 🔴 Exam Ready
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 SIDEBAR
# ═══════════════════════════════════════════════════════

# User Stats
st.sidebar.markdown("### 👤 Your Progress")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("⭐ XP", st.session_state.total_xp)
with col2:
    st.metric("🔥 Streak", f"{st.session_state.study_streak}d")

# Level Badge
user_level = get_user_level(st.session_state.total_xp)
st.sidebar.markdown(f"""
<div style="text-align: center; margin: 1rem 0;">
    <span class="level-badge">🏆 {user_level}</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Module List
st.sidebar.markdown("### 📚 Modules")

for mod_id, mod_data in MODULES.items():
    # Calculate progress
    mod_topics = [t["name"] for t in TOPICS.get(mod_id, [])]
    completed_in_mod = len([t for t in mod_topics if t in st.session_state.completed_topics])
    total = len(mod_topics)
    progress = int((completed_in_mod / total * 100)) if total > 0 else 0
    
    # Color and badge based on progress
    if progress == 100:
        color = "#10B981"
        badge = "✅"
    elif progress > 0:
        color = "#F59E0B"
        badge = "🔄"
    else:
        color = "#9CA3AF"
        badge = "📚"
    
    st.sidebar.markdown(f"""
    <div class="sidebar-card" style="border-left-color: {color};">
        <strong>{badge} Module {mod_id}</strong><br>
        <span style="font-size: 0.85rem; color: #6B7280;">{mod_data['name'][:22]}...</span>
        <div class="progress-mini">
            <div class="progress-mini-fill" style="width: {progress}%; background: {color};"></div>
        </div>
        <span style="font-size: 0.75rem; color: {color};">{completed_in_mod}/{total} topics</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button(f"Open Module {mod_id}", key=f"mod_{mod_id}", use_container_width=True):
        st.session_state.selected_module_id = mod_id
        st.session_state.selected_topic_name = None
        st.rerun()

# Overall Progress
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Overall Progress")

total_topics = sum(len(TOPICS.get(mid, [])) for mid in MODULES.keys())
completed_topics_count = len(st.session_state.completed_topics)
overall_progress = (completed_topics_count / total_topics * 100) if total_topics > 0 else 0

st.sidebar.progress(overall_progress / 100)
st.sidebar.caption(f"{completed_topics_count}/{total_topics} Topics ({overall_progress:.0f}%)")

# Bookmarked Topics
if st.session_state.bookmarked_topics:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔖 Bookmarked")
    
    for bookmarked in st.session_state.bookmarked_topics[:3]:
        if st.sidebar.button(f"📌 {bookmarked[:20]}...", key=f"bm_{bookmarked}", use_container_width=True):
            for mid, topics in TOPICS.items():
                if bookmarked in [t['name'] for t in topics]:
                    st.session_state.selected_module_id = mid
                    st.session_state.selected_topic_name = bookmarked
                    st.rerun()
                    break
    
    if len(st.session_state.bookmarked_topics) > 3:
        st.sidebar.caption(f"+{len(st.session_state.bookmarked_topics) - 3} more...")

st.sidebar.markdown("---")

# ═══════════════════════════════════════════════════════
# 📖 MAIN CONTENT
# ═══════════════════════════════════════════════════════

if st.session_state.selected_module_id is None:
    # Welcome Page
    st.markdown("## 👋 Welcome to the Learning Center!")
    
    st.info("""
    **📚 How to use the Elshamy 3-Layer Method™:**
    
    1. **Select a Module** from the sidebar (Modules 1-8)
    2. **Choose a Topic** to study
    3. **Study with 3 Layers:**
       - 🟢 **Simple**: Easy-to-understand explanation in Arabic/English
       - 🟡 **Technical**: Detailed field knowledge with formulas
       - 🔴 **Exam**: IWCF exam format questions and tips
    4. **Answer Practice Questions** to test your understanding
    5. **Mark as Completed** and earn **XP**! 🎉
    """)
    
    st.markdown("---")
    
    # Stats Overview
    st.markdown("### 📊 Your Learning Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="text-align: center; padding: 1rem;">
            <h2 style="margin: 0; color: #1E40AF;">📚 {completed_topics_count}</h2>
            <p style="margin: 0.5rem 0 0 0; color: #6B7280;">Topics Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="text-align: center; padding: 1rem;">
            <h2 style="margin: 0; color: #10B981;">📈 {overall_progress:.0f}%</h2>
            <p style="margin: 0.5rem 0 0 0; color: #6B7280;">Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="text-align: center; padding: 1rem;">
            <h2 style="margin: 0; color: #F59E0B;">⭐ {st.session_state.total_xp}</h2>
            <p style="margin: 0.5rem 0 0 0; color: #6B7280;">Total XP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card" style="text-align: center; padding: 1rem;">
            <h2 style="margin: 0; color: #EF4444;">🔥 {st.session_state.study_streak}</h2>
            <p style="margin: 0.5rem 0 0 0; color: #6B7280;">Day Streak</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Continue Learning
    st.markdown("### 🚀 Quick Start")
    
    # Find next uncompleted topic
    next_topic = None
    next_module = None
    
    for mid in range(1, 9):
        for topic in TOPICS.get(mid, []):
            if topic['name'] not in st.session_state.completed_topics:
                next_topic = topic
                next_module = mid
                break
        if next_topic:
            break
    
    if next_topic:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="tip-box">
                <h4>📖 Continue Learning</h4>
                <p><strong>Next Topic:</strong> {next_topic['name']}</p>
                <p><strong>Module {next_module}:</strong> {MODULES[next_module]['name']}</p>
                <p>⏱️ Estimated time: {next_topic['time']} minutes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("▶️ Start Learning", use_container_width=True, type="primary"):
                st.session_state.selected_module_id = next_module
                st.session_state.selected_topic_name = next_topic['name']
                st.session_state.current_topic_start = datetime.now()
                st.rerun()
    else:
        st.success("🎉 Congratulations! You've completed all topics!")
    
    st.markdown("---")
    
    # Module Overview
    st.markdown("### 📚 All Modules")
    
    cols = st.columns(4)
    
    for idx, (mod_id, mod_data) in enumerate(MODULES.items()):
        with cols[idx % 4]:
            mod_topics = TOPICS.get(mod_id, [])
            completed = len([t for t in mod_topics if t['name'] in st.session_state.completed_topics])
            total = len(mod_topics)
            pct = int((completed / total * 100)) if total > 0 else 0
            
            color = "#10B981" if pct == 100 else "#F59E0B" if pct > 0 else "#9CA3AF"
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 12px; 
                        border-top: 4px solid {color}; margin-bottom: 1rem;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0;">{mod_data['icon']} Module {mod_id}</h4>
                <p style="font-size: 0.85rem; color: #6B7280; margin: 0.5rem 0;">{mod_data['name']}</p>
                <div class="progress-mini">
                    <div class="progress-mini-fill" style="width: {pct}%; background: {color};"></div>
                </div>
                <span style="font-size: 0.8rem; color: {color};">{completed}/{total} • {pct}%</span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Open", key=f"open_mod_{mod_id}", use_container_width=True):
                st.session_state.selected_module_id = mod_id
                st.rerun()

else:
    # Module/Topic View
    mod_id = st.session_state.selected_module_id
    mod_data = MODULES[mod_id]
    topics = TOPICS.get(mod_id, [])
    
    # Back button
    if st.button("← Back to All Modules"):
        st.session_state.selected_module_id = None
        st.session_state.selected_topic_name = None
        st.rerun()
    
    st.markdown(f"## {mod_data['icon']} Module {mod_id}: {mod_data['name']}")
    
    # Module info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Difficulty:** {mod_data['difficulty']}")
    with col2:
        st.markdown(f"**Topics:** {len(topics)}")
    with col3:
        completed_in_mod = len([t for t in topics if t['name'] in st.session_state.completed_topics])
        st.markdown(f"**Progress:** {completed_in_mod}/{len(topics)}")
    
    st.markdown("---")
    
    if st.session_state.selected_topic_name is None:
        # Topic List
        st.markdown("### 📖 Topics in this Module:")
        
        for topic in topics:
            is_completed = topic["name"] in st.session_state.completed_topics
            is_bookmarked = topic["name"] in st.session_state.bookmarked_topics
            
            emoji = "✅" if is_completed else "📖"
            color = "#10B981" if is_completed else "#E5E7EB"
            
            col1, col2, col3 = st.columns([5, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="module-card" style="border-left-color: {color};">
                    <h4 style="margin: 0;">{emoji} {topic['name']}</h4>
                    <span style="color: #6B7280;">⏱️ {topic['time']} min</span>
                    {' <span class="xp-badge">+' + str(topic.get('xp', 25)) + ' XP</span>' if not is_completed else ' <span style="color: #10B981; font-weight: bold;">✓ Completed</span>'}
                    {' <span style="color: #F59E0B;">🔖</span>' if is_bookmarked else ''}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📖 Study", key=f"study_{topic['id']}", use_container_width=True):
                    st.session_state.selected_topic_name = topic["name"]
                    st.session_state.current_topic_start = datetime.now()
                    st.rerun()
            
            with col3:
                bm_emoji = "🔖" if is_bookmarked else "📌"
                if st.button(bm_emoji, key=f"bm_btn_{topic['id']}", use_container_width=True):
                    if is_bookmarked:
                        st.session_state.bookmarked_topics.remove(topic["name"])
                    else:
                        st.session_state.bookmarked_topics.append(topic["name"])
                    st.rerun()
    
    else:
        # Topic Content View
        topic_name = st.session_state.selected_topic_name
        content = CONTENT.get(topic_name, {})
        
        # Back to topics
        if st.button("← Back to Topics"):
            st.session_state.selected_topic_name = None
            st.rerun()
        
        st.markdown(f"## 📖 {topic_name}")
        
        # Layer selection
        st.markdown("### Choose Your Learning Layer:")
        
        layer = st.radio(
            "",
            ["🟢 Simple (Easy Explanation)", "🟡 Technical (Detailed Knowledge)", "🔴 Exam (IWCF Format)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Display content
        st.markdown('<div class="topic-content">', unsafe_allow_html=True)
        
        if "Simple" in layer:
            st.markdown(content.get("simple", "Content coming soon... 🚧"))
        elif "Technical" in layer:
            st.markdown(content.get("technical", "Content coming soon... 🚧"))
        else:
            st.markdown(content.get("exam", "Content coming soon... 🚧"))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ═══════════════════════════════════════════════════
        # 🎯 PRACTICE QUESTIONS
        # ═══════════════════════════════════════════════════
        
        if topic_name in PRACTICE_QUESTIONS:
            st.markdown("---")
            st.markdown("### 🎯 Practice Questions")
            st.info("💡 Test your understanding! Earn +5 XP for each correct answer.")
            
            questions = PRACTICE_QUESTIONS[topic_name]
            
            for idx, q in enumerate(questions):
                with st.expander(f"❓ Question {idx + 1}", expanded=False):
                    st.markdown(f"**{q['question']}**")
                    
                    answer_key = f"answer_{topic_name}_{idx}"
                    
                    user_answer = st.radio(
                        "Select your answer:",
                        q['options'],
                        key=answer_key,
                        index=None
                    )
                    
                    check_key = f"check_{topic_name}_{idx}"
                    answered_key = f"{topic_name}_{idx}"
                    
                    if st.button("✅ Check Answer", key=check_key):
                        if user_answer is None:
                            st.warning("⚠️ Please select an answer first!")
                        else:
                            selected_idx = q['options'].index(user_answer)
                            
                            if selected_idx == q['correct']:
                                st.success("✅ Correct! Excellent work!")
                                
                                # Add XP only once
                                if answered_key not in st.session_state.answered_questions:
                                    st.session_state.total_xp += 5
                                    st.session_state.answered_questions.append(answered_key)
                                    
                                    # Save to Data Manager
                                    if DATA_MANAGER_AVAILABLE:
                                        try:
                                            data = load_progress()
                                            if 'answered_questions' not in data:
                                                data['answered_questions'] = []
                                            if answered_key not in data['answered_questions']:
                                                data['answered_questions'].append(answered_key)
                                                data['achievements']['xp_total'] += 5
                                                save_progress(data)
                                        except:
                                            pass
                                    
                                    st.balloons()
                                    st.info("🎉 +5 XP earned!")
                                else:
                                    st.info("Already answered correctly! No additional XP.")
                            else:
                                correct_answer = q['options'][q['correct']]
                                st.error(f"❌ Not quite. The correct answer is: **{correct_answer}**")
                            
                            # Show solution
                            st.markdown("---")
                            st.markdown("**📝 Solution:**")
                            st.code(q['solution'], language="text")
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════
        # ACTION BUTTONS
        # ═══════════════════════════════════════════════════
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if topic_name not in st.session_state.completed_topics:
                # Find topic XP
                topic_xp = 25
                for t in topics:
                    if t['name'] == topic_name:
                        topic_xp = t.get('xp', 25)
                        break
                
                if st.button(f"✅ Mark Complete (+{topic_xp} XP)", use_container_width=True, type="primary"):
                    st.session_state.completed_topics.append(topic_name)
                    st.session_state.total_xp += topic_xp
                    
                    # Save to Data Manager
                    if DATA_MANAGER_AVAILABLE:
                        try:
                            data = load_progress()
                            
                            topic_entry = {
                                'topic': topic_name,
                                'module': mod_id,
                                'module_name': mod_data['name'],
                                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            if 'topics_completed' not in data['modules']:
                                data['modules']['topics_completed'] = []
                            
                            existing = [t['topic'] for t in data['modules']['topics_completed']]
                            if topic_name not in existing:
                                data['modules']['topics_completed'].append(topic_entry)
                                data['achievements']['xp_total'] += topic_xp
                            
                            # Study time
                            if st.session_state.current_topic_start:
                                study_minutes = (datetime.now() - st.session_state.current_topic_start).seconds // 60
                                study_minutes = max(1, min(study_minutes, 120))
                                data = record_study_time(data, study_minutes)
                            
                            # Update streak
                            data = update_streak(data)
                            
                            # Check module completion
                            mod_topics = [t["name"] for t in topics]
                            completed_in_mod = [t for t in mod_topics if t in st.session_state.completed_topics]
                            
                            if len(completed_in_mod) == len(mod_topics):
                                if mod_data['name'] not in data['modules'].get('completed', []):
                                    data = record_module_complete(data, mod_data['name'])
                                    st.success(f"🎉 Module {mod_id} Complete! +100 XP Bonus!")
                            
                            save_progress(data)
                            
                        except Exception as e:
                            pass
                    
                    st.success(f"✅ Completed! +{topic_xp} XP 🎉")
                    st.balloons()
                    st.rerun()
            else:
                st.success("✅ Already Completed!")
        
        with col2:
            is_bookmarked = topic_name in st.session_state.bookmarked_topics
            bm_text = "🔖 Unbookmark" if is_bookmarked else "📌 Bookmark"
            
            if st.button(bm_text, use_container_width=True):
                if is_bookmarked:
                    st.session_state.bookmarked_topics.remove(topic_name)
                    st.info("Bookmark removed!")
                else:
                    st.session_state.bookmarked_topics.append(topic_name)
                    st.success("Bookmarked for later!")
                st.rerun()
        
        with col3:
            if st.button("📝 Take Quiz", use_container_width=True):
                if os.path.exists("pages/02_❓_Quiz.py"):
                    st.switch_page("pages/02_❓_Quiz.py")
                else:
                    st.info("Quiz page coming soon!")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p style="margin: 0; font-size: 1.1rem;">
        📚 <strong>Elshamy IWCF Mastery Method™ 2026</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0;">
        Learn → Practice → Master → Pass! 🎓
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Created by Eng. Ahmed Elshamy | "Your Success is My Mission" 💪
    </p>
</div>
""", unsafe_allow_html=True)