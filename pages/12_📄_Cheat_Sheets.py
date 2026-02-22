import streamlit as st
from datetime import datetime

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Cheat Sheets - IWCF Mastery",
    page_icon="📄",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .cheat-header {
        background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    .sheet-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #7C3AED;
    }
    
    .formula-box {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #3B82F6;
        font-family: 'Courier New', monospace;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #F59E0B;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #EF4444;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        margin: 0.5rem 0;
    }
    
    .table-container {
        overflow-x: auto;
        margin: 1rem 0;
    }
    
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .comparison-table th {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
        padding: 1rem;
        text-align: left;
    }
    
    .comparison-table td {
        padding: 0.8rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .comparison-table tr:hover {
        background: #F9FAFB;
    }
    
    .quick-ref {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #7C3AED;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .category-badge {
        background: #EDE9FE;
        color: #7C3AED;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📄 CHEAT SHEETS DATA
# ═══════════════════════════════════════════════════════

CHEAT_SHEETS = {
    "Essential Formulas": {
        "icon": "🧮",
        "color": "#3B82F6",
        "content": """
### 🧮 Essential IWCF Formulas

**1️⃣ Hydrostatic Pressure (HP):**
HP (psi) = 0.052 × MW (ppg) × TVD (ft)



**2️⃣ Kill Mud Weight (KMW):**
KMW = OMW + (SIDPP ÷ (0.052 × TVD))

Or:
KMW = OMW + Kick Gradient



**3️⃣ Initial Circulating Pressure (ICP):**
ICP = SIDPP + SCR



**4️⃣ Final Circulating Pressure (FCP):**
FCP = SCR × (KMW ÷ OMW)



**5️⃣ Formation Pressure:**
FP = HP + SIDPP



**6️⃣ Riser Margin (Subsea):**
RM = (MW - Seawater) × 0.052 × Water Depth

Minimum: 200 psi
Recommended: 400-600 psi



**7️⃣ MAASP:**
MAASP = Formation Breakdown Pressure - Current HP - Safety Margin



**8️⃣ Pressure Gradient:**
Gradient (psi/ft) = Pressure (psi) ÷ Depth (ft)



**9️⃣ Volume Calculations:**
Annular Volume (bbl) = (Hole ID² - Pipe OD²) × Length × 0.000971

Pipe Capacity (bbl) = Pipe ID² × Length × 0.000971



**🔟 Pump Output:**
Output (bbl/stk) = (Liner Diameter² × Stroke Length × Efficiency) ÷ 294


        """
    },
    
    "Kick Detection": {
        "icon": "⚠️",
        "color": "#EF4444",
        "content": """
### ⚠️ Kick Detection Quick Reference

**PRIMARY Signs (Act Immediately!):**
✅ PIT GAIN - Increase in mud volume
✅ FLOW RATE INCREASE - More flow out than in
✅ FLOW WITH PUMPS OFF - Well flowing when stopped
✅ DRILLING BREAK - Sudden increase in ROP



**SECONDARY Signs:**
⚠️ Pump Pressure DECREASE
⚠️ Pump Stroke INCREASE
⚠️ Cut Mud (gas/oil/water)
⚠️ Change in cuttings density
⚠️ Chloride increase (saltwater influx)
⚠️ Flowline temperature change



**Immediate Actions (30 seconds!):**
STOP PUMPING immediately
PICK UP OFF BOTTOM (raise kelly)
CHECK FOR FLOW (observe flow line)
SHUT IN WELL (close annular BOP)
RECORD PRESSURES (SIDPP & SICP)
NOTIFY SUPERVISOR


**What NOT to Do:**
❌ Continue drilling
❌ Delay shut-in
❌ Try to "control" without shutting in
❌ Forget to record pressures
❌ Panic!


        """
    },
    
    "Kill Methods Comparison": {
        "icon": "🎯",
        "color": "#10B981",
        "content": """
### 🎯 Kill Methods - Quick Comparison

**Driller's Method:**
✅ SIMPLE - Easy to execute
✅ NO WAIT - Start immediately
✅ SAFE - Lower error risk
❌ SLOW - Two circulations
❌ LONGER TIME - More pressure exposure

When to Use:
• Kill mud NOT ready
• Inexperienced crew
• Simple situation
• Time to prepare KMW



**Wait & Weight Method:**
✅ FAST - One circulation only
✅ EFFICIENT - Less time under pressure
✅ BETTER for weak formations
❌ WAIT - Need KMW ready first
❌ COMPLEX - More calculations
❌ HIGHER RISK - If done wrong

When to Use:
• Kill mud ready quickly
• Experienced crew
• Weak formation at shoe
• Time is critical



**Step-by-Step Comparison:**

| Step | Driller's Method | Wait & Weight |
|------|-----------------|---------------|
| **Circulation 1** | OMW (circulate out kick) | KMW (kill well) |
| **Pressure Start** | ICP | ICP |
| **Pressure End** | Zero | FCP |
| **Circulation 2** | KMW (kill well) | None needed |
| **Total Time** | Longer | Shorter |
| **Complexity** | Lower | Higher |
        """
    },
    
    "BOP Operations": {
        "icon": "🛡️",
        "color": "#F59E0B",
        "content": """
### 🛡️ BOP Quick Reference

**BOP Stack (Top to Bottom):**
ANNULAR PREVENTER
• Closes on any shape
• First line of defense
• Pressure: 3,000-5,000 psi

UPPER PIPE RAMS
• Specific pipe size
• Pressure: 10,000-15,000 psi

MIDDLE BLIND/SHEAR RAMS
• Blind: Close open hole
• Shear: CUT pipe (emergency!)

LOWER PIPE RAMS
• Backup for upper rams

KILL & CHOKE LINES
• Kill: Pump heavy mud
• Choke: Control flow



**BOP Testing Schedule:**
FUNCTION TEST: Every 7-14 days
• Test all components
• No pressure required
• Check opening/closing

PRESSURE TEST: Every 21 days
• After installation
• After repairs
• After disconnect
• Test to rated pressure



**Closing Sequence (Normal Kick):**
1st Choice: ANNULAR (fastest)
↓
2nd Choice: PIPE RAMS (if annular fails)
↓
3rd Choice: BLIND RAMS (if no pipe across)
↓
LAST RESORT: SHEAR RAMS (emergency only!)



**Critical Rules:**
⚠️ NEVER close on tool joint
⚠️ Space out before closing rams
⚠️ Know your BOP stack configuration
⚠️ Test regularly
⚠️ Shear rams = LAST RESORT only


        """
    },
    
    "Subsea Differences": {
        "icon": "🌊",
        "color": "#06B6D4",
        "content": """
### 🌊 Subsea vs Surface - Key Differences

**Choke Line Friction (CLF):**
Surface Reading ≠ True Reading!

True SICP = Surface SICP + CLF

Example:
Surface SICP: 800 psi
CLF: 200 psi
True SICP: 1,000 psi ← Use this!



**Riser Margin:**
Why needed?
• Keep riser full if disconnected
• Prevent U-tubing
• Safety margin

Formula:
RM = (MW - 8.6) × 0.052 × Water Depth

Minimum: 200 psi
Recommended: 400-600 psi



**MAASP Differences:**
SURFACE WELLS:
Weak point: Usually casing shoe

SUBSEA WELLS:
Weak point: Often WELLHEAD
MAASP is LOWER due to:
• Seawater (lighter than mud)
• Less hydrostatic pressure
• Wellhead limitations



**Emergency Disconnect:**
When?
• Rig drift
• Weather deterioration
• Equipment failure

What happens?

LMRP disconnects from BOP
BOP stays on SEABED
Well remains SHUT IN
Rig moves to safety
Return later to kill well


**Subsea Calculations Checklist:**
✅ Always ADD CLF to surface readings
✅ Maintain proper Riser Margin
✅ Check BOTH wellhead AND shoe limits
✅ Monitor MAASP continuously
✅ Know disconnect procedures


        """
    },
    
    "Common Mistakes": {
        "icon": "❌",
        "color": "#EF4444",
        "content": """
### ❌ Common Mistakes to Avoid

**Calculation Errors:**
❌ Using MD instead of TVD
✅ Always use True Vertical Depth

❌ Forgetting to add OMW in KMW formula
✅ KMW = (SIDPP/0.052/TVD) + OMW

❌ Not adding CLF in subsea
✅ True SICP = Surface SICP + CLF

❌ Wrong pressure units
✅ Check: psi, ppg, ft (not bar, kg/m³, m)

❌ Forgetting safety margin
✅ Add 0.5 ppg to KMW for safety



**Operational Errors:**
❌ Delaying shut-in when kick detected
✅ Shut in within 30 seconds

❌ Closing rams on tool joint
✅ Space out first, then close

❌ Not recording SIDPP & SICP
✅ Write down pressures immediately

❌ Using Shear Rams as first option
✅ Shear rams = LAST RESORT only

❌ Exceeding MAASP
✅ Monitor continuously, stay below limit



**Study/Exam Errors:**
❌ Memorizing without understanding
✅ Understand the WHY behind formulas

❌ Skipping practice questions
✅ Practice 20+ questions daily

❌ Not reviewing wrong answers
✅ Learn from every mistake

❌ Ignoring subsea differences
✅ Subsea is heavily tested!

❌ Rushing through exam
✅ Read questions carefully, manage time



**Critical Safety Errors:**
🚨 NEVER ignore kick signs
🚨 NEVER delay well shut-in
🚨 NEVER exceed MAASP
🚨 NEVER use untested BOP
🚨 NEVER assume - always verify


        """
    },
    
    "Quick Facts": {
        "icon": "⚡",
        "color": "#8B5CF6",
        "content": """
### ⚡ Quick Facts & Numbers

**Standard Values:**
Seawater Density: 8.6 ppg
Seawater Gradient: 0.445 psi/ft
Freshwater Gradient: 0.433 psi/ft
Normal Formation Gradient: 0.433-0.465 psi/ft
Conversion Constant: 0.052



**Typical Mud Weights:**
Light: 8.5-10 ppg
Normal: 10-12 ppg
Medium: 12-14 ppg
Heavy: 14-18 ppg
Very Heavy: 18+ ppg



**BOP Ratings:**
Annular: 3,000-5,000 psi
Rams: 10,000-15,000 psi
Deepwater BOP: Up to 20,000 psi



**Test Frequencies:**
BOP Function Test: 7-14 days
BOP Pressure Test: 21 days
Pit Drills: Weekly
Full Crew Drill: Monthly



**Time Limits:**
Kick Detection: Immediate
Well Shut-in: 30 seconds max
Record Pressures: 1-2 minutes
Notify Supervisor: Immediately
Start Kill: ASAP (after verification)



**Safety Margins:**
Kill Mud Weight: +0.5 ppg
Riser Margin: 400-600 psi (min 200)
Trip Margin: 200-300 psi
Fracture Gradient Safety: 0.5-1.0 ppg



**Kick Types:**
GAS KICK:
• SICP > SIDPP
• Lightest fluid
• Most dangerous

OIL KICK:
• SICP ≈ SIDPP
• Medium density
• Moderate danger

WATER KICK:
• SICP < SIDPP
• Heaviest fluid
• Least dangerous (but still serious!)



**Critical Pressures:**
SIDPP: Shut-In Drill Pipe Pressure
SICP: Shut-In Casing Pressure
ICP: Initial Circulating Pressure
FCP: Final Circulating Pressure
MAASP: Maximum Allowable Annular Surface Pressure


        """
    },
    
    "Exam Tips": {
        "icon": "📝",
        "color": "#10B981",
        "content": """
### 📝 IWCF Exam Success Tips

**Before the Exam:**
✅ Sleep well (7-8 hours)
✅ Eat proper breakfast
✅ Arrive 30 min early
✅ Bring calculator, ID, confirmation
✅ Visit bathroom before exam
✅ Turn off phone



**During the Exam:**
1️⃣ READ CAREFULLY
• Don't rush
• Read question twice
• Underline key info

2️⃣ TIME MANAGEMENT
• Note total time
• Allocate time per question
• Don't get stuck on one question

3️⃣ ANSWERING STRATEGY
• Easy questions first
• Flag difficult ones
• Return to flagged later
• Never leave blank

4️⃣ CALCULATIONS
• Write down formula
• Show your work
• Double-check units
• Verify answer makes sense

5️⃣ MULTIPLE CHOICE
• Eliminate wrong answers
• Watch for "ALWAYS" or "NEVER"
• Look for keywords
• Trust your preparation



**Common Exam Traps:**
⚠️ MD vs TVD - Always use TVD!
⚠️ Surface vs True SICP in subsea
⚠️ Forgetting to add OMW
⚠️ Wrong units (psi vs bar)
⚠️ Not reading "EXCEPT" in question
⚠️ Rushing through calculations



**High-Probability Topics:**
🔥 Kill Mud Weight calculations
🔥 ICP & FCP calculations
🔥 Kick detection signs
🔥 BOP components & operations
🔥 Driller's vs W&W Method
🔥 Subsea differences (CLF, Riser Margin)
🔥 MAASP calculations
🔥 Safety procedures



**Last 10 Minutes:**
✓ Review flagged questions
✓ Check all calculations
✓ Verify no blanks
✓ Don't change answers (unless sure)
✓ Stay calm & confident



**Remember:**
💪 You've prepared for this
🎯 Trust your knowledge
⏰ Manage your time
📝 Read carefully
🧮 Double-check calculations
✅ You've got this!


        """
    }
}

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="cheat-header">
    <h1>📄 IWCF Cheat Sheets</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Quick reference guide for all essential IWCF concepts
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Everything you need in one place - Study smart, not hard!
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📋 SHEET SELECTOR
# ═══════════════════════════════════════════════════════

st.markdown("## 📋 Select Cheat Sheet")

# Create buttons for each sheet
cols = st.columns(4)

sheet_names = list(CHEAT_SHEETS.keys())

for idx, sheet_name in enumerate(sheet_names):
    sheet_data = CHEAT_SHEETS[sheet_name]
    
    with cols[idx % 4]:
        if st.button(
            f"{sheet_data['icon']} {sheet_name}",
            key=f"sheet_{idx}",
            use_container_width=True
        ):
            st.session_state.selected_sheet = sheet_name

# Default selection
if 'selected_sheet' not in st.session_state:
    st.session_state.selected_sheet = "Essential Formulas"

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📄 DISPLAY SELECTED SHEET
# ═══════════════════════════════════════════════════════

selected = CHEAT_SHEETS[st.session_state.selected_sheet]

st.markdown(f"""
<div class="sheet-card">
    <h2 style="color: {selected['color']}; margin: 0;">
        {selected['icon']} {st.session_state.selected_sheet}
    </h2>
</div>
""", unsafe_allow_html=True)

# Display content
st.markdown(selected['content'])

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎯 QUICK ACTIONS
# ═══════════════════════════════════════════════════════

st.markdown("## 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧮 Use Calculator", use_container_width=True):
        st.switch_page("pages/04_🧮_Calculator.py")

with col2:
    if st.button("❓ Practice Quiz", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")

with col3:
    if st.button("🎴 Study Flashcards", use_container_width=True):
        st.switch_page("pages/08_🎴_Flashcards.py")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 💡 STUDY TIPS
# ═══════════════════════════════════════════════════════

st.markdown("## 💡 How to Use Cheat Sheets Effectively")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tip-box">
        <strong>📚 Daily Review:</strong>
        <p style="margin: 0.5rem 0 0 0;">
            • Review one sheet per day<br>
            • Focus on weak areas<br>
            • Test yourself without looking
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <strong>✅ Before Exam:</strong>
        <p style="margin: 0.5rem 0 0 0;">
            • Review all sheets 2 days before<br>
            • Focus on formulas the night before<br>
            • Quick scan 1 hour before exam
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Don't Just Memorize:</strong>
        <p style="margin: 0.5rem 0 0 0;">
            • Understand the concepts<br>
            • Practice applying formulas<br>
            • Use AI Tutor for clarification
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-box">
        <strong>🎯 Pro Tip:</strong>
        <p style="margin: 0.5rem 0 0 0;">
            Print these sheets and keep them handy!<br>
            Take screenshots for offline study.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        📄 <strong>Elshamy IWCF Mastery Method™ - Cheat Sheets</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Knowledge is power when it's organized" 📚
    </p>
</div>
""", unsafe_allow_html=True)