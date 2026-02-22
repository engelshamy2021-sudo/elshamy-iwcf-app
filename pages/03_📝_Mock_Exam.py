"""
📝 ELSHAMY IWCF - Mock Exam System
Full simulation with Data Manager integration
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import time

# 🔗 Import Data Manager
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_manager import (
    load_progress, 
    save_progress, 
    record_exam_result,
    get_overall_stats,
    check_and_award_badges
)

# ═══════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Mock Exam - Elshamy IWCF",
    page_icon="📝",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# التصميم
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .exam-header {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
    }
    
    .timer-box {
        background: #DBEAFE;
        border: 3px solid #3B82F6;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E40AF;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    .timer-warning {
        background: #FEF3C7;
        border-color: #F59E0B;
        color: #92400E;
        animation: pulse-warning 2s infinite;
    }
    
    .timer-danger {
        background: #FEE2E2;
        border-color: #EF4444;
        color: #991B1B;
        animation: pulse-danger 1s infinite;
    }
    
    @keyframes pulse-warning {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes pulse-danger {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .q-navigator {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 0.5rem;
        margin: 1rem 0;
        padding: 1rem;
        background: #F9FAFB;
        border-radius: 10px;
    }
    
    .q-nav-btn {
        padding: 0.5rem;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        font-weight: bold;
        border: 2px solid #E5E7EB;
        transition: all 0.2s ease;
    }
    
    .q-nav-btn:hover {
        transform: scale(1.1);
    }
    
    .q-answered {
        background: #D1FAE5;
        border-color: #10B981;
        color: #065F46;
    }
    
    .q-current {
        background: #3B82F6;
        border-color: #1E40AF;
        color: white;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4);
    }
    
    .q-marked {
        background: #FEF3C7;
        border-color: #F59E0B;
        color: #92400E;
    }
    
    .q-unanswered {
        background: #F3F4F6;
        color: #6B7280;
    }
    
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .pass-badge {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
        padding: 1.5rem 3rem;
        border-radius: 50px;
        font-size: 2rem;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
        animation: bounce 1s;
    }
    
    .fail-badge {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 1.5rem 3rem;
        border-radius: 50px;
        font-size: 2rem;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.4);
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .review-correct {
        background: #D1FAE5;
        border: 2px solid #10B981;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .review-wrong {
        background: #FEE2E2;
        border: 2px solid #EF4444;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 4px solid #3B82F6;
    }
    
    .xp-notification {
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📚 بنك أسئلة Mock Exam (50 سؤال)
# ═══════════════════════════════════════════════════════

MOCK_EXAM_BANK = [
    # Module 1: Fundamentals (10 questions)
    {"q": "What is the PRIMARY barrier in well control?", "options": ["BOP", "Mud Weight (Hydrostatic Pressure)", "Casing", "Cement"], "correct": 1, "topic": "Fundamentals", "explanation": "Mud weight creates hydrostatic pressure - the primary barrier preventing formation fluids from entering the wellbore."},
    {"q": "What is the SECONDARY barrier?", "options": ["Mud Weight", "Casing", "BOP System", "Cement"], "correct": 2, "topic": "Fundamentals", "explanation": "BOP (Blowout Preventer) is the secondary barrier used when the primary barrier (mud) fails."},
    {"q": "Minimum number of barriers required at all times:", "options": ["One", "Two", "Three", "Four"], "correct": 1, "topic": "Fundamentals", "explanation": "Industry standard requires minimum TWO barriers at all times."},
    {"q": "What is a 'Kick'?", "options": ["Controlled flow", "Uncontrolled influx of formation fluids", "Mud loss", "Pump pressure increase"], "correct": 1, "topic": "Fundamentals", "explanation": "A kick is when formation fluids enter the wellbore due to insufficient bottomhole pressure."},
    {"q": "Normal formation pressure gradient is approximately:", "options": ["0.433 psi/ft", "0.465 psi/ft", "0.520 psi/ft", "0.624 psi/ft"], "correct": 1, "topic": "Fundamentals", "explanation": "Normal formation pressure gradient equals approximately 0.465 psi/ft (equivalent to ~8.94 ppg)."},
    {"q": "If HP > FP, the well is:", "options": ["Underbalanced", "Overbalanced", "Balanced", "In kick"], "correct": 1, "topic": "Fundamentals", "explanation": "Overbalanced means hydrostatic pressure exceeds formation pressure - safe condition."},
    {"q": "Which depth is used for hydrostatic calculations?", "options": ["Measured Depth (MD)", "True Vertical Depth (TVD)", "Total Depth", "Drilled Depth"], "correct": 1, "topic": "Fundamentals", "explanation": "Hydrostatic pressure depends on vertical fluid column only, so always use TVD."},
    {"q": "What causes a kick?", "options": ["High pump rate", "Insufficient mud weight", "Fast drilling", "Heavy mud"], "correct": 1, "topic": "Fundamentals", "explanation": "Insufficient mud weight (underbalance) is the primary cause - HP < FP allows formation fluids to enter."},
    {"q": "Swabbing can cause a kick because it:", "options": ["Increases BHP", "Reduces BHP temporarily", "Increases MW", "Seals formation"], "correct": 1, "topic": "Fundamentals", "explanation": "Swabbing (pulling pipe too fast) creates suction that temporarily reduces bottomhole pressure."},
    {"q": "What is 'Overbalance'?", "options": ["HP < FP", "HP > FP", "HP = FP", "No HP"], "correct": 1, "topic": "Fundamentals", "explanation": "Overbalance = Hydrostatic Pressure greater than Formation Pressure (safe drilling condition)."},
    
    # Module 2: Pressure Calculations (12 questions)
    {"q": "Calculate hydrostatic pressure: 10,000 ft TVD, 12 ppg mud", "options": ["5,200 psi", "6,000 psi", "6,240 psi", "7,200 psi"], "correct": 2, "topic": "Calculations", "explanation": "HP = 0.052 × 12 × 10,000 = 6,240 psi"},
    {"q": "What mud weight creates 5,200 psi at 10,000 ft?", "options": ["8 ppg", "10 ppg", "12 ppg", "14 ppg"], "correct": 1, "topic": "Calculations", "explanation": "MW = 5,200 / (0.052 × 10,000) = 10 ppg"},
    {"q": "Pressure gradient of 10 ppg mud:", "options": ["0.433 psi/ft", "0.465 psi/ft", "0.520 psi/ft", "0.624 psi/ft"], "correct": 2, "topic": "Calculations", "explanation": "Gradient = 0.052 × 10 = 0.520 psi/ft"},
    {"q": "Formation pressure after shut-in: TVD = 10,000 ft, MW = 10 ppg, SIDPP = 200 psi", "options": ["5,000 psi", "5,200 psi", "5,400 psi", "5,600 psi"], "correct": 2, "topic": "Calculations", "explanation": "FP = HP + SIDPP = (0.052 × 10 × 10,000) + 200 = 5,400 psi"},
    {"q": "Kill Mud Weight: OMW = 10 ppg, SIDPP = 260 psi, TVD = 10,000 ft", "options": ["10.3 ppg", "10.5 ppg", "10.7 ppg", "11.0 ppg"], "correct": 1, "topic": "Calculations", "explanation": "KMW = 10 + (260 / 0.052 / 10,000) = 10.5 ppg"},
    {"q": "ECD calculation: MW = 11 ppg, APL = 286 psi, TVD = 10,000 ft", "options": ["11.25 ppg", "11.55 ppg", "11.75 ppg", "12.00 ppg"], "correct": 1, "topic": "Calculations", "explanation": "ECD = 11 + (286 / 0.052 / 10,000) = 11.55 ppg"},
    {"q": "ECD is ALWAYS:", "options": ["Less than MW", "Equal to MW", "Greater than MW when circulating", "Zero"], "correct": 2, "topic": "Calculations", "explanation": "ECD = MW + APL, so during circulation ECD > MW"},
    {"q": "MAASP: LOT = 15 ppg, MW = 12 ppg, Shoe TVD = 5,000 ft", "options": ["680 psi", "780 psi", "880 psi", "980 psi"], "correct": 1, "topic": "Calculations", "explanation": "MAASP = (15 - 12) × 0.052 × 5,000 = 780 psi"},
    {"q": "If you INCREASE mud weight, MAASP will:", "options": ["Increase", "Decrease", "Stay same", "Double"], "correct": 1, "topic": "Calculations", "explanation": "MAASP = (LOT - MW) × constant, so higher MW = lower MAASP"},
    {"q": "ICP calculation: SIDPP = 400 psi, SCR = 500 psi", "options": ["800 psi", "900 psi", "1000 psi", "1100 psi"], "correct": 1, "topic": "Calculations", "explanation": "ICP = SIDPP + SCR = 400 + 500 = 900 psi"},
    {"q": "FCP: SCR = 500 psi, KMW = 11 ppg, OMW = 10 ppg", "options": ["500 psi", "525 psi", "550 psi", "575 psi"], "correct": 2, "topic": "Calculations", "explanation": "FCP = 500 × (11/10) = 550 psi"},
    {"q": "Which pressure is used to calculate formation pressure?", "options": ["SICP", "SIDPP", "Pump pressure", "Casing pressure"], "correct": 1, "topic": "Calculations", "explanation": "SIDPP directly reads formation pressure. Formula: FP = HP + SIDPP"},
    
    # Module 3: Kick Detection (8 questions)
    {"q": "Most RELIABLE kick indicator:", "options": ["Drilling break", "Pit gain", "Connection gas", "Pump pressure"], "correct": 1, "topic": "Kick Detection", "explanation": "Pit gain is the most reliable and definitive indicator of a kick."},
    {"q": "All are PRIMARY kick indicators EXCEPT:", "options": ["Pit gain", "Flow increase", "Drilling break", "Pump pressure drop"], "correct": 2, "topic": "Kick Detection", "explanation": "Drilling break is a SECONDARY (indirect) indicator."},
    {"q": "FIRST action when kick detected:", "options": ["Close BOP", "Stop pumps", "Notify supervisor", "Increase MW"], "correct": 1, "topic": "Kick Detection", "explanation": "Always stop pumps FIRST. Sequence: Stop → Raise → Close → Record"},
    {"q": "SICP = 700 psi, SIDPP = 400 psi. Kick is most likely:", "options": ["Water", "Oil", "Gas", "Mud"], "correct": 2, "topic": "Kick Detection", "explanation": "SICP >> SIDPP indicates light fluid = Gas kick"},
    {"q": "If SICP ≈ SIDPP, the kick is probably:", "options": ["Gas", "Liquid (water/oil)", "Air", "Cannot determine"], "correct": 1, "topic": "Kick Detection", "explanation": "Similar pressures indicate kick fluid has similar density to mud = liquid kick"},
    {"q": "Hard shut-in procedure means:", "options": ["Slow closure", "Close BOP then open choke", "Open choke then close BOP", "High pressure"], "correct": 1, "topic": "Kick Detection", "explanation": "Hard shut-in: Close BOP immediately, then open choke to read pressures (standard method)"},
    {"q": "Drilling break is a:", "options": ["Primary indicator", "Secondary indicator", "Not an indicator", "Equipment alarm"], "correct": 1, "topic": "Kick Detection", "explanation": "Drilling break (sudden ROP increase) is a secondary warning sign, not definite confirmation."},
    {"q": "Pit volume should be monitored with accuracy of:", "options": ["± 10 bbls", "± 5 bbls", "± 1 bbl", "Not important"], "correct": 2, "topic": "Kick Detection", "explanation": "Accurate pit monitoring (± 1 bbl) is critical for early kick detection."},
    
    # Module 4: Kill Methods (10 questions)
    {"q": "Driller's Method requires how many circulations?", "options": ["One", "Two", "Three", "Depends"], "correct": 1, "topic": "Kill Methods", "explanation": "Driller's Method: 2 circulations (1st removes kick, 2nd kills with heavy mud)"},
    {"q": "Wait and Weight Method requires:", "options": ["One circulation", "Two circulations", "Three circulations", "No circulation"], "correct": 0, "topic": "Kill Methods", "explanation": "Wait & Weight (Engineer's Method): 1 circulation only"},
    {"q": "During Driller's Method first circulation, maintain:", "options": ["Constant SICP", "Constant ICP", "Constant pump rate", "Constant MW"], "correct": 1, "topic": "Kill Methods", "explanation": "Hold constant drillpipe pressure (ICP) throughout first circulation to maintain constant BHP"},
    {"q": "During Wait & Weight, drillpipe pressure:", "options": ["Stays at ICP", "Decreases from ICP to FCP", "Increases", "Stays at FCP"], "correct": 1, "topic": "Kill Methods", "explanation": "Pressure decreases linearly from ICP to FCP as kill mud reaches bit"},
    {"q": "Volumetric Method is used when:", "options": ["Kick is large", "MW is high", "Circulation NOT possible", "Gas kick only"], "correct": 2, "topic": "Kill Methods", "explanation": "Volumetric when circulation impossible (stuck pipe, plugged string, pump failure)"},
    {"q": "In Volumetric Method, as gas migrates up:", "options": ["Pump mud in", "Close choke", "Bleed mud to reduce pressure", "Wait"], "correct": 2, "topic": "Kill Methods", "explanation": "Bleed mud equal to pressure increase to maintain constant BHP"},
    {"q": "Bullheading pushes the kick:", "options": ["To surface", "Back into formation", "Into casing", "Through choke"], "correct": 1, "topic": "Kill Methods", "explanation": "Bullheading forces kick back into formation (used for H2S or when no drillstring)"},
    {"q": "Bullheading is preferred for:", "options": ["Normal gas", "H2S kick", "Small water kick", "All kicks"], "correct": 1, "topic": "Kill Methods", "explanation": "H2S is deadly - bullhead pushes it back into formation instead of bringing to surface"},
    {"q": "Which method gives LOWER casing pressure?", "options": ["Driller's Method", "Wait and Weight", "Both equal", "Volumetric"], "correct": 1, "topic": "Kill Methods", "explanation": "Wait & Weight keeps casing pressure lower because kill mud is introduced immediately"},
    {"q": "During kill, BHP should be maintained:", "options": ["Below FP", "Equal to FP", "Slightly above FP", "Maximum"], "correct": 2, "topic": "Kill Methods", "explanation": "BHP must stay slightly above formation pressure to prevent more influx"},
    
    # Module 5: Equipment (5 questions)
    {"q": "Annular preventer can seal around:", "options": ["Drill pipe only", "Specific size only", "Any shape or size", "Open hole only"], "correct": 2, "topic": "Equipment", "explanation": "Annular has flexible rubber element that conforms to any shape"},
    {"q": "Which BOP element can cut the drill pipe?", "options": ["Annular", "Pipe rams", "Blind rams", "Shear rams"], "correct": 3, "topic": "Equipment", "explanation": "Shear rams have cutting blades - used as LAST RESORT emergency only"},
    {"q": "Blind rams seal:", "options": ["Around pipe", "Open hole (no pipe)", "Any size pipe", "Kelly only"], "correct": 1, "topic": "Equipment", "explanation": "Blind rams seal when NO pipe in BOP. Warning: Never close with pipe in hole!"},
    {"q": "Accumulator bottles are pre-charged with:", "options": ["Air", "Nitrogen", "Hydraulic fluid", "Oxygen"], "correct": 1, "topic": "Equipment", "explanation": "Nitrogen is used because it's inert, non-flammable, and compressible"},
    {"q": "Opening the choke will:", "options": ["Increase backpressure", "Decrease backpressure", "No effect", "Close well"], "correct": 1, "topic": "Equipment", "explanation": "More choke opening = Less restriction = Less backpressure"},
    
    # Module 6: Gas Behavior (5 questions)
    {"q": "As gas rises in the well, it:", "options": ["Compresses", "Expands", "Stays same", "Disappears"], "correct": 1, "topic": "Gas Behavior", "explanation": "Boyle's Law: P₁V₁ = P₂V₂. As pressure decreases (rising), volume increases"},
    {"q": "Gas volume = 5 bbls at 5,000 psi. Volume at 500 psi?", "options": ["10 bbls", "25 bbls", "50 bbls", "100 bbls"], "correct": 2, "topic": "Gas Behavior", "explanation": "V₂ = 5,000 × 5 / 500 = 50 bbls (10× pressure drop = 10× volume increase)"},
    {"q": "Typical gas migration rate:", "options": ["100 ft/hr", "500 ft/hr", "1,000 ft/hr", "5,000 ft/hr"], "correct": 2, "topic": "Gas Behavior", "explanation": "Average gas migration rate is approximately 1,000 ft/hour"},
    {"q": "Most rapid gas expansion occurs:", "options": ["At bottom", "Mid-well", "Near surface", "Equal throughout"], "correct": 2, "topic": "Gas Behavior", "explanation": "Near surface, pressure changes more dramatically per foot = rapid expansion"},
    {"q": "Gas kick is more dangerous because:", "options": ["It's heavier", "It expands as it rises", "Easier to detect", "Doesn't migrate"], "correct": 1, "topic": "Gas Behavior", "explanation": "Small gas kick at depth can expand massively at surface (Boyle's Law)"},
    
    # Module 7: Complications (5 questions)
    {"q": "Lost circulation increases risk of:", "options": ["Equipment damage", "Stuck pipe", "Kick", "Nothing"], "correct": 2, "topic": "Complications", "explanation": "Lost circulation = losing hydrostatic pressure. If HP < FP = Kick!"},
    {"q": "If losses occur during kill:", "options": ["Shut in", "Increase rate", "Continue at reduced rate", "Stop"], "correct": 2, "topic": "Complications", "explanation": "Reduce pump rate (lower ECD) but continue circulating to maintain BHP"},
    {"q": "Underground blowout is flow:", "options": ["To surface", "From one zone to another underground", "Into drillpipe", "Through casing"], "correct": 1, "topic": "Complications", "explanation": "Underground blowout: high-pressure zone flows to weak zone, all underground"},
    {"q": "If pipe sticks during kill, priority is:", "options": ["Free pipe", "Maintain well control", "Pull hard", "Increase rate"], "correct": 1, "topic": "Complications", "explanation": "Well control ALWAYS first! Can use volumetric method if stuck"},
    {"q": "H2S at 100 ppm will:", "options": ["Strong smell", "Paralyze sense of smell", "No effect", "Headache"], "correct": 1, "topic": "Complications", "explanation": "High H2S paralyzes olfactory nerves - you can't smell it at deadly concentrations!"},
    
    # Module 8: Procedures (5 questions)
    {"q": "IWCF certificate is valid for:", "options": ["1 year", "2 years", "5 years", "Lifetime"], "correct": 1, "topic": "Procedures", "explanation": "IWCF certificates must be renewed every 2 years"},
    {"q": "IWCF exam pass mark:", "options": ["50%", "60%", "70%", "80%"], "correct": 2, "topic": "Procedures", "explanation": "70% (35/50 questions) required to pass IWCF exam"},
    {"q": "Primary barrier in drilling well:", "options": ["BOP", "Casing", "Mud column", "Cement"], "correct": 2, "topic": "Procedures", "explanation": "Mud (hydrostatic pressure) is always the primary barrier during drilling"},
    {"q": "Barriers must be:", "options": ["Assumed working", "Installed only", "Tested and verified", "Optional"], "correct": 2, "topic": "Procedures", "explanation": "Never assume - always verify barriers through testing"},
    {"q": "Shut-in time from kick detection should be:", "options": ["< 5 min", "< 2 min", "< 10 min", "Doesn't matter"], "correct": 1, "topic": "Procedures", "explanation": "Fast shut-in (< 2 minutes) = smaller kick = easier kill"},
]

# ═══════════════════════════════════════════════════════
# Session State
# ═══════════════════════════════════════════════════════

def init_exam_state():
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'exam_answers' not in st.session_state:
        st.session_state.exam_answers = {}
    if 'marked_questions' not in st.session_state:
        st.session_state.marked_questions = set()
    if 'current_exam_q' not in st.session_state:
        st.session_state.current_exam_q = 0
    if 'exam_start_time' not in st.session_state:
        st.session_state.exam_start_time = None
    if 'exam_submitted' not in st.session_state:
        st.session_state.exam_submitted = False
    if 'exam_questions' not in st.session_state:
        st.session_state.exam_questions = []
    if 'reviewing_answers' not in st.session_state:
        st.session_state.reviewing_answers = False
    if 'xp_awarded' not in st.session_state:
        st.session_state.xp_awarded = False
    
    # 🆕 Load exam history from Data Manager
    if 'exam_results_history' not in st.session_state:
        try:
            progress = load_progress()
            st.session_state.exam_results_history = progress['exams']['exam_history']
        except:
            st.session_state.exam_results_history = []

init_exam_state()

# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="exam-header">
    <h1>📝 IWCF Mock Examination</h1>
    <p>Simulate real exam conditions - 50 questions, 120 minutes, 70% to pass</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# EXAM SETUP
# ═══════════════════════════════════════════════════════

if not st.session_state.exam_started:
    
    st.markdown("## 🎯 IWCF Level 4 - Surface Stack Mock Exam")
    
    st.markdown("""
    <div style="background: #DBEAFE; border-left: 5px solid #3B82F6; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
        <h3>📋 Exam Instructions:</h3>
        <ul>
            <li>⏱️ <strong>Time Limit:</strong> 120 minutes (2 hours)</li>
            <li>❓ <strong>Questions:</strong> 50 multiple choice</li>
            <li>✅ <strong>Pass Mark:</strong> 70% (35/50 correct)</li>
            <li>📝 <strong>Format:</strong> Single best answer</li>
            <li>🔄 <strong>Navigation:</strong> Jump to any question</li>
            <li>🔖 <strong>Mark for review:</strong> Flag difficult questions</li>
            <li>⏰ <strong>Auto-submit:</strong> When time expires</li>
            <li>📊 <strong>Review:</strong> See all answers after submission</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 🆕 Stats from Data Manager
    try:
        progress = load_progress()
        exam_stats = progress['exams']
        
        st.markdown("### 📊 Your Exam Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("📝 Exams Taken", exam_stats['mock_exams_taken'])
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("✅ Passed", exam_stats['mock_exams_passed'])
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("🏆 Best Score", f"{exam_stats['best_score']}%")
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("📊 Average", f"{exam_stats['average_score']}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent attempts
        if exam_stats['exam_history']:
            st.markdown("### 📈 Last 3 Attempts:")
            recent_exams = exam_stats['exam_history'][-3:]
            
            for idx, result in enumerate(reversed(recent_exams), 1):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text(f"📅 {result['date']}")
                with col2:
                    st.text(f"📊 {result['score']}%")
                with col3:
                    if result['passed']:
                        st.success("✅ PASS")
                    else:
                        st.error("❌ FAIL")
    except:
        st.info("📝 No previous exam history. This will be your first attempt!")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 START EXAM", use_container_width=True, type="primary"):
            # Select 50 random questions
            questions = random.sample(MOCK_EXAM_BANK, min(50, len(MOCK_EXAM_BANK)))
            
            st.session_state.exam_questions = questions
            st.session_state.exam_answers = {}
            st.session_state.marked_questions = set()
            st.session_state.current_exam_q = 0
            st.session_state.exam_start_time = datetime.now()
            st.session_state.exam_started = True
            st.session_state.exam_submitted = False
            st.session_state.reviewing_answers = False
            st.session_state.xp_awarded = False
            st.rerun()

# ═══════════════════════════════════════════════════════
# EXAM IN PROGRESS
# ═══════════════════════════════════════════════════════

elif st.session_state.exam_started and not st.session_state.exam_submitted:
    
    # Timer calculation
    elapsed = datetime.now() - st.session_state.exam_start_time
    remaining = timedelta(minutes=120) - elapsed
    remaining_seconds = int(remaining.total_seconds())
    
    # Auto-submit if time up
    if remaining_seconds <= 0:
        st.session_state.exam_submitted = True
        st.warning("⏰ Time's up! Exam auto-submitted.")
        st.rerun()
    
    # Timer display
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds % 3600) // 60
    seconds = remaining_seconds % 60
    
    timer_class = "timer-box"
    if remaining_seconds < 300:  # 5 minutes
        timer_class = "timer-box timer-danger"
    elif remaining_seconds < 1800:  # 30 minutes
        timer_class = "timer-box timer-warning"
    
    # Top bar: Timer + Progress
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="{timer_class}">
            ⏰ {hours:02d}:{minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        answered = len(st.session_state.exam_answers)
        total = len(st.session_state.exam_questions)
        progress_pct = answered / total if total > 0 else 0
        st.progress(progress_pct)
        st.markdown(f"**Progress:** {answered}/{total} answered | {len(st.session_state.marked_questions)} marked")
    
    # Question Navigator
    st.markdown("### 🗺️ Question Navigator")
    
    nav_html = '<div class="q-navigator">'
    for idx in range(len(st.session_state.exam_questions)):
        is_current = idx == st.session_state.current_exam_q
        is_answered = idx in st.session_state.exam_answers
        is_marked = idx in st.session_state.marked_questions
        
        if is_current:
            q_class = "q-current"
        elif is_marked:
            q_class = "q-marked"
        elif is_answered:
            q_class = "q-answered"
        else:
            q_class = "q-unanswered"
        
        nav_html += f'<div class="q-nav-btn {q_class}">{idx + 1}</div>'
    
    nav_html += '</div>'
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Jump to question
    col_a, col_b = st.columns([3, 1])
    with col_a:
        jump_to = st.number_input(
            "Jump to question:",
            min_value=1,
            max_value=len(st.session_state.exam_questions),
            value=st.session_state.current_exam_q + 1,
            step=1,
            key="jump_input"
        )
    with col_b:
        if st.button("Go", key="jump_btn", use_container_width=True):
            st.session_state.current_exam_q = jump_to - 1
            st.rerun()
    
    st.markdown("---")
    
    # Current Question
    q_idx = st.session_state.current_exam_q
    q = st.session_state.exam_questions[q_idx]
    
    st.markdown(f"### Question {q_idx + 1} of {len(st.session_state.exam_questions)}")
    st.markdown(f"**Topic:** {q['topic']}")
    
    st.markdown(f"## {q['q']}")
    
    # Answer options
    current_answer = st.session_state.exam_answers.get(q_idx)
    
    answer = st.radio(
        "Select your answer:",
        options=range(len(q['options'])),
        format_func=lambda x: f"{chr(65+x)}) {q['options'][x]}",
        index=current_answer if current_answer is not None else None,
        key=f"exam_q_{q_idx}",
        label_visibility="collapsed"
    )
    
    if answer is not None:
        st.session_state.exam_answers[q_idx] = answer
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if q_idx > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_exam_q -= 1
                st.rerun()
    
    with col2:
        is_marked = q_idx in st.session_state.marked_questions
        if st.button("🔖 Unmark" if is_marked else "🔖 Mark", use_container_width=True):
            if is_marked:
                st.session_state.marked_questions.remove(q_idx)
            else:
                st.session_state.marked_questions.add(q_idx)
            st.rerun()
    
    with col3:
        if st.button("🔄 Clear Answer", use_container_width=True):
            if q_idx in st.session_state.exam_answers:
                del st.session_state.exam_answers[q_idx]
            st.rerun()
    
    with col4:
        if q_idx < len(st.session_state.exam_questions) - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_exam_q += 1
                st.rerun()
    
    with col5:
        if st.button("✅ Submit Exam", use_container_width=True, type="primary"):
            if len(st.session_state.exam_answers) < len(st.session_state.exam_questions):
                unanswered = len(st.session_state.exam_questions) - len(st.session_state.exam_answers)
                st.warning(f"⚠️ You have {unanswered} unanswered questions. Submit anyway?")
                if st.button("Yes, Submit", key="confirm_submit"):
                    st.session_state.exam_submitted = True
                    st.rerun()
            else:
                st.session_state.exam_submitted = True
                st.rerun()
    
    # Auto-refresh for timer (every second)
    time.sleep(1)
    st.rerun()

# ═══════════════════════════════════════════════════════
# EXAM RESULTS
# ═══════════════════════════════════════════════════════

else:
    # Calculate results
    correct = 0
    total = len(st.session_state.exam_questions)
    
    for i, q in enumerate(st.session_state.exam_questions):
        user_answer = st.session_state.exam_answers.get(i)
        if user_answer == q['correct']:
            correct += 1
    
    percentage = (correct / total) * 100 if total > 0 else 0
    passed = percentage >= 70
    
    # 🆕 Save to Data Manager (only once)
    if not st.session_state.reviewing_answers and not st.session_state.xp_awarded:
        try:
            # Save exam result
            record_exam_result(int(percentage), passed)
            
            # Award XP
            progress = load_progress()
            
            xp_earned = 50  # Base XP for taking exam
            
            if passed:
                xp_earned += 100  # Bonus for passing
                
                if percentage >= 90:
                    xp_earned += 50  # Excellence bonus
                elif percentage >= 80:
                    xp_earned += 25  # Good performance bonus
            
            progress['achievements']['xp_total'] += xp_earned
            progress['achievements']['level'] = (progress['achievements']['xp_total'] // 500) + 1
            
            save_progress(progress)
            
            # Check for new badges
            new_badges = check_and_award_badges()
            
            st.session_state.xp_awarded = True
            st.session_state.xp_amount = xp_earned
            st.session_state.new_badges = new_badges
            
        except Exception as e:
            st.warning(f"⚠️ Could not save result: {e}")
    
    # Results display
    if not st.session_state.reviewing_answers:
        
        # XP Notification
        if st.session_state.xp_awarded:
            st.markdown(f"""
            <div class="xp-notification">
                🎁 +{st.session_state.xp_amount} XP Earned!
            </div>
            """, unsafe_allow_html=True)
            
            # Show new badges
            if st.session_state.new_badges:
                cols = st.columns(len(st.session_state.new_badges))
                for idx, badge in enumerate(st.session_state.new_badges):
                    with cols[idx]:
                        st.success(f"🏆 New Badge: {badge}")
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h1>📊 Exam Results</h1>
            <div class="{'pass-badge' if passed else 'fail-badge'}">
                {'PASS ✅' if passed else 'FAIL ❌'}
            </div>
            <h1 style="font-size: 4rem; margin: 1rem 0;">
                {percentage:.1f}%
            </h1>
            <h2>{correct} out of {total} correct</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if passed:
            if percentage >= 90:
                st.success("🏆 Outstanding! You're exam ready!")
            else:
                st.success("✅ Congratulations! You passed!")
            st.balloons()
        else:
            st.error("❌ Keep practicing! Review the topics and try again.")
        
        # User Progress Stats
        try:
            stats = get_overall_stats()
            
            st.markdown("### 🎯 Your Overall Progress")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🌟 Total XP", stats['xp_total'])
            with col2:
                st.metric("📊 Level", stats['level'])
            with col3:
                st.metric("🔥 Study Streak", f"{stats['study_streak']} days")
            with col4:
                st.metric("🏆 Badges", len(stats['badges']))
        except:
            pass
        
        st.markdown("---")
        
        # Stats breakdown
        st.markdown("### 📈 Performance by Topic")
        
        topic_stats = {}
        for i, q in enumerate(st.session_state.exam_questions):
            topic = q['topic']
            if topic not in topic_stats:
                topic_stats[topic] = {'correct': 0, 'total': 0}
            topic_stats[topic]['total'] += 1
            if st.session_state.exam_answers.get(i) == q['correct']:
                topic_stats[topic]['correct'] += 1
        
        for topic, stats in sorted(topic_stats.items()):
            pct = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(pct / 100)
            with col2:
                st.markdown(f"**{topic}:** {stats['correct']}/{stats['total']} ({pct:.0f}%)")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Retake Exam", use_container_width=True):
                st.session_state.exam_started = False
                st.session_state.exam_submitted = False
                st.session_state.reviewing_answers = False
                st.session_state.xp_awarded = False
                st.rerun()
        
        with col2:
            if st.button("📖 Review Answers", use_container_width=True):
                st.session_state.reviewing_answers = True
                st.rerun()
        
        with col3:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("app.py")
    
    # Review mode
    else:
        st.markdown("## 📖 Answer Review")
        st.markdown("---")
        
        for i, q in enumerate(st.session_state.exam_questions):
            user_answer = st.session_state.exam_answers.get(i)
            is_correct = user_answer == q['correct']
            
            st.markdown(f"### Question {i+1}: {q['topic']}")
            st.markdown(f"**{q['q']}**")
            
            for idx, option in enumerate(q['options']):
                prefix = chr(65 + idx)
                
                if idx == q['correct']:
                    st.markdown(f"""
                    <div class="review-correct">
                        ✅ {prefix}) {option} <strong>(Correct Answer)</strong>
                    </div>
                    """, unsafe_allow_html=True)
                elif idx == user_answer and not is_correct:
                    st.markdown(f"""
                    <div class="review-wrong">
                        ❌ {prefix}) {option} <strong>(Your Answer)</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"{prefix}) {option}")
            
            st.info(f"📖 **Explanation:** {q['explanation']}")
            
            st.markdown("---")
        
        # Back button
        if st.button("⬅️ Back to Results", use_container_width=True):
            st.session_state.reviewing_answers = False
            st.rerun()

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>📝 <strong>Elshamy IWCF Mock Exam</strong> | Practice Makes Perfect</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        Created by Eng. Ahmed Elshamy | © 2026
    </p>
</div>
""", unsafe_allow_html=True)