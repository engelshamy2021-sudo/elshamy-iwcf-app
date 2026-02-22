import streamlit as st
import time
from datetime import datetime

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Scenarios - IWCF Mastery",
    page_icon="🎬",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .scenario-header {
        background: linear-gradient(135deg, #DC2626 0%, #F87171 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
    }
    
    .scenario-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #DC2626;
    }
    
    .situation-box {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #DC2626;
        margin: 1rem 0;
    }
    
    .data-box {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
    
    .question-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .correct-answer {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
    }
    
    .wrong-answer {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #EF4444;
        margin: 1rem 0;
    }
    
    .step-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #7C3AED;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #DC2626;
    }
    
    .outcome-success {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .outcome-failure {
        background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .outcome-warning {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎬 SCENARIOS DATA
# ═══════════════════════════════════════════════════════

SCENARIOS = [
    {
        "id": 1,
        "title": "Kick Detection on Drilling Rig",
        "difficulty": "Easy",
        "category": "Kick Detection",
        "time_limit": 300,
        "situation": "You are the Driller on a drilling rig. Current Depth: 10,000 ft TVD, Mud Weight: 10.5 ppg. You are drilling ahead at normal ROP. Suddenly, you notice: Pit level increased by 10 bbls, Pump pressure decreased by 100 psi, Flow rate from the well increased.",
        "well_data": {
            "TVD": "10,000 ft",
            "MD": "10,500 ft",
            "Mud Weight": "10.5 ppg",
            "Pit Gain": "10 bbls",
            "Casing Shoe": "8,000 ft",
            "Previous SCR": "500 psi at 30 spm"
        },
        "questions": [
            {
                "question": "What is happening in this situation?",
                "options": [
                    "A) Lost circulation",
                    "B) Kick (influx into wellbore)",
                    "C) Pump failure",
                    "D) Normal drilling variation"
                ],
                "correct": 1,
                "explanation": "The combination of pit gain, pump pressure decrease, and flow rate increase are PRIMARY kick indicators. This is definitely a kick!"
            },
            {
                "question": "What should be your FIRST action?",
                "options": [
                    "A) Increase pump rate",
                    "B) Call the company man",
                    "C) Stop the pumps and pick up off bottom",
                    "D) Continue drilling and monitor"
                ],
                "correct": 2,
                "explanation": "The first action is ALWAYS: Stop pumps, pick up off bottom, then shut in the well. Never delay shutting in!"
            },
            {
                "question": "After shutting in, you record SIDPP = 400 psi and SICP = 550 psi. What does this tell you?",
                "options": [
                    "A) Gas kick (SICP > SIDPP)",
                    "B) Water kick",
                    "C) Equipment malfunction",
                    "D) Formation breakdown"
                ],
                "correct": 0,
                "explanation": "When SICP > SIDPP, it indicates gas in the annulus. Gas is lighter than mud, so less hydrostatic pressure, requiring more surface pressure to balance."
            },
            {
                "question": "Calculate the Kill Mud Weight (KMW):",
                "options": [
                    "A) 10.5 ppg",
                    "B) 11.0 ppg",
                    "C) 11.27 ppg",
                    "D) 12.0 ppg"
                ],
                "correct": 2,
                "explanation": "KMW = OMW + (SIDPP / (0.052 × TVD))\nKMW = 10.5 + (400 / (0.052 × 10,000))\nKMW = 10.5 + (400 / 520)\nKMW = 10.5 + 0.77 = 11.27 ppg"
            }
        ],
        "lessons_learned": [
            "Always monitor pit levels continuously",
            "React quickly to kick indicators",
            "Never hesitate to shut in",
            "Record pressures accurately for calculations"
        ]
    },
    {
        "id": 2,
        "title": "Choosing the Right Kill Method",
        "difficulty": "Medium",
        "category": "Kill Methods",
        "time_limit": 420,
        "situation": "You have successfully shut in the well after detecting a kick. SIDPP = 600 psi (stable), SICP = 750 psi (stable), Pit Gain = 15 bbls. Kill mud is NOT immediately available - mixing facilities will take 45 minutes to prepare KMW. Crew is relatively inexperienced. The company man asks you to recommend a kill method.",
        "well_data": {
            "TVD": "12,000 ft",
            "MD": "13,000 ft",
            "Current MW": "11.0 ppg",
            "SIDPP": "600 psi",
            "SICP": "750 psi",
            "Pit Gain": "15 bbls",
            "SCR": "550 psi at 30 spm",
            "Casing Shoe": "9,500 ft",
            "LOT at Shoe": "14.5 ppg EMW"
        },
        "questions": [
            {
                "question": "Which kill method would you recommend?",
                "options": [
                    "A) Wait & Weight Method",
                    "B) Driller's Method",
                    "C) Bullheading",
                    "D) Volumetric Method"
                ],
                "correct": 1,
                "explanation": "Driller's Method is best here because: 1) Kill mud is NOT ready (45 min wait), 2) Crew is inexperienced (simpler method), 3) Driller's allows immediate circulation, 4) Two circulations but starts immediately"
            },
            {
                "question": "Calculate the ICP (Initial Circulating Pressure):",
                "options": [
                    "A) 600 psi",
                    "B) 1,150 psi",
                    "C) 750 psi",
                    "D) 550 psi"
                ],
                "correct": 1,
                "explanation": "ICP = SIDPP + SCR\nICP = 600 + 550 = 1,150 psi"
            },
            {
                "question": "Calculate the Kill Mud Weight:",
                "options": [
                    "A) 11.5 ppg",
                    "B) 11.96 ppg",
                    "C) 12.5 ppg",
                    "D) 11.0 ppg"
                ],
                "correct": 1,
                "explanation": "KMW = OMW + (SIDPP / (0.052 × TVD))\nKMW = 11.0 + (600 / (0.052 × 12,000))\nKMW = 11.0 + (600 / 624) = 11.0 + 0.96 = 11.96 ppg"
            },
            {
                "question": "Calculate the FCP (Final Circulating Pressure):",
                "options": [
                    "A) 550 psi",
                    "B) 600 psi",
                    "C) 500 psi",
                    "D) 650 psi"
                ],
                "correct": 1,
                "explanation": "FCP = SCR × (KMW / OMW)\nFCP = 550 × (12.0 / 11.0) = 550 × 1.09 = 600 psi"
            },
            {
                "question": "In Driller's Method, when do you switch from ICP to FCP?",
                "options": [
                    "A) Immediately when you start pumping",
                    "B) When kill mud reaches the bit (2nd circulation)",
                    "C) At the end of first circulation",
                    "D) When kick is out of the annulus"
                ],
                "correct": 1,
                "explanation": "In Driller's Method: 1st circulation - Maintain ICP, then reduce to zero when kick is out. 2nd circulation - Start at ICP, reduce to FCP when KMW reaches bit."
            }
        ],
        "lessons_learned": [
            "Choose method based on: mud availability, crew experience, and well conditions",
            "Driller's Method is simpler but takes longer",
            "Always calculate ICP, FCP, and KMW before starting",
            "Document all calculations and get verification"
        ]
    },
    {
        "id": 3,
        "title": "Subsea Well Control Emergency",
        "difficulty": "Hard",
        "category": "Subsea Operations",
        "time_limit": 600,
        "situation": "You are working on a deepwater drilling rig in 5,000 ft of water. During drilling at 15,000 ft TVD, sudden pit gain of 20 bbls occurs. Flow with pumps off confirmed. Well has been shut in. Surface SIDPP = 800 psi, Surface SICP = 1,100 psi. Choke Line Friction (CLF) at kill rate is 200 psi.",
        "well_data": {
            "Water Depth": "5,000 ft",
            "TVD": "15,000 ft",
            "RKB to Mudline": "5,100 ft",
            "Current MW": "12.0 ppg",
            "Surface SIDPP": "800 psi",
            "Surface SICP": "1,100 psi",
            "CLF": "200 psi",
            "SCR": "700 psi at 25 spm",
            "Seawater Gradient": "0.445 psi/ft",
            "MAASP": "1,400 psi"
        },
        "questions": [
            {
                "question": "What is the TRUE SICP (corrected for CLF)?",
                "options": [
                    "A) 1,100 psi",
                    "B) 1,300 psi",
                    "C) 900 psi",
                    "D) 1,500 psi"
                ],
                "correct": 1,
                "explanation": "True SICP = Surface SICP + CLF\nTrue SICP = 1,100 + 200 = 1,300 psi\n\nIn subsea, always ADD CLF to get true pressure!"
            },
            {
                "question": "Is the current SICP within safe limits?",
                "options": [
                    "A) Yes, 1,100 psi < MAASP (1,400 psi)",
                    "B) No, True SICP (1,300 psi) is close to MAASP",
                    "C) Cannot determine",
                    "D) MAASP doesn't apply to subsea"
                ],
                "correct": 1,
                "explanation": "True SICP = 1,300 psi, MAASP = 1,400 psi. Only 100 psi margin! Very close to limit. Must be very careful during circulation."
            },
            {
                "question": "Calculate the Kill Mud Weight:",
                "options": [
                    "A) 12.5 ppg",
                    "B) 13.0 ppg",
                    "C) 13.03 ppg",
                    "D) 12.8 ppg"
                ],
                "correct": 2,
                "explanation": "KMW = OMW + (SIDPP / (0.052 × TVD))\nKMW = 12.0 + (800 / (0.052 × 15,000))\nKMW = 12.0 + (800 / 780) = 12.0 + 1.03 = 13.03 ppg"
            },
            {
                "question": "What special consideration applies to subsea well control?",
                "options": [
                    "A) Use higher pump rates",
                    "B) Ignore the choke line",
                    "C) Account for CLF and monitor MAASP closely",
                    "D) Wait for better weather"
                ],
                "correct": 2,
                "explanation": "Subsea well control requires: 1) Adding CLF to all casing pressure readings, 2) Careful MAASP monitoring, 3) Riser margin consideration, 4) Emergency disconnect procedures ready"
            },
            {
                "question": "If you need to disconnect in emergency, what happens to the well?",
                "options": [
                    "A) Well flows uncontrolled",
                    "B) BOP remains on seabed, well stays shut in",
                    "C) Well collapses",
                    "D) Mud falls out of riser"
                ],
                "correct": 1,
                "explanation": "In emergency disconnect: 1) LMRP disconnects from BOP, 2) BOP stays on seabed, 3) Well remains SHUT IN by BOP, 4) Rig moves away safely, 5) Return later to reconnect and kill well"
            }
        ],
        "lessons_learned": [
            "Always add CLF to surface casing pressure readings",
            "Monitor MAASP closely - margins are tighter in subsea",
            "Prepare emergency disconnect procedures",
            "Consider riser margin when planning mud weights",
            "Subsea adds complexity - take extra care with calculations"
        ]
    },
    {
        "id": 4,
        "title": "BOP Failure During Kill Operation",
        "difficulty": "Hard",
        "category": "Emergency Procedures",
        "time_limit": 480,
        "situation": "You are in the middle of killing a well using Driller's Method. First circulation is 50% complete when suddenly: Annular preventer starts leaking, Pressure is escaping around the annular element, SICP is rising uncontrollably, Pipe rams are available but well has tool joint across rams.",
        "well_data": {
            "TVD": "11,000 ft",
            "Current MW": "10.0 ppg",
            "KMW": "11.0 ppg",
            "SIDPP before leak": "500 psi",
            "Current Casing Pressure": "Rising - 800 psi and increasing",
            "String Position": "Tool joint across pipe rams",
            "Annular Status": "Leaking",
            "Pipe Rams": "Available",
            "Blind Rams": "Available"
        },
        "questions": [
            {
                "question": "What is the FIRST thing you should try?",
                "options": [
                    "A) Close blind rams immediately",
                    "B) Increase annular closing pressure",
                    "C) Space out to put pipe body across rams, then close pipe rams",
                    "D) Shut down and evacuate"
                ],
                "correct": 2,
                "explanation": "First action: Space out the string to position pipe body (not tool joint) across the pipe rams, then close pipe rams. Closing rams on tool joint can damage rams and create worse leak!"
            },
            {
                "question": "If spacing out is not possible, what is your backup?",
                "options": [
                    "A) Accept the leak",
                    "B) Use VBR (Variable Bore Rams) if available",
                    "C) Increase annular pressure to maximum",
                    "D) Both B and C"
                ],
                "correct": 3,
                "explanation": "Backup options: 1) Try increasing annular closing pressure (may reseal), 2) Use VBR if available (can close on different sizes), 3) Consider pipe rams on smaller pipe section, 4) Last resort: Shear rams"
            },
            {
                "question": "Pipe rams are now closed. Pressure is stable. What next?",
                "options": [
                    "A) Resume kill operation immediately",
                    "B) Check pressures, verify seal, then resume cautiously",
                    "C) Pull out of hole",
                    "D) Wait 24 hours"
                ],
                "correct": 1,
                "explanation": "After securing the well: 1) Verify seal is holding (pressure stable), 2) Record new SIDPP and SICP, 3) Verify nothing changed in wellbore, 4) Resume kill operation cautiously, 5) Monitor closely for further issues"
            },
            {
                "question": "When would you use Shear Rams?",
                "options": [
                    "A) As first option for any leak",
                    "B) When you want to trip out",
                    "C) Only as LAST RESORT when all else fails",
                    "D) During normal BOP tests"
                ],
                "correct": 2,
                "explanation": "Shear Rams = LAST RESORT ONLY! They CUT the pipe! Expensive ($$$). May damage BOP. Use ONLY when: All other options exhausted, Imminent blowout risk, Emergency well abandonment"
            }
        ],
        "lessons_learned": [
            "Know your BOP stack configuration",
            "Always track string position relative to rams",
            "Space out procedure is critical",
            "Have backup plans ready before starting kill",
            "Shear rams are LAST RESORT only"
        ]
    },
    {
        "id": 5,
        "title": "Lost Circulation During Kill",
        "difficulty": "Hard",
        "category": "Complications",
        "time_limit": 540,
        "situation": "You are performing Wait & Weight Method to kill a well. Kill mud (12.5 ppg) is entering the annulus. Suddenly: Pit level starts DROPPING, Pump pressure decreasing, Flow out is less than flow in, Current choke pressure: 400 psi. You suspect lost circulation has started.",
        "well_data": {
            "TVD": "13,000 ft",
            "Casing Shoe": "10,000 ft",
            "LOT at Shoe": "14.0 ppg EMW",
            "Original MW": "11.0 ppg",
            "KMW": "12.5 ppg",
            "Current Position": "KMW 30% into annulus",
            "Pit Loss Rate": "5 bbl/min",
            "MAASP": "1,200 psi"
        },
        "questions": [
            {
                "question": "What is likely happening?",
                "options": [
                    "A) Formation taking fluid (lost circulation)",
                    "B) Another kick occurring",
                    "C) Pump failure",
                    "D) Choke plugged"
                ],
                "correct": 0,
                "explanation": "Signs of Lost Circulation: Pit level DROPPING, Flow out < Flow in, Pump pressure decreasing. The heavier KMW may have exceeded formation strength at a weak point."
            },
            {
                "question": "What is your immediate action?",
                "options": [
                    "A) Increase pump rate to fill hole faster",
                    "B) Stop pumping and assess the situation",
                    "C) Continue pumping - losses are normal",
                    "D) Open the choke fully"
                ],
                "correct": 1,
                "explanation": "STOP PUMPING immediately! Assess: 1) How much is being lost? 2) Is the well still secure? 3) Can we continue with lighter mud? 4) Need LCM (Lost Circulation Material)?"
            },
            {
                "question": "If losses continue, what technique might help?",
                "options": [
                    "A) Increase mud weight more",
                    "B) Use Concurrent Method with lighter mud",
                    "C) Pump faster",
                    "D) Close BOP tighter"
                ],
                "correct": 1,
                "explanation": "Options for lost circulation during kill: 1) Concurrent Method - start with lighter mud, increase gradually, 2) Add LCM to seal losses, 3) Reduce pump rate, 4) Consider lower KMW with more circulations. Balance: Control kick vs. Don't break formation"
            },
            {
                "question": "What is the danger of continuing with heavy losses?",
                "options": [
                    "A) Underground blowout",
                    "B) Just losing expensive mud",
                    "C) No danger",
                    "D) Pump damage"
                ],
                "correct": 0,
                "explanation": "UNDERGROUND BLOWOUT RISK! If losses continue: Hydrostatic pressure drops, Kick can get larger, Flow may go from formation to loss zone. This is one of the worst scenarios in well control."
            }
        ],
        "lessons_learned": [
            "Monitor pit level CONTINUOUSLY during kill",
            "Know your weak points (shoe, depleted zones)",
            "Have LCM ready before starting kill",
            "Balance kick control vs. formation strength",
            "Underground blowout is a critical risk"
        ]
    }
]

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None

if 'scenario_step' not in st.session_state:
    st.session_state.scenario_step = 0

if 'scenario_answers' not in st.session_state:
    st.session_state.scenario_answers = []

if 'scenario_score' not in st.session_state:
    st.session_state.scenario_score = 0

if 'completed_scenarios' not in st.session_state:
    st.session_state.completed_scenarios = []

if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False

if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="scenario-header">
    <h1>🎬 Real-World Scenarios</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Practice decision-making with realistic well control situations
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Think fast, act right - Your choices matter!
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 STATS
# ═══════════════════════════════════════════════════════

total_scenarios = len(SCENARIOS)
completed_count = len(st.session_state.completed_scenarios)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #DC2626; margin: 0;">🎬 {total_scenarios}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Total Scenarios</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #10B981; margin: 0;">✅ {completed_count}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Completed</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_score = 0
    if st.session_state.completed_scenarios:
        avg_score = sum(s.get('score', 0) for s in st.session_state.completed_scenarios) / len(st.session_state.completed_scenarios)
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #F59E0B; margin: 0;">🎯 {avg_score:.0f}%</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Avg Score</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    mastery = (completed_count / total_scenarios * 100) if total_scenarios > 0 else 0
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #7C3AED; margin: 0;">📈 {mastery:.0f}%</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Progress</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📋 SCENARIO LIST
# ═══════════════════════════════════════════════════════

if st.session_state.current_scenario is None:
    st.markdown("## 📋 Available Scenarios")
    st.markdown("*Select a scenario to start the simulation*")
    
    # Filter
    col1, col2 = st.columns([2, 1])
    with col1:
        filter_difficulty = st.selectbox("Filter by difficulty:", ["All", "Easy", "Medium", "Hard"])
    with col2:
        categories = ["All"] + list(set(s['category'] for s in SCENARIOS))
        filter_category = st.selectbox("Filter by category:", categories)
    
    # Display scenarios
    for scenario in SCENARIOS:
        # Apply filters
        if filter_difficulty != "All" and scenario['difficulty'] != filter_difficulty:
            continue
        if filter_category != "All" and scenario['category'] != filter_category:
            continue
        
        is_completed = scenario['id'] in [s.get('id') for s in st.session_state.completed_scenarios]
        
        # Difficulty colors
        if scenario['difficulty'] == "Easy":
            diff_bg = "#D1FAE5"
            diff_color = "#065F46"
        elif scenario['difficulty'] == "Medium":
            diff_bg = "#FEF3C7"
            diff_color = "#92400E"
        else:
            diff_bg = "#FEE2E2"
            diff_color = "#991B1B"
        
        st.markdown(f"### 🎬 {scenario['title']}")
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"**Category:** {scenario['category']}")
            st.write(f"**Questions:** {len(scenario['questions'])} decisions")
        
        with col2:
            st.markdown(f"""
            <span style="background: {diff_bg}; color: {diff_color}; padding: 0.3rem 0.8rem; 
                        border-radius: 12px; font-weight: 600;">{scenario['difficulty']}</span>
            """, unsafe_allow_html=True)
        
        with col3:
            st.write(f"⏱️ {scenario['time_limit'] // 60} min")
        
        with col4:
            if is_completed:
                st.success("✅ Completed")
        
        if st.button(
            f"🚀 {'Retry' if is_completed else 'Start'} Scenario", 
            key=f"start_{scenario['id']}", 
            use_container_width=True
        ):
            st.session_state.current_scenario = scenario
            st.session_state.scenario_step = 0
            st.session_state.scenario_answers = []
            st.session_state.scenario_score = 0
            st.session_state.show_explanation = False
            st.session_state.selected_answer = None
            st.rerun()
        
        st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎮 SCENARIO GAMEPLAY
# ═══════════════════════════════════════════════════════

else:
    scenario = st.session_state.current_scenario
    questions = scenario['questions']
    current_step = st.session_state.scenario_step
    
    # Back button
    if st.button("← Exit Scenario"):
        st.session_state.current_scenario = None
        st.session_state.scenario_step = 0
        st.session_state.scenario_answers = []
        st.session_state.show_explanation = False
        st.rerun()
    
    # Progress bar
    progress = ((current_step) / len(questions)) * 100
    st.progress(progress / 100)
    st.write(f"**Step {min(current_step + 1, len(questions))} of {len(questions)}**")
    
    st.markdown(f"## 🎬 {scenario['title']}")
    
    # Situation & Well Data
    with st.expander("📋 Situation & Well Data", expanded=(current_step == 0)):
        st.markdown(f"""
        <div class="situation-box">
            <h4>🚨 Situation:</h4>
            <p>{scenario['situation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📊 Well Data:**")
        data_cols = st.columns(3)
        data_items = list(scenario['well_data'].items())
        for idx, (key, value) in enumerate(data_items):
            with data_cols[idx % 3]:
                st.info(f"**{key}:** {value}")
    
    st.markdown("---")
    
    # Current question
    if current_step < len(questions):
        question_data = questions[current_step]
        
        st.markdown(f"""
        <div class="question-box">
            <h3>❓ Decision {current_step + 1}:</h3>
            <p style="font-size: 1.2rem;">{question_data['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer options
        if not st.session_state.show_explanation:
            st.markdown("### Choose your answer:")
            
            for idx, option in enumerate(question_data['options']):
                if st.button(option, key=f"option_{idx}", use_container_width=True):
                    st.session_state.selected_answer = idx
                    st.session_state.show_explanation = True
                    
                    if idx == question_data['correct']:
                        st.session_state.scenario_score += 1
                    
                    st.session_state.scenario_answers.append({
                        'question': question_data['question'],
                        'selected': idx,
                        'correct': question_data['correct'],
                        'is_correct': idx == question_data['correct']
                    })
                    
                    st.rerun()
        
        else:
            # Show result
            is_correct = st.session_state.selected_answer == question_data['correct']
            
            if is_correct:
                st.markdown(f"""
                <div class="correct-answer">
                    <h3>✅ Correct!</h3>
                    <p>Great decision! You chose the right action.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                correct_option = question_data['options'][question_data['correct']]
                st.markdown(f"""
                <div class="wrong-answer">
                    <h3>❌ Not quite right</h3>
                    <p>The correct answer was: <strong>{correct_option}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Explanation
            st.markdown(f"""
            <div class="data-box">
                <h4>📚 Explanation:</h4>
                <p>{question_data['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Next button
            if current_step < len(questions) - 1:
                if st.button("➡️ Next Decision", use_container_width=True, type="primary"):
                    st.session_state.scenario_step += 1
                    st.session_state.show_explanation = False
                    st.session_state.selected_answer = None
                    st.rerun()
            else:
                if st.button("🏁 See Final Results", use_container_width=True, type="primary"):
                    st.session_state.scenario_step += 1
                    st.rerun()
    
    # Final results
    else:
        score_percentage = (st.session_state.scenario_score / len(questions)) * 100
        
        if score_percentage >= 80:
            st.markdown(f"""
            <div class="outcome-success">
                <h2>🎉 Excellent Performance!</h2>
                <p style="font-size: 2rem; margin: 1rem 0;">{st.session_state.scenario_score}/{len(questions)} correct ({score_percentage:.0f}%)</p>
                <p>You handled this emergency like a pro! 💪</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        elif score_percentage >= 60:
            st.markdown(f"""
            <div class="outcome-warning">
                <h2>👍 Good Job!</h2>
                <p style="font-size: 2rem; margin: 1rem 0;">{st.session_state.scenario_score}/{len(questions)} correct ({score_percentage:.0f}%)</p>
                <p>Room for improvement, but solid performance!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="outcome-failure">
                <h2>📚 Keep Learning!</h2>
                <p style="font-size: 2rem; margin: 1rem 0;">{st.session_state.scenario_score}/{len(questions)} correct ({score_percentage:.0f}%)</p>
                <p>Review the material and try again. You'll get better!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Lessons learned
        st.markdown("### 📝 Key Lessons from this Scenario:")
        for lesson in scenario['lessons_learned']:
            st.markdown(f"""
            <div class="step-box">
                ✅ {lesson}
            </div>
            """, unsafe_allow_html=True)
        
        # Save completion
        completion_record = {
            'id': scenario['id'],
            'title': scenario['title'],
            'score': score_percentage,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        existing_ids = [s.get('id') for s in st.session_state.completed_scenarios]
        if scenario['id'] in existing_ids:
            for s in st.session_state.completed_scenarios:
                if s.get('id') == scenario['id']:
                    s.update(completion_record)
                    break
        else:
            st.session_state.completed_scenarios.append(completion_record)
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Retry Scenario", use_container_width=True):
                st.session_state.scenario_step = 0
                st.session_state.scenario_answers = []
                st.session_state.scenario_score = 0
                st.session_state.show_explanation = False
                st.session_state.selected_answer = None
                st.rerun()
        
        with col2:
            if st.button("📋 Back to Scenarios", use_container_width=True):
                st.session_state.current_scenario = None
                st.rerun()

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        🎬 <strong>Elshamy IWCF Mastery Method™ - Scenarios</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Experience is the best teacher - practice makes perfect" 🎯
    </p>
</div>
""", unsafe_allow_html=True)