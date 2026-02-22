import streamlit as st
import random
from datetime import datetime, timedelta
import json
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
        record_question_attempt,
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
    page_title="Quiz - Elshamy IWCF",
    page_icon="❓",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 التصميم المحسّن
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .quiz-header {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 50%, #B45309 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(245, 158, 11, 0.3);
    }
    
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #F59E0B;
    }
    
    .score-card {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
    }
    
    .correct-box {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border: 2px solid #10B981;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .wrong-box {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        border: 2px solid #EF4444;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .normal-box {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .normal-box:hover {
        background: #E5E7EB;
        transform: translateX(5px);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid #F59E0B;
    }
    
    .timer-box {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    .timer-warning {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: pulse 1s infinite;
    }
    
    .timer-danger {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: pulse 0.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .xp-badge {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    .level-badge {
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .difficulty-easy { background: #D1FAE5; color: #065F46; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; }
    .difficulty-medium { background: #FEF3C7; color: #92400E; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; }
    .difficulty-hard { background: #FEE2E2; color: #991B1B; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; }
    
    .leaderboard-item {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .module-filter {
        background: #F3F4F6;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .module-filter:hover {
        background: #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📚 MODULES DICTIONARY
# ═══════════════════════════════════════════════════════

MODULES = {
    1: "Module 1: Well Control Fundamentals",
    2: "Module 2: Pressure Calculations",
    3: "Module 3: Kick Detection & Analysis",
    4: "Module 4: Kill Methods",
    5: "Module 5: Well Control Equipment",
    6: "Module 6: Gas Behavior",
    7: "Module 7: Complications",
    8: "Module 8: Procedures & Regulations"
}

# ═══════════════════════════════════════════════════════
# 📚 بنك الأسئلة الكامل - 100 سؤال
# ═══════════════════════════════════════════════════════

QUESTIONS_BANK = [
    # ═══════════════════════════════════════════════════
    # MODULE 1: Well Control Fundamentals (15 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 1,
        "module": 1,
        "topic": "Hydrostatic Pressure",
        "difficulty": "Easy",
        "question": "What is the formula for hydrostatic pressure in oilfield units?",
        "options": [
            "HP = MW × TVD",
            "HP = 0.052 × MW × TVD",
            "HP = 0.052 × MW² × TVD",
            "HP = MW / TVD"
        ],
        "correct": 1,
        "explanation": """**Correct Answer: HP = 0.052 × MW × TVD**

Where:
• HP = Hydrostatic Pressure (psi)
• MW = Mud Weight (ppg)
• TVD = True Vertical Depth (ft)
• 0.052 = Conversion constant

**Why others are wrong:**
• Option A: Missing the 0.052 constant
• Option C: MW shouldn't be squared
• Option D: Division is wrong"""
    },
    {
        "id": 2,
        "module": 1,
        "topic": "Hydrostatic Pressure",
        "difficulty": "Medium",
        "question": "Calculate the hydrostatic pressure at 10,000 ft TVD with 12 ppg mud.",
        "options": ["5,200 psi", "6,240 psi", "7,200 psi", "120,000 psi"],
        "correct": 1,
        "explanation": """**Solution:**

HP = 0.052 × MW × TVD
HP = 0.052 × 12 × 10,000
HP = 6,240 psi ✓

**Step by step:**
1. Multiply 0.052 × 12 = 0.624
2. Multiply 0.624 × 10,000 = 6,240 psi"""
    },
    {
        "id": 3,
        "module": 1,
        "topic": "Hydrostatic Pressure",
        "difficulty": "Medium",
        "question": "What mud weight is needed to create 5,200 psi at 10,000 ft?",
        "options": ["8 ppg", "10 ppg", "12 ppg", "14 ppg"],
        "correct": 1,
        "explanation": """**Solution:**

MW = HP / (0.052 × TVD)
MW = 5,200 / (0.052 × 10,000)
MW = 5,200 / 520
MW = 10 ppg ✓

**Memory tip:** 10 ppg at 10,000 ft = 5,200 psi"""
    },
    {
        "id": 4,
        "module": 1,
        "topic": "Hydrostatic Pressure",
        "difficulty": "Hard",
        "question": "At what TVD will 11 ppg mud create 4,576 psi?",
        "options": ["6,000 ft", "7,000 ft", "8,000 ft", "9,000 ft"],
        "correct": 2,
        "explanation": """**Solution:**

TVD = HP / (0.052 × MW)
TVD = 4,576 / (0.052 × 11)
TVD = 4,576 / 0.572
TVD = 8,000 ft ✓

**Verification:** 0.052 × 11 × 8,000 = 4,576 psi ✓"""
    },
    {
        "id": 5,
        "module": 1,
        "topic": "Barriers",
        "difficulty": "Easy",
        "question": "What is the PRIMARY barrier in well control?",
        "options": ["BOP", "Mud Weight (Hydrostatic Pressure)", "Casing", "Cement"],
        "correct": 1,
        "explanation": """**Correct: Mud Weight (Hydrostatic Pressure)**

• **Primary barrier** = Mud column (hydrostatic pressure)
• **Secondary barrier** = BOP

The mud weight creates hydrostatic pressure that prevents formation fluids from entering.

**Memory tip:** Primary = Pressure = Mud"""
    },
    {
        "id": 6,
        "module": 1,
        "topic": "Barriers",
        "difficulty": "Easy",
        "question": "What is the SECONDARY barrier?",
        "options": ["Mud Weight", "Casing", "BOP System", "Cement"],
        "correct": 2,
        "explanation": """**Correct: BOP System**

The BOP is the secondary barrier used when the primary barrier (mud) fails.

**Memory tips:**
• **P**rimary = **P**ressure (mud)
• **S**econdary = **S**teel (BOP)"""
    },
    {
        "id": 7,
        "module": 1,
        "topic": "Barriers",
        "difficulty": "Medium",
        "question": "How many barriers should be in place at ALL times?",
        "options": ["One", "Two", "Three", "Four"],
        "correct": 1,
        "explanation": """**Correct: Two**

The well control principle requires **MINIMUM TWO barriers** at all times:
1. Primary barrier (mud)
2. Secondary barrier (BOP)

**Never operate with only one barrier!**"""
    },
    {
        "id": 8,
        "module": 1,
        "topic": "Basic Concepts",
        "difficulty": "Easy",
        "question": "What is a 'Kick'?",
        "options": ["Controlled flow of mud", "Uncontrolled influx of formation fluids", "Increase in pump pressure", "Loss of mud to formation"],
        "correct": 1,
        "explanation": """**Correct: Uncontrolled influx of formation fluids**

A kick occurs when:
• Formation pressure > Bottomhole pressure
• Formation fluids (gas, oil, water) enter the wellbore

**Causes:** Low MW, Swabbing, Lost circulation"""
    },
    {
        "id": 9,
        "module": 1,
        "topic": "Basic Concepts",
        "difficulty": "Easy",
        "question": "What is a 'Blowout'?",
        "options": ["Controlled kick", "Uncontrolled flow of formation fluids to surface", "Normal drilling operation", "Circulation of mud"],
        "correct": 1,
        "explanation": """**Correct: Uncontrolled flow of formation fluids to surface**

A blowout is a kick that was NOT controlled, resulting in:
• Uncontrolled flow to surface, OR
• Flow into another formation (underground blowout)

**Prevention:** Proper kick detection and shut-in"""
    },
    {
        "id": 10,
        "module": 1,
        "topic": "Pressure Concepts",
        "difficulty": "Medium",
        "question": "If HP > FP, the well is:",
        "options": ["Underbalanced", "Overbalanced", "Balanced", "In a kick situation"],
        "correct": 1,
        "explanation": """**Correct: Overbalanced**

• **Overbalanced:** HP > FP (Safe - no kick)
• **Underbalanced:** HP < FP (Kick risk!)
• **Balanced:** HP = FP (Risky - no margin)

Where: HP = Hydrostatic Pressure, FP = Formation Pressure"""
    },
    {
        "id": 11,
        "module": 1,
        "topic": "Hydrostatic Pressure",
        "difficulty": "Medium",
        "question": "Which depth is used for hydrostatic calculations?",
        "options": ["Measured Depth (MD)", "True Vertical Depth (TVD)", "Drilled Depth", "Total Depth"],
        "correct": 1,
        "explanation": """**Correct: True Vertical Depth (TVD)**

Hydrostatic pressure depends on the **vertical** fluid column only.

⚠️ **Common Exam Trap:**
Question gives MD = 12,000 ft, TVD = 10,000 ft
**Always use TVD (10,000 ft)!**"""
    },
    {
        "id": 12,
        "module": 1,
        "topic": "Pressure Gradients",
        "difficulty": "Medium",
        "question": "What is the pressure gradient of 10 ppg mud?",
        "options": ["0.433 psi/ft", "0.465 psi/ft", "0.520 psi/ft", "0.624 psi/ft"],
        "correct": 2,
        "explanation": """**Solution:**

Gradient = 0.052 × MW
Gradient = 0.052 × 10
Gradient = 0.520 psi/ft ✓

**Common gradients:**
• 0.433 = Fresh water (8.33 ppg)
• 0.465 = Normal formation
• 0.520 = 10 ppg mud"""
    },
    {
        "id": 13,
        "module": 1,
        "topic": "Pressure Gradients",
        "difficulty": "Easy",
        "question": "Normal formation pressure gradient is approximately:",
        "options": ["0.433 psi/ft", "0.465 psi/ft", "0.520 psi/ft", "0.600 psi/ft"],
        "correct": 1,
        "explanation": """**Correct: 0.465 psi/ft**

This equals approximately **8.94 ppg** mud weight.

• **Normal:** 0.465 psi/ft
• **Abnormal (high):** > 0.465 psi/ft
• **Subnormal (low):** < 0.465 psi/ft"""
    },
    {
        "id": 14,
        "module": 1,
        "topic": "Pressure Gradients",
        "difficulty": "Hard",
        "question": "A formation has a gradient of 0.572 psi/ft. What equivalent MW balances it?",
        "options": ["10 ppg", "11 ppg", "12 ppg", "13 ppg"],
        "correct": 1,
        "explanation": """**Solution:**

MW = Gradient / 0.052
MW = 0.572 / 0.052
MW = 11 ppg ✓

This is ABNORMAL pressure (> 0.465 psi/ft)"""
    },
    {
        "id": 15,
        "module": 1,
        "topic": "Hydrostatic Pressure",
        "difficulty": "Hard",
        "question": "Which creates MORE hydrostatic pressure?\nA) 10 ppg at 10,000 ft\nB) 12 ppg at 8,500 ft",
        "options": ["Option A (10 ppg at 10,000 ft)", "Option B (12 ppg at 8,500 ft)", "Both are equal", "Cannot be determined"],
        "correct": 1,
        "explanation": """**Solution:**

Option A: HP = 0.052 × 10 × 10,000 = 5,200 psi
Option B: HP = 0.052 × 12 × 8,500 = 5,304 psi

**Option B creates MORE pressure (5,304 > 5,200)** ✓"""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 2: Pressure Calculations (15 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 16,
        "module": 2,
        "topic": "Formation Pressure",
        "difficulty": "Medium",
        "question": "After shut-in: TVD = 10,000 ft, MW = 10 ppg, SIDPP = 200 psi. Calculate formation pressure.",
        "options": ["5,000 psi", "5,200 psi", "5,400 psi", "5,600 psi"],
        "correct": 2,
        "explanation": """**Solution:**

FP = HP + SIDPP
FP = (0.052 × MW × TVD) + SIDPP
FP = (0.052 × 10 × 10,000) + 200
FP = 5,200 + 200
FP = 5,400 psi ✓"""
    },
    {
        "id": 17,
        "module": 2,
        "topic": "Formation Pressure",
        "difficulty": "Hard",
        "question": "TVD = 12,000 ft, MW = 11 ppg, SIDPP = 350 psi. What is formation pressure?",
        "options": ["6,864 psi", "7,014 psi", "7,214 psi", "7,414 psi"],
        "correct": 2,
        "explanation": """**Solution:**

HP = 0.052 × 11 × 12,000 = 6,864 psi
FP = HP + SIDPP
FP = 6,864 + 350
FP = 7,214 psi ✓"""
    },
    {
        "id": 18,
        "module": 2,
        "topic": "Kill Mud Weight",
        "difficulty": "Medium",
        "question": "TVD = 10,000 ft, OMW = 10 ppg, SIDPP = 260 psi. Calculate Kill Mud Weight.",
        "options": ["10.3 ppg", "10.5 ppg", "10.7 ppg", "11.0 ppg"],
        "correct": 1,
        "explanation": """**Solution:**

KMW = OMW + (SIDPP / 0.052 / TVD)
KMW = 10 + (260 / 0.052 / 10,000)
KMW = 10 + (260 / 520)
KMW = 10 + 0.5
KMW = 10.5 ppg ✓"""
    },
    {
        "id": 19,
        "module": 2,
        "topic": "Kill Mud Weight",
        "difficulty": "Hard",
        "question": "SIDPP = 400 psi, OMW = 12 ppg, TVD = 10,000 ft. Calculate KMW.",
        "options": ["12.50 ppg", "12.77 ppg", "13.00 ppg", "13.25 ppg"],
        "correct": 1,
        "explanation": """**Solution:**

KMW = OMW + (SIDPP / 0.052 / TVD)
KMW = 12 + (400 / 0.052 / 10,000)
KMW = 12 + (400 / 520)
KMW = 12 + 0.769
KMW = 12.77 ppg ✓"""
    },
    {
        "id": 20,
        "module": 2,
        "topic": "ECD",
        "difficulty": "Medium",
        "question": "MW = 11 ppg, APL = 286 psi, TVD = 10,000 ft. Calculate ECD.",
        "options": ["11.25 ppg", "11.55 ppg", "11.75 ppg", "12.00 ppg"],
        "correct": 1,
        "explanation": """**Solution:**

ECD = MW + (APL / 0.052 / TVD)
ECD = 11 + (286 / 0.052 / 10,000)
ECD = 11 + (286 / 520)
ECD = 11 + 0.55
ECD = 11.55 ppg ✓

**ECD > MW always when circulating!**"""
    },
    {
        "id": 21,
        "module": 2,
        "topic": "ECD",
        "difficulty": "Easy",
        "question": "ECD is ALWAYS:",
        "options": ["Less than static MW", "Equal to static MW", "Greater than static MW when circulating", "Zero when circulating"],
        "correct": 2,
        "explanation": """**Correct: Greater than static MW when circulating**

ECD = MW + (APL / 0.052 / TVD)

• **ECD > MW** (when pumping - friction adds pressure)
• **ECD = MW** (when pumps OFF)"""
    },
    {
        "id": 22,
        "module": 2,
        "topic": "MAASP",
        "difficulty": "Hard",
        "question": "LOT EMW = 15 ppg, Current MW = 12 ppg, Shoe TVD = 5,000 ft. Calculate MAASP.",
        "options": ["680 psi", "780 psi", "880 psi", "980 psi"],
        "correct": 1,
        "explanation": """**Solution:**

MAASP = (LOT - MW) × 0.052 × Shoe TVD
MAASP = (15 - 12) × 0.052 × 5,000
MAASP = 3 × 0.052 × 5,000
MAASP = 780 psi ✓

**Never exceed MAASP!**"""
    },
    {
        "id": 23,
        "module": 2,
        "topic": "MAASP",
        "difficulty": "Medium",
        "question": "If you INCREASE mud weight, MAASP will:",
        "options": ["Increase", "Decrease", "Stay the same", "Double"],
        "correct": 1,
        "explanation": """**Correct: Decrease**

MAASP = (LOT - MW) × 0.052 × Shoe TVD

As MW ↑ → (LOT - MW) ↓ → MAASP ↓

**Higher MW = Lower MAASP = Less margin**"""
    },
    {
        "id": 24,
        "module": 2,
        "topic": "BHP",
        "difficulty": "Medium",
        "question": "MW = 10 ppg, TVD = 10,000 ft, APL = 260 psi. Calculate BHP while circulating.",
        "options": ["5,200 psi", "5,460 psi", "5,720 psi", "6,000 psi"],
        "correct": 1,
        "explanation": """**Solution:**

BHP (circulating) = HP + APL
BHP = (0.052 × 10 × 10,000) + 260
BHP = 5,200 + 260
BHP = 5,460 psi ✓"""
    },
    {
        "id": 25,
        "module": 2,
        "topic": "BHP",
        "difficulty": "Easy",
        "question": "Which gives HIGHER BHP?",
        "options": ["Pumps OFF (static)", "Pumps ON (circulating)", "Both equal", "Cannot determine"],
        "correct": 1,
        "explanation": """**Correct: Pumps ON (circulating)**

• Static BHP = HP only
• Dynamic BHP = HP + APL

Since APL > 0: **Dynamic BHP > Static BHP**"""
    },
    {
        "id": 26,
        "module": 2,
        "topic": "ICP & FCP",
        "difficulty": "Medium",
        "question": "SIDPP = 400 psi, SCR = 500 psi. Calculate ICP.",
        "options": ["800 psi", "900 psi", "1,000 psi", "1,100 psi"],
        "correct": 1,
        "explanation": """**Solution:**

ICP = SIDPP + SCR
ICP = 400 + 500
ICP = 900 psi ✓

ICP = Initial Circulating Pressure"""
    },
    {
        "id": 27,
        "module": 2,
        "topic": "ICP & FCP",
        "difficulty": "Hard",
        "question": "SCR = 500 psi, KMW = 11 ppg, OMW = 10 ppg. Calculate FCP.",
        "options": ["500 psi", "525 psi", "550 psi", "575 psi"],
        "correct": 2,
        "explanation": """**Solution:**

FCP = SCR × (KMW / OMW)
FCP = 500 × (11 / 10)
FCP = 500 × 1.1
FCP = 550 psi ✓

FCP reached when kill mud at bit."""
    },
    {
        "id": 28,
        "module": 2,
        "topic": "Kill Sheet",
        "difficulty": "Hard",
        "question": "ICP = 800 psi, FCP = 600 psi, Strokes to bit = 1000. Pressure after 500 strokes?",
        "options": ["650 psi", "700 psi", "750 psi", "800 psi"],
        "correct": 1,
        "explanation": """**Solution:**

P = ICP - [(ICP - FCP) × (Strokes / Total)]
P = 800 - [(800 - 600) × (500 / 1000)]
P = 800 - [200 × 0.5]
P = 800 - 100
P = 700 psi ✓"""
    },
    {
        "id": 29,
        "module": 2,
        "topic": "Pressure",
        "difficulty": "Medium",
        "question": "SIDPP reads formation pressure directly because:",
        "options": ["It's higher than SICP", "Drill pipe is full of known mud weight to formation", "It measures surface pressure only", "It includes kick gradient"],
        "correct": 1,
        "explanation": """**Correct: Drill pipe is full of known mud weight to formation**

The drill pipe provides direct hydraulic connection to bottom with known MW.

FP = HP + SIDPP"""
    },
    {
        "id": 30,
        "module": 2,
        "topic": "Pressure",
        "difficulty": "Easy",
        "question": "Which pressure is used to calculate formation pressure?",
        "options": ["SICP", "SIDPP", "Pump pressure", "Casing pressure"],
        "correct": 1,
        "explanation": """**Correct: SIDPP**

Formula: FP = HP + SIDPP

⚠️ **Never use SICP** - it's affected by kick gradient."""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 3: Kick Detection (15 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 31,
        "module": 3,
        "topic": "Primary Indicators",
        "difficulty": "Easy",
        "question": "What is the MOST reliable kick indicator?",
        "options": ["Drilling break", "Pit gain", "Connection gas", "Pump pressure change"],
        "correct": 1,
        "explanation": """**Correct: Pit gain**

Pit gain is most reliable - directly shows fluid entered wellbore.

**Reliability ranking:**
1. 🥇 Pit gain
2. 🥈 Flow rate increase
3. 🥉 Pump pressure drop"""
    },
    {
        "id": 32,
        "module": 3,
        "topic": "Primary Indicators",
        "difficulty": "Easy",
        "question": "All are PRIMARY kick indicators EXCEPT:",
        "options": ["Pit gain", "Flow rate increase", "Drilling break", "Pump pressure decrease"],
        "correct": 2,
        "explanation": """**Correct: Drilling break**

Drilling break is **SECONDARY** indicator.

**PRIMARY:** Pit gain, Flow increase, Pump P drop
**SECONDARY:** Drilling break, Connection gas, Cut mud"""
    },
    {
        "id": 33,
        "module": 3,
        "topic": "Primary Indicators",
        "difficulty": "Medium",
        "question": "A sudden 10 bbl pit gain indicates:",
        "options": ["Normal operation", "Possible kick - monitor", "Definite kick - shut in immediately", "Equipment malfunction"],
        "correct": 2,
        "explanation": """**Correct: Definite kick - shut in immediately**

Any sudden pit gain = Definite kick = IMMEDIATE shut-in!

**Action:** Stop pumps → Raise kelly → Close BOP → Record"""
    },
    {
        "id": 34,
        "module": 3,
        "topic": "Secondary Indicators",
        "difficulty": "Easy",
        "question": "Drilling break is a:",
        "options": ["Primary kick indicator", "Secondary kick indicator", "Not a kick indicator", "Equipment alarm"],
        "correct": 1,
        "explanation": """**Correct: Secondary kick indicator**

Drilling break = Sudden ROP increase
**Action:** Monitor closely, flow check if suspicious"""
    },
    {
        "id": 35,
        "module": 3,
        "topic": "Kick Analysis",
        "difficulty": "Medium",
        "question": "SICP = 700 psi, SIDPP = 400 psi. The kick is most likely:",
        "options": ["Water", "Oil", "Gas", "Mud"],
        "correct": 2,
        "explanation": """**Correct: Gas**

SICP >> SIDPP = Light fluid = **GAS kick**

• SICP > SIDPP (big diff) → Gas
• SICP ≈ SIDPP (small diff) → Liquid"""
    },
    {
        "id": 36,
        "module": 3,
        "topic": "Kick Analysis",
        "difficulty": "Medium",
        "question": "If SICP ≈ SIDPP after shut-in, the kick is probably:",
        "options": ["Gas", "Liquid (water or oil)", "Air", "Cannot determine"],
        "correct": 1,
        "explanation": """**Correct: Liquid (water or oil)**

SICP ≈ SIDPP = Similar density to mud = **Liquid kick**"""
    },
    {
        "id": 37,
        "module": 3,
        "topic": "Shut-in",
        "difficulty": "Easy",
        "question": "FIRST action when a kick is detected:",
        "options": ["Close BOP", "Stop pumps", "Notify supervisor", "Increase mud weight"],
        "correct": 1,
        "explanation": """**Correct: Stop pumps**

**S-R-C-R sequence:**
1. **S**top pumps ← FIRST!
2. **R**aise kelly
3. **C**lose BOP
4. **R**ecord pressures"""
    },
    {
        "id": 38,
        "module": 3,
        "topic": "Shut-in",
        "difficulty": "Medium",
        "question": "Hard shut-in procedure means:",
        "options": ["Slow BOP closure", "Close BOP first, then open choke line", "Open choke first, then close BOP", "High pressure shut-in"],
        "correct": 1,
        "explanation": """**Correct: Close BOP first, then open choke line**

**Hard:** Close BOP → Open choke (standard, faster)
**Soft:** Open choke → Close BOP → Close choke"""
    },
    {
        "id": 39,
        "module": 3,
        "topic": "Shut-in",
        "difficulty": "Easy",
        "question": "Target time for complete shut-in from kick detection:",
        "options": ["Less than 5 minutes", "Less than 2 minutes", "Less than 10 minutes", "Time doesn't matter"],
        "correct": 1,
        "explanation": """**Correct: Less than 2 minutes**

Fast shut-in = Less influx = Easier kill!

**Every minute delay = More kick volume!**"""
    },
    {
        "id": 40,
        "module": 3,
        "topic": "Kick Detection",
        "difficulty": "Medium",
        "question": "Flow check should be performed when:",
        "options": ["Never during drilling", "Every hour routinely", "When any suspicious indicator is observed", "Only after shut-in"],
        "correct": 2,
        "explanation": """**Correct: When any suspicious indicator is observed**

Flow check when: Drilling break, Connection gas, Any suspicious sign

**If well flows = Shut in immediately!**"""
    },
    {
        "id": 41,
        "module": 3,
        "topic": "SIDPP/SICP",
        "difficulty": "Medium",
        "question": "SIDPP is used to calculate all EXCEPT:",
        "options": ["Formation pressure", "Kill mud weight", "Kick fluid gradient", "Initial circulating pressure"],
        "correct": 2,
        "explanation": """**Correct: Kick fluid gradient**

Kick gradient needs BOTH pressures:
Gradient = (SICP - SIDPP) / Kick Height

**SIDPP alone:** FP, KMW, ICP"""
    },
    {
        "id": 42,
        "module": 3,
        "topic": "Kick Detection",
        "difficulty": "Easy",
        "question": "Pit volume should be monitored with accuracy of:",
        "options": ["± 10 bbls", "± 5 bbls", "± 1 bbl", "Not important"],
        "correct": 2,
        "explanation": """**Correct: ± 1 bbl**

Accurate monitoring = Early detection = Smaller kick!"""
    },
    {
        "id": 43,
        "module": 3,
        "topic": "Kick Causes",
        "difficulty": "Medium",
        "question": "Which does NOT cause a kick?",
        "options": ["Insufficient mud weight", "Swabbing while tripping", "High pump rate", "Lost circulation"],
        "correct": 2,
        "explanation": """**Correct: High pump rate**

High pump rate increases ECD = HELPS prevent kicks!

**Kick causes:** Low MW, Swabbing, Lost circulation"""
    },
    {
        "id": 44,
        "module": 3,
        "topic": "Kick Causes",
        "difficulty": "Easy",
        "question": "Swabbing can cause a kick because it:",
        "options": ["Increases BHP", "Reduces BHP temporarily", "Increases mud weight", "Seals the formation"],
        "correct": 1,
        "explanation": """**Correct: Reduces BHP temporarily**

Swabbing = Suction effect = BHP drops

If BHP < FP = **KICK!**"""
    },
    {
        "id": 45,
        "module": 3,
        "topic": "Kick Detection",
        "difficulty": "Easy",
        "question": "Connection gas indicates:",
        "options": ["Definite kick", "Possible kick - warning sign", "Normal drilling", "Equipment problem"],
        "correct": 1,
        "explanation": """**Correct: Possible kick - warning sign**

Connection gas = Secondary indicator = Warning that FP ≈ HP

**Action:** Monitor, consider increasing MW"""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 4: Kill Methods (15 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 46,
        "module": 4,
        "topic": "Driller's Method",
        "difficulty": "Easy",
        "question": "Driller's Method requires how many circulations?",
        "options": ["One", "Two", "Three", "Depends on kick size"],
        "correct": 1,
        "explanation": """**Correct: Two**

**Driller's Method = 2 Circulations:**
1. Remove kick (original mud)
2. Kill well (kill mud)"""
    },
    {
        "id": 47,
        "module": 4,
        "topic": "Wait & Weight",
        "difficulty": "Easy",
        "question": "Wait and Weight Method requires how many circulations?",
        "options": ["One", "Two", "Three", "Four"],
        "correct": 0,
        "explanation": """**Correct: One**

**Wait & Weight = 1 Circulation:**
Remove kick AND kill well simultaneously with kill mud."""
    },
    {
        "id": 48,
        "module": 4,
        "topic": "Driller's Method",
        "difficulty": "Medium",
        "question": "During Driller's Method first circulation, you maintain:",
        "options": ["Constant casing pressure", "Constant drillpipe pressure (ICP)", "Constant pump rate", "Constant mud weight"],
        "correct": 1,
        "explanation": """**Correct: Constant drillpipe pressure (ICP)**

First circulation: Hold ICP constant = Maintains constant BHP"""
    },
    {
        "id": 49,
        "module": 4,
        "topic": "Wait & Weight",
        "difficulty": "Medium",
        "question": "During Wait & Weight, drillpipe pressure should:",
        "options": ["Stay at ICP throughout", "Decrease from ICP to FCP as kill mud fills drillstring", "Increase throughout", "Stay at FCP throughout"],
        "correct": 1,
        "explanation": """**Correct: Decrease from ICP to FCP**

Pressure schedule: ICP → FCP linearly as kill mud fills drillstring"""
    },
    {
        "id": 50,
        "module": 4,
        "topic": "Volumetric",
        "difficulty": "Medium",
        "question": "Volumetric Method is used when:",
        "options": ["Kick is too large", "Mud weight is too high", "Circulation is NOT possible", "Gas kick only"],
        "correct": 2,
        "explanation": """**Correct: Circulation is NOT possible**

Use Volumetric when: Stuck pipe, No pumps, Plugged string"""
    },
    {
        "id": 51,
        "module": 4,
        "topic": "Volumetric",
        "difficulty": "Medium",
        "question": "In Volumetric Method, as gas migrates up you:",
        "options": ["Pump mud in", "Close choke tighter", "Bleed mud to reduce pressure", "Wait without action"],
        "correct": 2,
        "explanation": """**Correct: Bleed mud to reduce pressure**

Gas rises → Pressure up → Bleed mud to maintain BHP"""
    },
    {
        "id": 52,
        "module": 4,
        "topic": "Bullheading",
        "difficulty": "Easy",
        "question": "Bullheading pushes the kick:",
        "options": ["To surface", "Back into formation", "Into casing", "Through choke"],
        "correct": 1,
        "explanation": """**Correct: Back into formation**

Bullheading = Force kick back into formation (used for H2S)"""
    },
    {
        "id": 53,
        "module": 4,
        "topic": "Bullheading",
        "difficulty": "Medium",
        "question": "Bullheading is preferred for:",
        "options": ["Normal gas kick", "H2S kick", "Small water kick", "All kicks"],
        "correct": 1,
        "explanation": """**Correct: H2S kick**

H2S is deadly - bullhead to keep it underground!"""
    },
    {
        "id": 54,
        "module": 4,
        "topic": "Kill Calculations",
        "difficulty": "Hard",
        "question": "SIDPP = 300 psi, SCR = 400 psi, OMW = 10 ppg, TVD = 10,000 ft. Calculate KMW.",
        "options": ["10.38 ppg", "10.58 ppg", "10.78 ppg", "10.98 ppg"],
        "correct": 1,
        "explanation": """**Solution:**

KMW = OMW + (SIDPP / 0.052 / TVD)
KMW = 10 + (300 / 520)
KMW = 10 + 0.577
KMW = 10.58 ppg ✓"""
    },
    {
        "id": 55,
        "module": 4,
        "topic": "Kill Calculations",
        "difficulty": "Medium",
        "question": "SIDPP = 350 psi, SCR = 500 psi. Calculate ICP.",
        "options": ["750 psi", "800 psi", "850 psi", "900 psi"],
        "correct": 2,
        "explanation": """**Solution:**

ICP = SIDPP + SCR
ICP = 350 + 500
ICP = 850 psi ✓"""
    },
    {
        "id": 56,
        "module": 4,
        "topic": "Kill Calculations",
        "difficulty": "Hard",
        "question": "SCR = 450 psi, KMW = 12 ppg, OMW = 11 ppg. Calculate FCP.",
        "options": ["450 psi", "470 psi", "491 psi", "510 psi"],
        "correct": 2,
        "explanation": """**Solution:**

FCP = SCR × (KMW / OMW)
FCP = 450 × (12 / 11)
FCP = 450 × 1.0909
FCP = 491 psi ✓"""
    },
    {
        "id": 57,
        "module": 4,
        "topic": "Kill Methods",
        "difficulty": "Medium",
        "question": "Which method gives LOWER maximum casing pressure?",
        "options": ["Driller's Method", "Wait and Weight Method", "Both equal", "Volumetric Method"],
        "correct": 1,
        "explanation": """**Correct: Wait and Weight Method**

W&W = Lower casing pressure = Better for weak formations"""
    },
    {
        "id": 58,
        "module": 4,
        "topic": "Kill Methods",
        "difficulty": "Medium",
        "question": "Which method can start IMMEDIATELY without waiting?",
        "options": ["Wait and Weight only", "Driller's Method only", "Both can start immediately", "Neither"],
        "correct": 1,
        "explanation": """**Correct: Driller's Method only**

Driller's = Uses existing mud, no waiting
W&W = Must prepare kill mud first"""
    },
    {
        "id": 59,
        "module": 4,
        "topic": "Kill Methods",
        "difficulty": "Easy",
        "question": "During kill operation, BHP should be maintained:",
        "options": ["Below formation pressure", "Equal to formation pressure", "Slightly above formation pressure", "As high as possible"],
        "correct": 2,
        "explanation": """**Correct: Slightly above formation pressure**

BHP > FP (prevent influx) but not too high (avoid breakdown)"""
    },
    {
        "id": 60,
        "module": 4,
        "topic": "Kill Methods",
        "difficulty": "Hard",
        "question": "If casing pressure exceeds MAASP during kill, you should:",
        "options": ["Continue pumping faster", "Reduce pump rate and/or consider alternative methods", "Ignore and continue", "Increase mud weight more"],
        "correct": 1,
        "explanation": """**Correct: Reduce rate/consider alternatives**

Exceeding MAASP = Fracture risk! May need to bullhead."""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 5: BOP Equipment (10 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 61,
        "module": 5,
        "topic": "BOP",
        "difficulty": "Easy",
        "question": "Annular preventer can seal around:",
        "options": ["Drill pipe only", "Specific size only", "Any shape or size including open hole", "Open hole only"],
        "correct": 2,
        "explanation": """**Correct: Any shape or size including open hole**

Annular = Flexible rubber = Seals ANY shape

**Memory: Annular = Any**"""
    },
    {
        "id": 62,
        "module": 5,
        "topic": "BOP",
        "difficulty": "Easy",
        "question": "Which BOP element can CUT the drill pipe?",
        "options": ["Annular preventer", "Pipe rams", "Blind rams", "Shear rams"],
        "correct": 3,
        "explanation": """**Correct: Shear rams**

Shear rams = Cut pipe + seal

**LAST RESORT only!**"""
    },
    {
        "id": 63,
        "module": 5,
        "topic": "BOP",
        "difficulty": "Easy",
        "question": "Blind rams seal:",
        "options": ["Around drill pipe", "Open hole (no pipe present)", "Any size pipe", "Kelly only"],
        "correct": 1,
        "explanation": """**Correct: Open hole (no pipe present)**

Blind rams = NO pipe in BOP"""
    },
    {
        "id": 64,
        "module": 5,
        "topic": "BOP",
        "difficulty": "Medium",
        "question": "Pipe rams seal around:",
        "options": ["Any pipe size", "Specific pipe OD only", "Open hole", "Square kelly"],
        "correct": 1,
        "explanation": """**Correct: Specific pipe OD only**

Pipe rams = Size-specific (e.g., 5" rams for 5" pipe)

Variable Bore Rams (VBR) seal a range."""
    },
    {
        "id": 65,
        "module": 5,
        "topic": "Accumulator",
        "difficulty": "Medium",
        "question": "Accumulator bottles are pre-charged with:",
        "options": ["Air", "Nitrogen", "Hydraulic fluid", "Oxygen"],
        "correct": 1,
        "explanation": """**Correct: Nitrogen**

N₂ = Inert + Non-flammable + Compressible

NOT Oxygen (explosive risk!)"""
    },
    {
        "id": 66,
        "module": 5,
        "topic": "Accumulator",
        "difficulty": "Medium",
        "question": "After closing ALL BOPs, minimum remaining accumulator pressure should be:",
        "options": ["0 psi", "100 psi", "200 psi above precharge", "500 psi"],
        "correct": 2,
        "explanation": """**Correct: 200 psi above precharge**

Must have 200 psi reserve for emergency operations."""
    },
    {
        "id": 67,
        "module": 5,
        "topic": "Choke",
        "difficulty": "Easy",
        "question": "Opening the choke will:",
        "options": ["Increase backpressure", "Decrease backpressure", "Have no effect", "Close the well"],
        "correct": 1,
        "explanation": """**Correct: Decrease backpressure**

Open choke = Less restriction = Less pressure"""
    },
    {
        "id": 68,
        "module": 5,
        "topic": "Choke",
        "difficulty": "Medium",
        "question": "During well kill, choke is adjusted to maintain:",
        "options": ["Maximum pressure", "Minimum pressure", "Constant bottomhole pressure", "Zero pressure"],
        "correct": 2,
        "explanation": """**Correct: Constant bottomhole pressure**

Choke adjusts to keep BHP constant (slightly > FP)"""
    },
    {
        "id": 69,
        "module": 5,
        "topic": "BOP",
        "difficulty": "Medium",
        "question": "Stripping pipe through closed BOP requires using:",
        "options": ["Blind rams", "Shear rams", "Annular preventer", "Pipe rams only"],
        "correct": 2,
        "explanation": """**Correct: Annular preventer**

Annular's flexible element allows pipe movement while sealing."""
    },
    {
        "id": 70,
        "module": 5,
        "topic": "BOP",
        "difficulty": "Hard",
        "question": "Before closing pipe rams, you should always:",
        "options": ["Increase pump rate", "Space out to position pipe body (not tool joint) across rams", "Open choke fully", "Record pressures"],
        "correct": 1,
        "explanation": """**Correct: Space out (pipe body across rams)**

Tool joints are larger - may prevent proper seal."""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 6: Gas Behavior (10 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 71,
        "module": 6,
        "topic": "Boyle's Law",
        "difficulty": "Easy",
        "question": "As gas rises in the well, it:",
        "options": ["Compresses", "Expands", "Stays same volume", "Disappears"],
        "correct": 1,
        "explanation": """**Correct: Expands**

P₁V₁ = P₂V₂

Lower pressure = Higher volume = EXPANDS"""
    },
    {
        "id": 72,
        "module": 6,
        "topic": "Boyle's Law",
        "difficulty": "Medium",
        "question": "Gas volume = 5 bbls at 5,000 psi. Volume at 500 psi?",
        "options": ["10 bbls", "25 bbls", "50 bbls", "100 bbls"],
        "correct": 2,
        "explanation": """**Solution:**

V₂ = P₁ × V₁ / P₂
V₂ = 5,000 × 5 / 500
V₂ = 50 bbls ✓

10× pressure drop = 10× volume!"""
    },
    {
        "id": 73,
        "module": 6,
        "topic": "Boyle's Law",
        "difficulty": "Hard",
        "question": "10 bbls gas at 6,000 psi expands to what volume at 600 psi?",
        "options": ["50 bbls", "100 bbls", "150 bbls", "200 bbls"],
        "correct": 1,
        "explanation": """**Solution:**

V₂ = 6,000 × 10 / 600
V₂ = 100 bbls ✓"""
    },
    {
        "id": 74,
        "module": 6,
        "topic": "Gas Migration",
        "difficulty": "Easy",
        "question": "Typical gas migration rate in mud is approximately:",
        "options": ["100 ft/hour", "500 ft/hour", "1,000 ft/hour", "5,000 ft/hour"],
        "correct": 2,
        "explanation": """**Correct: 1,000 ft/hour**

10,000 ft well ≈ 10 hours for gas to reach surface"""
    },
    {
        "id": 75,
        "module": 6,
        "topic": "Gas Migration",
        "difficulty": "Medium",
        "question": "How long for gas to reach surface from 8,000 ft (assuming 1000 ft/hr)?",
        "options": ["4 hours", "6 hours", "8 hours", "10 hours"],
        "correct": 2,
        "explanation": """**Solution:**

Time = Depth / Rate
Time = 8,000 / 1,000
Time = 8 hours ✓"""
    },
    {
        "id": 76,
        "module": 6,
        "topic": "Gas Migration",
        "difficulty": "Medium",
        "question": "During shut-in, if gas migrates WITHOUT bleeding mud:",
        "options": ["Pressure stays constant", "Surface pressure increases", "Surface pressure decreases", "No effect"],
        "correct": 1,
        "explanation": """**Correct: Surface pressure increases**

Gas migration → Pressure rises → Could exceed MAASP!"""
    },
    {
        "id": 77,
        "module": 6,
        "topic": "Gas Expansion",
        "difficulty": "Medium",
        "question": "Most RAPID gas expansion occurs:",
        "options": ["At the bottom", "In the middle", "Near the surface", "Equal throughout"],
        "correct": 2,
        "explanation": """**Correct: Near the surface**

Near surface = Biggest pressure change per foot = Most expansion

**Critical zone = Last 2,000 ft!**"""
    },
    {
        "id": 78,
        "module": 6,
        "topic": "Gas Behavior",
        "difficulty": "Hard",
        "question": "Why is gas kick more dangerous than liquid kick?",
        "options": ["Gas is heavier", "Gas expands as it rises", "Gas is easier to detect", "Gas doesn't migrate"],
        "correct": 1,
        "explanation": """**Correct: Gas expands as it rises**

Small gas kick → MASSIVE at surface (Boyle's Law)"""
    },
    {
        "id": 79,
        "module": 6,
        "topic": "Boyle's Law",
        "difficulty": "Easy",
        "question": "Boyle's Law states that at constant temperature:",
        "options": ["Pressure × Volume = Constant", "Pressure / Volume = Constant", "Pressure + Volume = Constant", "Pressure = Volume"],
        "correct": 0,
        "explanation": """**Correct: Pressure × Volume = Constant**

P₁V₁ = P₂V₂"""
    },
    {
        "id": 80,
        "module": 6,
        "topic": "Stripping",
        "difficulty": "Medium",
        "question": "Stripping differs from snubbing because in stripping:",
        "options": ["Pipe is pushed out by pressure", "Pipe wants to fall (weight > well force)", "No BOP is used", "Faster operation"],
        "correct": 1,
        "explanation": """**Correct: Pipe wants to fall (heavy)**

Stripping: Pipe weight > Well force (sinks)
Snubbing: Well force > Pipe weight (pushes out)"""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 7: Complications (10 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 81,
        "module": 7,
        "topic": "Lost Circulation",
        "difficulty": "Easy",
        "question": "Lost circulation increases risk of:",
        "options": ["Equipment damage only", "Stuck pipe only", "Kick", "Nothing serious"],
        "correct": 2,
        "explanation": """**Correct: Kick**

Lost mud = Lost HP = Possible KICK!"""
    },
    {
        "id": 82,
        "module": 7,
        "topic": "Lost Circulation",
        "difficulty": "Medium",
        "question": "If losses occur DURING well kill, you should:",
        "options": ["Shut in immediately", "Increase pump rate", "Continue at reduced rate", "Stop all operations"],
        "correct": 2,
        "explanation": """**Correct: Continue at reduced rate**

Reduce rate (lower ECD), maintain BHP. Don't stop!"""
    },
    {
        "id": 83,
        "module": 7,
        "topic": "Underground Blowout",
        "difficulty": "Medium",
        "question": "Underground blowout is flow:",
        "options": ["To surface", "From one zone to another underground", "Into drill pipe", "Through casing"],
        "correct": 1,
        "explanation": """**Correct: From one zone to another underground**

Very difficult to control!"""
    },
    {
        "id": 84,
        "module": 7,
        "topic": "Underground Blowout",
        "difficulty": "Hard",
        "question": "Signs of underground blowout include:",
        "options": ["Large pit gain", "Dropping SIDPP with stable or decreasing pit", "Normal circulation returns", "Increasing pump pressure"],
        "correct": 1,
        "explanation": """**Correct: Dropping SIDPP with stable pit**

SIDPP drops + Pit stable = Pressure escaping underground!"""
    },
    {
        "id": 85,
        "module": 7,
        "topic": "Underground Blowout",
        "difficulty": "Medium",
        "question": "Main cause of underground blowout during kill:",
        "options": ["Low pump rate", "Exceeding MAASP / fracture pressure", "Light mud weight", "Slow response"],
        "correct": 1,
        "explanation": """**Correct: Exceeding MAASP**

Excessive pressure fractures weak zone at shoe!"""
    },
    {
        "id": 86,
        "module": 7,
        "topic": "Stuck Pipe",
        "difficulty": "Easy",
        "question": "If pipe becomes stuck during kill operation, priority is:",
        "options": ["Free the pipe first", "Maintain well control", "Pull hard", "Increase pump rate"],
        "correct": 1,
        "explanation": """**Correct: Maintain well control**

**WELL CONTROL ALWAYS FIRST!**

Use volumetric if no circulation."""
    },
    {
        "id": 87,
        "module": 7,
        "topic": "Stuck Pipe",
        "difficulty": "Medium",
        "question": "With stuck pipe and NO circulation possible, use:",
        "options": ["Driller's Method", "Wait and Weight", "Volumetric Method", "Bullheading"],
        "correct": 2,
        "explanation": """**Correct: Volumetric Method**

Volumetric = No pumping required!"""
    },
    {
        "id": 88,
        "module": 7,
        "topic": "H2S",
        "difficulty": "Easy",
        "question": "H2S at 100 ppm concentration will:",
        "options": ["Have strong rotten egg smell", "Paralyze sense of smell (olfactory fatigue)", "Have no effect", "Cause mild headache only"],
        "correct": 1,
        "explanation": """**Correct: Paralyze sense of smell**

100 ppm = NO smell detection!

**You can't smell the danger!**"""
    },
    {
        "id": 89,
        "module": 7,
        "topic": "H2S",
        "difficulty": "Easy",
        "question": "Preferred kill method for H2S kick:",
        "options": ["Driller's Method", "Wait and Weight", "Bullheading", "Volumetric"],
        "correct": 2,
        "explanation": """**Correct: Bullheading**

H2S is deadly - DON'T bring to surface!"""
    },
    {
        "id": 90,
        "module": 7,
        "topic": "H2S",
        "difficulty": "Medium",
        "question": "IDLH (Immediately Dangerous to Life or Health) for H2S is:",
        "options": ["10 ppm", "50 ppm", "100 ppm", "500 ppm"],
        "correct": 2,
        "explanation": """**Correct: 100 ppm**

At 100 ppm: Can't smell + Life threatening"""
    },
    
    # ═══════════════════════════════════════════════════
    # MODULE 8: Procedures & Regulations (10 questions)
    # ═══════════════════════════════════════════════════
    {
        "id": 91,
        "module": 8,
        "topic": "IWCF",
        "difficulty": "Easy",
        "question": "IWCF certificate is valid for:",
        "options": ["1 year", "2 years", "5 years", "Lifetime"],
        "correct": 1,
        "explanation": """**Correct: 2 years**

Must recertify before expiry."""
    },
    {
        "id": 92,
        "module": 8,
        "topic": "IWCF",
        "difficulty": "Easy",
        "question": "IWCF exam pass mark is:",
        "options": ["50%", "60%", "70%", "80%"],
        "correct": 2,
        "explanation": """**Correct: 70%**

35 out of 50 questions to pass."""
    },
    {
        "id": 93,
        "module": 8,
        "topic": "Safety",
        "difficulty": "Easy",
        "question": "FIRST action when kick is detected:",
        "options": ["Call supervisor", "Check instruments", "Stop pumps", "Close BOP"],
        "correct": 2,
        "explanation": """**Correct: Stop pumps**

S-R-C-R: STOP pumps first!"""
    },
    {
        "id": 94,
        "module": 8,
        "topic": "Barriers",
        "difficulty": "Easy",
        "question": "Primary barrier in a drilling well is:",
        "options": ["BOP", "Casing", "Mud column (hydrostatic pressure)", "Cement"],
        "correct": 2,
        "explanation": """**Correct: Mud column**

Primary = Mud, Secondary = BOP"""
    },
    {
        "id": 95,
        "module": 8,
        "topic": "Safety",
        "difficulty": "Medium",
        "question": "Well control drills should be conducted:",
        "options": ["Annually", "Monthly", "Weekly / Regularly", "Company discretion only"],
        "correct": 2,
        "explanation": """**Correct: Weekly / Regularly**

Regular drills = Prepared crew!"""
    },
    {
        "id": 96,
        "module": 8,
        "topic": "IWCF",
        "difficulty": "Easy",
        "question": "IWCF stands for:",
        "options": ["International Water Control Forum", "International Well Control Forum", "Internal Well Control Function", "International Wellbore Control"],
        "correct": 1,
        "explanation": """**Correct: International Well Control Forum**"""
    },
    {
        "id": 97,
        "module": 8,
        "topic": "Barriers",
        "difficulty": "Medium",
        "question": "Well control barriers must be:",
        "options": ["Assumed working", "Installed only", "Tested and verified", "Optional"],
        "correct": 2,
        "explanation": """**Correct: Tested and verified**

Never assume! Always test!"""
    },
    {
        "id": 98,
        "module": 8,
        "topic": "Safety",
        "difficulty": "Medium",
        "question": "Target shut-in time from kick detection:",
        "options": ["Less than 5 minutes", "Less than 2 minutes", "Less than 10 minutes", "No target"],
        "correct": 1,
        "explanation": """**Correct: Less than 2 minutes**

Fast shut-in = Less influx!"""
    },
    {
        "id": 99,
        "module": 8,
        "topic": "Safety",
        "difficulty": "Easy",
        "question": "The driller is responsible for:",
        "options": ["Drilling only", "Well control only", "Overall well control on the rig floor", "Paperwork only"],
        "correct": 2,
        "explanation": """**Correct: Overall well control on rig floor**"""
    },
    {
        "id": 100,
        "module": 8,
        "topic": "IWCF",
        "difficulty": "Medium",
        "question": "IWCF Level 2 Surface exam has how many questions?",
        "options": ["25 questions", "50 questions", "75 questions", "100 questions"],
        "correct": 1,
        "explanation": """**Correct: 50 questions**

50 questions in 2 hours. Pass = 70% = 35 correct."""
    },
]
# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════

# Quiz state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []  # Store all answers for review

# Timer state
if 'quiz_timer_enabled' not in st.session_state:
    st.session_state.quiz_timer_enabled = False
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
if 'time_per_question' not in st.session_state:
    st.session_state.time_per_question = 120  # 2 minutes default

# Statistics (local)
if 'total_quizzes_taken' not in st.session_state:
    st.session_state.total_quizzes_taken = 0
if 'total_correct_answers' not in st.session_state:
    st.session_state.total_correct_answers = 0
if 'total_questions_attempted' not in st.session_state:
    st.session_state.total_questions_attempted = 0

# XP tracking
if 'quiz_xp' not in st.session_state:
    st.session_state.quiz_xp = 0

# Load from Data Manager if available
if DATA_MANAGER_AVAILABLE:
    try:
        data = load_progress()
        st.session_state.quiz_xp = data['achievements'].get('xp_total', 0)
        st.session_state.total_quizzes_taken = data['quizzes'].get('completed', 0)
        st.session_state.total_questions_attempted = data['questions'].get('total_attempted', 0)
        st.session_state.total_correct_answers = data['questions'].get('total_correct', 0)
    except:
        pass

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="quiz-header">
    <h1>❓ IWCF Quiz Practice</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">100+ Real Exam Questions with Detailed Explanations</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        🎯 Practice → Learn → Pass!
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 SIDEBAR - USER STATS
# ═══════════════════════════════════════════════════════

st.sidebar.markdown("### 📊 Your Statistics")

# XP and Level
if DATA_MANAGER_AVAILABLE:
    try:
        data = load_progress()
        total_xp = data['achievements'].get('xp_total', 0)
        user_level = get_user_level(total_xp)
        streak = data['user'].get('study_streak', 0)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("⭐ XP", f"{total_xp:,}")
        with col2:
            st.metric("🔥 Streak", f"{streak}d")
        
        st.sidebar.markdown(f"""
        <div style="text-align: center; margin: 1rem 0;">
            <span class="level-badge">🏆 {user_level}</span>
        </div>
        """, unsafe_allow_html=True)
        
    except:
        st.sidebar.info("Data not available")
else:
    st.sidebar.info("📊 Connect Data Manager for full stats")

st.sidebar.markdown("---")

# Quiz statistics
st.sidebar.markdown("### 📈 Quiz Performance")

if st.session_state.total_quizzes_taken > 0:
    accuracy = (st.session_state.total_correct_answers / 
                max(st.session_state.total_questions_attempted, 1)) * 100
    
    st.sidebar.metric("📝 Quizzes Taken", st.session_state.total_quizzes_taken)
    st.sidebar.metric("✅ Total Correct", st.session_state.total_correct_answers)
    st.sidebar.metric("🎯 Accuracy", f"{accuracy:.1f}%")
    
    # Progress bar for accuracy
    if accuracy >= 70:
        color = "#10B981"
        status = "Passing!"
    elif accuracy >= 50:
        color = "#F59E0B"
        status = "Keep practicing"
    else:
        color = "#EF4444"
        status = "Needs work"
    
    st.sidebar.markdown(f"""
    <div style="background: #E5E7EB; border-radius: 10px; height: 20px; overflow: hidden; margin: 0.5rem 0;">
        <div style="background: {color}; height: 100%; width: {min(accuracy, 100)}%; 
                    display: flex; align-items: center; justify-content: center;
                    color: white; font-size: 0.75rem; font-weight: bold;">
            {accuracy:.0f}%
        </div>
    </div>
    <p style="text-align: center; color: {color}; font-size: 0.85rem;">{status}</p>
    """, unsafe_allow_html=True)
else:
    st.sidebar.info("Take your first quiz to see stats!")

st.sidebar.markdown("---")

# Quick links
st.sidebar.markdown("### 🔗 Quick Links")
if st.sidebar.button("📚 Go to Learn", use_container_width=True):
    st.switch_page("pages/01_📚_Learn.py")
if st.sidebar.button("📝 Mock Exam", use_container_width=True):
    st.switch_page("pages/03_📝_Mock_Exam.py")

# ═══════════════════════════════════════════════════════
# 🎮 QUIZ SETUP PAGE
# ═══════════════════════════════════════════════════════

if not st.session_state.quiz_started:
    
    st.markdown("## 🎯 Configure Your Quiz")
    
    # Main configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_questions = st.slider(
            "📊 Number of Questions:",
            min_value=5,
            max_value=25,
            value=10,
            step=5,
            help="Choose how many questions you want to practice"
        )
    
    with col2:
        difficulty = st.selectbox(
            "💪 Difficulty Level:",
            ["All Levels", "Easy Only", "Medium Only", "Hard Only"],
            help="Filter questions by difficulty"
        )
    
    with col3:
        quiz_mode = st.selectbox(
            "🎮 Quiz Mode:",
            ["Practice Mode", "Timed Mode", "Exam Simulation"],
            help="Choose your quiz experience"
        )
    
    st.markdown("---")
    
    # Module selection
    st.markdown("### 📚 Select Modules")
    st.caption("Leave empty to include all modules")
    
    # Create columns for module selection
    cols = st.columns(4)
    selected_modules = []
    
    for idx, (mod_id, mod_name) in enumerate(MODULES.items()):
        with cols[idx % 4]:
            if st.checkbox(f"Module {mod_id}", key=f"mod_select_{mod_id}"):
                selected_modules.append(mod_id)
    
    st.markdown("---")
    
    # Timer settings (for Timed Mode)
    if quiz_mode == "Timed Mode":
        st.markdown("### ⏱️ Timer Settings")
        time_per_q = st.slider(
            "Seconds per question:",
            min_value=30,
            max_value=300,
            value=120,
            step=30,
            help="Time allowed for each question"
        )
        st.session_state.time_per_question = time_per_q
        st.info(f"⏱️ Total time: {(time_per_q * num_questions) // 60} minutes {(time_per_q * num_questions) % 60} seconds")
    
    elif quiz_mode == "Exam Simulation":
        st.info("""
        🎓 **Exam Simulation Mode:**
        - 50 questions (like real IWCF exam)
        - 2 hours time limit
        - No explanations until end
        - Pass mark: 70%
        """)
        num_questions = 50
        st.session_state.time_per_question = 144  # 2 hours / 50 questions
    
    st.markdown("---")
    
    # Question pool info
    filtered_count = len(QUESTIONS_BANK)
    
    if selected_modules:
        filtered_count = len([q for q in QUESTIONS_BANK if q['module'] in selected_modules])
    
    if difficulty == "Easy Only":
        filtered_count = len([q for q in QUESTIONS_BANK if q['difficulty'] == "Easy" and (not selected_modules or q['module'] in selected_modules)])
    elif difficulty == "Medium Only":
        filtered_count = len([q for q in QUESTIONS_BANK if q['difficulty'] == "Medium" and (not selected_modules or q['module'] in selected_modules)])
    elif difficulty == "Hard Only":
        filtered_count = len([q for q in QUESTIONS_BANK if q['difficulty'] == "Hard" and (not selected_modules or q['module'] in selected_modules)])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); 
                padding: 1rem; border-radius: 10px; border-left: 4px solid #3B82F6;">
        <strong>📊 Question Pool:</strong> {filtered_count} questions available
        <br>
        <span style="color: #6B7280; font-size: 0.9rem;">
            Based on your selections: {num_questions} questions will be randomly selected
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Start button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START QUIZ", use_container_width=True, type="primary"):
            # Filter questions
            questions = QUESTIONS_BANK.copy()
            
            # Module filter
            if selected_modules:
                questions = [q for q in questions if q['module'] in selected_modules]
            
            # Difficulty filter
            if difficulty == "Easy Only":
                questions = [q for q in questions if q['difficulty'] == "Easy"]
            elif difficulty == "Medium Only":
                questions = [q for q in questions if q['difficulty'] == "Medium"]
            elif difficulty == "Hard Only":
                questions = [q for q in questions if q['difficulty'] == "Hard"]
            
            # Check if enough questions
            if len(questions) < num_questions:
                st.error(f"❌ Not enough questions! Only {len(questions)} available with current filters.")
            else:
                # Shuffle and select
                random.shuffle(questions)
                st.session_state.quiz_questions = questions[:num_questions]
                
                # Reset quiz state
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.selected_answer = None
                st.session_state.answer_submitted = False
                st.session_state.quiz_answers = []
                
                # Timer setup
                if quiz_mode in ["Timed Mode", "Exam Simulation"]:
                    st.session_state.quiz_timer_enabled = True
                    st.session_state.quiz_start_time = datetime.now()
                else:
                    st.session_state.quiz_timer_enabled = False
                
                st.rerun()

# ═══════════════════════════════════════════════════════
# 🎮 QUIZ IN PROGRESS
# ═══════════════════════════════════════════════════════

elif st.session_state.current_question < len(st.session_state.quiz_questions):
    
    q = st.session_state.quiz_questions[st.session_state.current_question]
    total = len(st.session_state.quiz_questions)
    current = st.session_state.current_question + 1
    
    # Top bar with progress and timer
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Progress bar
        progress = current / total
        st.progress(progress)
        st.caption(f"Question {current} of {total}")
    
    with col2:
        # Score display
        st.markdown(f"""
        <div style="background: #10B981; color: white; padding: 0.5rem 1rem; 
                    border-radius: 10px; text-align: center;">
            ✅ Score: {st.session_state.score}/{current-1 if current > 1 else 0}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Timer (if enabled)
        if st.session_state.quiz_timer_enabled and st.session_state.quiz_start_time:
            elapsed = (datetime.now() - st.session_state.quiz_start_time).seconds
            expected = st.session_state.current_question * st.session_state.time_per_question
            time_for_current = st.session_state.time_per_question
            time_spent_on_current = elapsed - expected
            remaining = time_for_current - time_spent_on_current
            
            if remaining > 60:
                st.markdown(f"""
                <div style="background: #3B82F6; color: white; padding: 0.5rem 1rem; 
                            border-radius: 10px; text-align: center;">
                    ⏱️ {remaining // 60}:{remaining % 60:02d}
                </div>
                """, unsafe_allow_html=True)
            elif remaining > 30:
                st.markdown(f"""
                <div class="timer-warning">
                    ⏱️ {remaining}s
                </div>
                """, unsafe_allow_html=True)
            elif remaining > 0:
                st.markdown(f"""
                <div class="timer-danger">
                    ⏱️ {remaining}s!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="timer-danger">
                    ⏱️ Time's up!
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Question card
    diff_class = f"difficulty-{q['difficulty'].lower()}"
    
    st.markdown(f"""
    <div class="question-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="color: #6B7280; font-size: 0.9rem;">
                📚 {MODULES.get(q['module'], f"Module {q['module']}")}
            </span>
            <span class="{diff_class}">{q['difficulty']}</span>
        </div>
        <p style="color: #6B7280; font-size: 0.85rem; margin-bottom: 0.5rem;">
            📝 Topic: {q['topic']}
        </p>
        <h3 style="color: #1F2937; line-height: 1.5;">{q['question']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Answer options
    if not st.session_state.answer_submitted:
        st.markdown("### 📝 Select Your Answer:")
        
        # Create styled radio buttons
        selected = st.radio(
            "Options:",
            options=range(len(q['options'])),
            format_func=lambda x: f"{chr(65+x)}) {q['options'][x]}",
            key=f"q_{st.session_state.current_question}",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
                st.session_state.selected_answer = selected
                st.session_state.answer_submitted = True
                
                # Check if correct
                is_correct = (selected == q['correct'])
                
                if is_correct:
                    st.session_state.score += 1
                
                # Store answer for review
                st.session_state.quiz_answers.append({
                    'question': q['question'],
                    'selected': selected,
                    'correct': q['correct'],
                    'is_correct': is_correct,
                    'options': q['options'],
                    'explanation': q['explanation']
                })
                
                # Save to Data Manager
                if DATA_MANAGER_AVAILABLE:
                    try:
                        data = load_progress()
                        
                        # Record question attempt
                        category = f"Module {q['module']} - {q['topic']}"
                        data = record_question_attempt(data, category, is_correct)
                        
                        save_progress(data)
                        
                        # Update local state
                        st.session_state.total_questions_attempted += 1
                        if is_correct:
                            st.session_state.total_correct_answers += 1
                        
                    except Exception as e:
                        pass
                else:
                    # Update local stats only
                    st.session_state.total_questions_attempted += 1
                    if is_correct:
                        st.session_state.total_correct_answers += 1
                
                st.rerun()
    
    else:
        # Show results
        st.markdown("### 📊 Answer Review:")
        
        for idx, option in enumerate(q['options']):
            if idx == q['correct']:
                st.markdown(f"""
                <div class="correct-box">
                    <strong>✅ {chr(65+idx)}) {option}</strong>
                    <span style="float: right; color: #065F46;">Correct Answer</span>
                </div>
                """, unsafe_allow_html=True)
            elif idx == st.session_state.selected_answer and idx != q['correct']:
                st.markdown(f"""
                <div class="wrong-box">
                    <strong>❌ {chr(65+idx)}) {option}</strong>
                    <span style="float: right; color: #991B1B;">Your Answer</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="normal-box">
                    {chr(65+idx)}) {option}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Result feedback
        if st.session_state.selected_answer == q['correct']:
            st.success("🎉 **Correct!** Well done!")
            
            # Show XP earned
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                        padding: 0.75rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <span class="xp-badge">+5 XP</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            correct_answer = q['options'][q['correct']]
            st.error(f"❌ **Incorrect.** The correct answer is: **{chr(65+q['correct'])}) {correct_answer}**")
        
        # Explanation
        with st.expander("📖 **Detailed Explanation**", expanded=True):
            st.markdown(q['explanation'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if current < total:
                if st.button("➡️ Next Question", use_container_width=True, type="primary"):
                    st.session_state.current_question += 1
                    st.session_state.selected_answer = None
                    st.session_state.answer_submitted = False
                    st.rerun()
            else:
                if st.button("🏁 Finish Quiz", use_container_width=True, type="primary"):
                    st.session_state.current_question += 1
                    st.rerun()
    
    # Quit button
    st.markdown("---")
    if st.button("🚪 Quit Quiz", type="secondary"):
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.rerun()

# ═══════════════════════════════════════════════════════
# 🏆 QUIZ COMPLETED
# ═══════════════════════════════════════════════════════

else:
    total = len(st.session_state.quiz_questions)
    score = st.session_state.score
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Calculate XP earned
    xp_earned = score * 5  # 5 XP per correct answer
    bonus_xp = 0
    
    if percentage >= 90:
        bonus_xp = 100
        grade = "A+"
        grade_color = "#10B981"
        message = "🌟 Outstanding! You're exam ready!"
    elif percentage >= 80:
        bonus_xp = 75
        grade = "A"
        grade_color = "#10B981"
        message = "🎯 Excellent work!"
    elif percentage >= 70:
        bonus_xp = 50
        grade = "B"
        grade_color = "#3B82F6"
        message = "✅ Good job! You passed!"
    elif percentage >= 60:
        bonus_xp = 25
        grade = "C"
        grade_color = "#F59E0B"
        message = "📚 Fair. More practice recommended."
    else:
        bonus_xp = 0
        grade = "F"
        grade_color = "#EF4444"
        message = "❌ Needs improvement. Review the topics."
    
    total_xp_earned = xp_earned + bonus_xp
    
    # Update statistics
    st.session_state.total_quizzes_taken += 1
    
    # Save to Data Manager
    if DATA_MANAGER_AVAILABLE:
        try:
            data = load_progress()
            
            # Record quiz completion
            data['quizzes']['completed'] = data['quizzes'].get('completed', 0) + 1
            
            if 'scores' not in data['quizzes']:
                data['quizzes']['scores'] = []
            
            data['quizzes']['scores'].append({
                'score': score,
                'total': total,
                'percentage': round(percentage, 1),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'xp_earned': total_xp_earned
            })
            
            # Keep only last 20 quiz records
            data['quizzes']['scores'] = data['quizzes']['scores'][-20:]
            
            # Add XP
            data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + total_xp_earned
            
            # Update streak
            data = update_streak(data)
            
            save_progress(data)
            
        except Exception as e:
            st.warning(f"Could not save progress: {e}")
    
    # Results display
    st.markdown(f"""
    <div class="score-card">
        <h1 style="margin: 0;">🎊 Quiz Complete!</h1>
        <div style="margin: 2rem 0;">
            <h2 style="margin: 0; font-size: 4rem; color: {grade_color};">{grade}</h2>
        </div>
        <h2 style="margin: 0;">Score: {score}/{total}</h2>
        <h1 style="font-size: 3.5rem; margin: 1rem 0;">{percentage:.0f}%</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if percentage >= 70:
        st.balloons()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # XP Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="margin: 0; color: #10B981;">✅ Correct</h3>
            <h2 style="margin: 0.5rem 0;">{score}</h2>
            <p style="color: #6B7280; margin: 0;">+{xp_earned} XP</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="margin: 0; color: #EF4444;">❌ Incorrect</h3>
            <h2 style="margin: 0.5rem 0;">{total - score}</h2>
            <p style="color: #6B7280; margin: 0;">Review needed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="margin: 0; color: #F59E0B;">🏆 Total XP</h3>
            <h2 style="margin: 0.5rem 0;">+{total_xp_earned}</h2>
            <p style="color: #6B7280; margin: 0;">Bonus: +{bonus_xp}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Performance by difficulty
    st.markdown("### 📊 Performance Analysis")
    
    easy_correct = sum(1 for i, a in enumerate(st.session_state.quiz_answers) 
                       if a['is_correct'] and st.session_state.quiz_questions[i]['difficulty'] == 'Easy')
    easy_total = sum(1 for q in st.session_state.quiz_questions if q['difficulty'] == 'Easy')
    
    medium_correct = sum(1 for i, a in enumerate(st.session_state.quiz_answers) 
                         if a['is_correct'] and st.session_state.quiz_questions[i]['difficulty'] == 'Medium')
    medium_total = sum(1 for q in st.session_state.quiz_questions if q['difficulty'] == 'Medium')
    
    hard_correct = sum(1 for i, a in enumerate(st.session_state.quiz_answers) 
                       if a['is_correct'] and st.session_state.quiz_questions[i]['difficulty'] == 'Hard')
    hard_total = sum(1 for q in st.session_state.quiz_questions if q['difficulty'] == 'Hard')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if easy_total > 0:
            pct = (easy_correct / easy_total) * 100
            st.markdown(f"""
            <div style="background: #D1FAE5; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong style="color: #065F46;">🟢 Easy</strong>
                <h3 style="margin: 0.5rem 0;">{easy_correct}/{easy_total}</h3>
                <p style="margin: 0; color: #065F46;">{pct:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if medium_total > 0:
            pct = (medium_correct / medium_total) * 100
            st.markdown(f"""
            <div style="background: #FEF3C7; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong style="color: #92400E;">🟡 Medium</strong>
                <h3 style="margin: 0.5rem 0;">{medium_correct}/{medium_total}</h3>
                <p style="margin: 0; color: #92400E;">{pct:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if hard_total > 0:
            pct = (hard_correct / hard_total) * 100
            st.markdown(f"""
            <div style="background: #FEE2E2; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong style="color: #991B1B;">🔴 Hard</strong>
                <h3 style="margin: 0.5rem 0;">{hard_correct}/{hard_total}</h3>
                <p style="margin: 0; color: #991B1B;">{pct:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Review all questions
    st.markdown("### 📋 Question Review")
    
    if st.checkbox("📝 Show All Questions & Answers"):
        for idx, answer in enumerate(st.session_state.quiz_answers):
            q = st.session_state.quiz_questions[idx]
            
            status_emoji = "✅" if answer['is_correct'] else "❌"
            status_color = "#10B981" if answer['is_correct'] else "#EF4444"
            
            with st.expander(f"{status_emoji} Question {idx+1}: {q['question'][:60]}..."):
                st.markdown(f"**Question:** {q['question']}")
                st.markdown(f"**Topic:** {q['topic']} | **Difficulty:** {q['difficulty']}")
                
                st.markdown("---")
                
                for i, option in enumerate(answer['options']):
                    if i == answer['correct']:
                        st.success(f"✅ {chr(65+i)}) {option} **(Correct)**")
                    elif i == answer['selected']:
                        st.error(f"❌ {chr(65+i)}) {option} **(Your Answer)**")
                    else:
                        st.markdown(f"{chr(65+i)}) {option}")
                
                st.markdown("---")
                st.markdown("**📖 Explanation:**")
                st.info(answer['explanation'])
    
    st.markdown("---")
    
    # Leaderboard / Recent Scores
    if DATA_MANAGER_AVAILABLE:
        st.markdown("### 🏆 Your Recent Scores")
        
        try:
            data = load_progress()
            recent_scores = data['quizzes'].get('scores', [])[-5:]
            
            if recent_scores:
                for i, quiz in enumerate(reversed(recent_scores), 1):
                    pct = quiz['percentage']
                    
                    if pct >= 70:
                        color = "#10B981"
                        icon = "🏆"
                    elif pct >= 50:
                        color = "#F59E0B"
                        icon = "📊"
                    else:
                        color = "#EF4444"
                        icon = "📉"
                    
                    st.markdown(f"""
                    <div class="leaderboard-item" style="border-left: 4px solid {color};">
                        <div>
                            <strong>{icon} #{i}</strong> - 
                            {quiz['score']}/{quiz['total']} ({pct:.0f}%)
                        </div>
                        <div style="color: #6B7280; font-size: 0.85rem;">
                            {quiz['date'][:10]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except:
            pass
    
    st.markdown("---")
    
    # Export results
    st.markdown("### 📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export
        export_data = {
            "quiz_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": f"{score}/{total}",
            "percentage": f"{percentage:.1f}%",
            "grade": grade,
            "xp_earned": total_xp_earned,
            "questions": [
                {
                    "number": i+1,
                    "question": st.session_state.quiz_questions[i]['question'],
                    "your_answer": chr(65 + a['selected']) + ") " + a['options'][a['selected']],
                    "correct_answer": chr(65 + a['correct']) + ") " + a['options'][a['correct']],
                    "result": "Correct" if a['is_correct'] else "Incorrect",
                    "topic": st.session_state.quiz_questions[i]['topic'],
                    "difficulty": st.session_state.quiz_questions[i]['difficulty']
                }
                for i, a in enumerate(st.session_state.quiz_answers)
            ]
        }
        
        st.download_button(
            label="📄 Download as JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Text summary export
        text_summary = f"""
IWCF Quiz Results
================
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Score: {score}/{total} ({percentage:.1f}%)
Grade: {grade}
XP Earned: {total_xp_earned}

Questions Summary:
------------------
"""
        for i, a in enumerate(st.session_state.quiz_answers):
            result = "✓" if a['is_correct'] else "✗"
            text_summary += f"{i+1}. [{result}] {st.session_state.quiz_questions[i]['topic']}\n"
        
        st.download_button(
            label="📝 Download as Text",
            data=text_summary,
            file_name=f"quiz_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.quiz_answers = []
            st.rerun()
    
    with col2:
        if st.button("📚 Review Topics", use_container_width=True):
            st.switch_page("pages/01_📚_Learn.py")
    
    with col3:
        if st.button("📝 Try Mock Exam", use_container_width=True):
            st.switch_page("pages/03_📝_Mock_Exam.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p style="margin: 0; font-size: 1.1rem;">
        ❓ <strong>Elshamy IWCF Quiz Practice</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0;">
        100+ Real Exam Questions | Detailed Explanations | Track Your Progress
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Created by Eng. Ahmed Elshamy | "Practice Makes Perfect" 💪
    </p>
</div>
""", unsafe_allow_html=True)