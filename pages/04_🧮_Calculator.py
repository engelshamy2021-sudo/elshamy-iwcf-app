"""
🧮 ELSHAMY IWCF - Calculation Center
Complete IWCF calculations with step-by-step solutions
With History & Export Features
"""

import streamlit as st
import math
from datetime import datetime

# ═══════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Calculator - Elshamy IWCF",
    page_icon="🧮",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 💾 CALCULATION HISTORY FUNCTIONS
# ═══════════════════════════════════════════════════════

def init_calc_history():
    """Initialize calculation history"""
    if 'calc_history' not in st.session_state:
        st.session_state.calc_history = []


def save_calculation(calc_type, inputs, result, formula=""):
    """Save calculation to session history"""
    init_calc_history()
    
    entry = {
        'type': calc_type,
        'inputs': inputs,
        'result': result,
        'formula': formula,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.session_state.calc_history.insert(0, entry)
    
    # Keep only last 50 calculations
    if len(st.session_state.calc_history) > 50:
        st.session_state.calc_history = st.session_state.calc_history[:50]


def clear_history():
    """Clear calculation history"""
    st.session_state.calc_history = []


def export_history_text():
    """Export history as text"""
    if 'calc_history' not in st.session_state or not st.session_state.calc_history:
        return ""
    
    lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║       ELSHAMY IWCF - CALCULATION HISTORY                    ║",
        "║       Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "                      ║",
        "╚══════════════════════════════════════════════════════════════╝",
        ""
    ]
    
    for idx, calc in enumerate(st.session_state.calc_history, 1):
        lines.append(f"━━━ Calculation #{idx} ━━━")
        lines.append(f"📊 Type: {calc['type']}")
        lines.append(f"⏰ Time: {calc['timestamp']}")
        if calc.get('formula'):
            lines.append(f"📐 Formula: {calc['formula']}")
        lines.append("📝 Inputs:")
        for key, val in calc['inputs'].items():
            lines.append(f"   • {key}: {val}")
        lines.append(f"✅ Result: {calc['result']}")
        lines.append("")
    
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("Created by Eng. Ahmed Elshamy | Elshamy IWCF Mastery System™")
    
    return "\n".join(lines)

# Initialize history
init_calc_history()

# ═══════════════════════════════════════════════════════
# التصميم
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .calc-header {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    
    .result-box {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
        animation: fadeIn 0.5s ease;
    }
    
    .formula-box {
        background: #F3F4F6;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #8B5CF6;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
    }
    
    .step-box {
        background: #DBEAFE;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #3B82F6;
    }
    
    .warning-box {
        background: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .history-item {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #8B5CF6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .saved-badge {
        background: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="calc-header">
    <h1>🧮 IWCF Calculation Center</h1>
    <p>Solve any well control calculation with step-by-step solutions</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# SIDEBAR - Calculator Selection & History
# ═══════════════════════════════════════════════════════

st.sidebar.markdown("## 🧮 Select Calculator")

calc_categories = {
    "📊 Pressure Calculations": [
        "Hydrostatic Pressure (HP)",
        "Formation Pressure (FP)",
        "Kill Mud Weight (KMW)",
        "ECD Calculation",
        "MAASP Calculation"
    ],
    "⚡ Kill Sheet Calculations": [
        "ICP & FCP",
        "Pressure Schedule",
        "Strokes to Bit"
    ],
    "📐 Volume Calculations": [
        "Annular Volume",
        "Pipe Volume",
        "Displacement"
    ],
    "🔄 Time & Strokes": [
        "Strokes Calculation",
        "Circulation Time",
        "Trip Speed"
    ],
    "🌊 Gas Behavior": [
        "Boyle's Law (Gas Expansion)",
        "Gas Migration"
    ],
    "🔀 Conversions": [
        "Unit Conversions"
    ]
}

selected_category = st.sidebar.selectbox("Category:", list(calc_categories.keys()))
calc_type = st.sidebar.radio("Calculator:", calc_categories[selected_category])

# ═══════════════════════════════════════════════════════
# SIDEBAR - History Section
# ═══════════════════════════════════════════════════════

st.sidebar.markdown("---")
st.sidebar.markdown("### 📜 Calculation History")

if st.session_state.calc_history:
    st.sidebar.caption(f"📊 {len(st.session_state.calc_history)} calculations saved")
    
    # Show last 5 calculations
    for idx, calc in enumerate(st.session_state.calc_history[:5]):
        with st.sidebar.expander(f"🔢 {calc['type'][:20]}...", expanded=False):
            st.caption(f"⏰ {calc['timestamp']}")
            for key, val in calc['inputs'].items():
                st.text(f"{key}: {val}")
            st.success(f"✅ {calc['result']}")
    
    # Export & Clear buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        export_text = export_history_text()
        st.download_button(
            label="📥 Export",
            data=export_text,
            file_name=f"IWCF_Calcs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_history()
            st.rerun()
else:
    st.sidebar.info("No calculations yet. Start calculating!")

st.sidebar.markdown("---")

# Quick Reference in Sidebar
st.sidebar.markdown("### 📚 Quick Reference")
st.sidebar.markdown("""
**Key Constants:**
- **0.052** = MW to gradient
- **1029.4** = Volume constant
- **0.433** = Water gradient
- **14.5** = psi to bar
""")

# ═══════════════════════════════════════════════════════
# CALCULATOR 1: Hydrostatic Pressure
# ═══════════════════════════════════════════════════════

if "Hydrostatic Pressure" in calc_type:
    st.markdown("## 📊 Hydrostatic Pressure Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>HP = 0.052 × MW × TVD</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        calc_mode = st.radio(
            "What do you want to calculate?",
            ["Calculate HP", "Calculate MW", "Calculate TVD"],
            horizontal=True
        )
        
        if calc_mode == "Calculate HP":
            mw = st.number_input("Mud Weight (ppg):", 0.0, 25.0, 10.0, 0.1)
            tvd = st.number_input("TVD (ft):", 0, 40000, 10000, 100)
            
            if st.button("🧮 Calculate HP", type="primary", use_container_width=True):
                hp = 0.052 * mw * tvd
                
                # Save to history
                save_calculation(
                    calc_type="Hydrostatic Pressure",
                    inputs={"MW": f"{mw} ppg", "TVD": f"{tvd:,} ft"},
                    result=f"{hp:,.2f} psi",
                    formula="HP = 0.052 × MW × TVD"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    HP = {hp:,.2f} psi
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    <strong>Step 1:</strong> HP = 0.052 × MW × TVD<br>
                    <strong>Step 2:</strong> HP = 0.052 × {mw} × {tvd:,}<br>
                    <strong>Step 3:</strong> HP = {0.052 * mw:.4f} × {tvd:,}<br>
                    <strong>Result:</strong> HP = <strong>{hp:,.2f} psi</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"""
                **Additional Info:**
                - Gradient: {0.052 * mw:.4f} psi/ft
                - Per 1000 ft: {hp/tvd*1000:.2f} psi
                - In bar: {hp/14.5:.2f} bar
                - In kPa: {hp * 6.895:.0f} kPa
                """)
        
        elif calc_mode == "Calculate MW":
            hp = st.number_input("Target HP (psi):", 0, 20000, 5200, 100)
            tvd = st.number_input("TVD (ft):", 0, 40000, 10000, 100, key="tvd_mw")
            
            if st.button("🧮 Calculate MW", type="primary", use_container_width=True):
                if tvd > 0:
                    mw = hp / (0.052 * tvd)
                    
                    save_calculation(
                        calc_type="Mud Weight from HP",
                        inputs={"HP": f"{hp:,} psi", "TVD": f"{tvd:,} ft"},
                        result=f"{mw:.2f} ppg",
                        formula="MW = HP / (0.052 × TVD)"
                    )
                    
                    st.markdown(f"""
                    <div class="result-box">
                        MW = {mw:.2f} ppg
                    </div>
                    <span class="saved-badge">✓ Saved to History</span>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="step-box">
                        <strong>Formula:</strong> MW = HP / (0.052 × TVD)<br>
                        <strong>Calculation:</strong> MW = {hp:,} / (0.052 × {tvd:,})<br>
                        <strong>Result:</strong> MW = <strong>{mw:.2f} ppg</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("TVD must be greater than 0")
        
        else:  # Calculate TVD
            hp = st.number_input("HP (psi):", 0, 20000, 5200, 100, key="hp_tvd")
            mw = st.number_input("MW (ppg):", 0.0, 25.0, 10.0, 0.1, key="mw_tvd")
            
            if st.button("🧮 Calculate TVD", type="primary", use_container_width=True):
                if mw > 0:
                    tvd = hp / (0.052 * mw)
                    
                    save_calculation(
                        calc_type="TVD from HP",
                        inputs={"HP": f"{hp:,} psi", "MW": f"{mw} ppg"},
                        result=f"{tvd:,.0f} ft",
                        formula="TVD = HP / (0.052 × MW)"
                    )
                    
                    st.markdown(f"""
                    <div class="result-box">
                        TVD = {tvd:,.0f} ft
                    </div>
                    <span class="saved-badge">✓ Saved to History</span>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="step-box">
                        <strong>Formula:</strong> TVD = HP / (0.052 × MW)<br>
                        <strong>Calculation:</strong> TVD = {hp:,} / (0.052 × {mw})<br>
                        <strong>Result:</strong> TVD = <strong>{tvd:,.0f} ft</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("MW must be greater than 0")
    
    with col2:
        st.markdown("### 💡 Quick Reference")
        
        st.info("""
        **Common Values:**
        - 10 ppg at 10,000 ft = 5,200 psi
        - 12 ppg at 10,000 ft = 6,240 psi
        - 14 ppg at 10,000 ft = 7,280 psi
        - 16 ppg at 10,000 ft = 8,320 psi
        
        **Gradient Formula:**
        Gradient = 0.052 × MW
        - 10 ppg = 0.52 psi/ft
        - 12 ppg = 0.624 psi/ft
        - 14 ppg = 0.728 psi/ft
        """)
        
        st.warning("""
        **⚠️ Common Mistakes:**
        - Using MD instead of TVD
        - Forgetting 0.052 constant
        - Wrong mud weight units
        - Not accounting for gas-cut mud
        """)
        
        # Quick calc table
        st.markdown("### 📊 Quick Reference Table")
        st.markdown("""
        | MW (ppg) | HP at 10,000ft |
        |----------|----------------|
        | 9.0 | 4,680 psi |
        | 10.0 | 5,200 psi |
        | 11.0 | 5,720 psi |
        | 12.0 | 6,240 psi |
        | 13.0 | 6,760 psi |
        | 14.0 | 7,280 psi |
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 2: Formation Pressure
# ═══════════════════════════════════════════════════════

elif "Formation Pressure" in calc_type:
    st.markdown("## 📊 Formation Pressure Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>FP = HP + SIDPP = (0.052 × MW × TVD) + SIDPP</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        tvd = st.number_input("TVD (ft):", 0, 40000, 10000, 100)
        mw = st.number_input("Mud Weight (ppg):", 0.0, 25.0, 10.0, 0.1)
        sidpp = st.number_input("SIDPP (psi):", 0, 5000, 200, 10)
        
        if st.button("🧮 Calculate Formation Pressure", type="primary", use_container_width=True):
            hp = 0.052 * mw * tvd
            fp = hp + sidpp
            gradient = fp / tvd if tvd > 0 else 0
            equiv_mw = gradient / 0.052 if gradient > 0 else 0
            
            save_calculation(
                calc_type="Formation Pressure",
                inputs={
                    "TVD": f"{tvd:,} ft",
                    "MW": f"{mw} ppg",
                    "SIDPP": f"{sidpp} psi"
                },
                result=f"{fp:,.0f} psi ({equiv_mw:.2f} ppg EMW)",
                formula="FP = HP + SIDPP"
            )
            
            st.markdown(f"""
            <div class="result-box">
                Formation Pressure = {fp:,.0f} psi
            </div>
            <span class="saved-badge">✓ Saved to History</span>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="step-box">
                <strong>Step 1:</strong> Calculate HP<br>
                HP = 0.052 × {mw} × {tvd:,} = {hp:,.0f} psi<br><br>
                
                <strong>Step 2:</strong> Add SIDPP<br>
                FP = {hp:,.0f} + {sidpp} = <strong>{fp:,.0f} psi</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Determine pressure type
            if gradient > 0.6:
                pressure_type = "🔴 **High Abnormal Pressure!**"
                advice = "Use heavy mud and extreme caution!"
            elif gradient > 0.465:
                pressure_type = "🟡 **Abnormal Pressure**"
                advice = "Monitor closely, prepare for kill"
            elif gradient >= 0.43:
                pressure_type = "🟢 **Normal Pressure**"
                advice = "Standard operations applicable"
            else:
                pressure_type = "🔵 **Subnormal Pressure**"
                advice = "Watch for lost circulation"
            
            st.success(f"""
            **Formation Analysis:**
            - Formation Pressure: **{fp:,.0f} psi**
            - Formation Gradient: **{gradient:.4f} psi/ft**
            - Equivalent MW: **{equiv_mw:.2f} ppg**
            - Classification: {pressure_type}
            - Advice: {advice}
            """)
    
    with col2:
        st.markdown("### 💡 Pressure Gradients")
        
        st.info("""
        **Normal Gradients:**
        - Fresh water: 0.433 psi/ft (8.33 ppg)
        - Salt water: 0.465 psi/ft (8.94 ppg)
        
        **Classification:**
        - **Subnormal:** < 0.433 psi/ft
        - **Normal:** 0.433-0.465 psi/ft
        - **Abnormal:** > 0.465 psi/ft
        - **High Abnormal:** > 0.6 psi/ft
        """)
        
        st.warning("""
        **⚠️ Important:**
        - SIDPP = direct reading of underbalance
        - Use SIDPP only (not SICP) for calculations
        - Wait for pressures to stabilize
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 3: Kill Mud Weight
# ═══════════════════════════════════════════════════════

elif "Kill Mud Weight" in calc_type:
    st.markdown("## 💧 Kill Mud Weight Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>KMW = OMW + [SIDPP / (0.052 × TVD)]</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        sidpp = st.number_input("SIDPP (psi):", 0, 5000, 400, 10)
        tvd = st.number_input("TVD (ft):", 0, 40000, 10000, 100)
        omw = st.number_input("Original MW (ppg):", 0.0, 25.0, 10.0, 0.1)
        safety_margin = st.slider("Safety Margin (ppg):", 0.0, 2.0, 0.5, 0.1)
        
        if st.button("🧮 Calculate KMW", type="primary", use_container_width=True):
            if tvd > 0:
                increase = sidpp / (0.052 * tvd)
                kmw = omw + increase
                kmw_with_safety = kmw + safety_margin
                fp = (0.052 * omw * tvd) + sidpp
                
                save_calculation(
                    calc_type="Kill Mud Weight",
                    inputs={
                        "SIDPP": f"{sidpp} psi",
                        "TVD": f"{tvd:,} ft",
                        "Original MW": f"{omw} ppg",
                        "Safety Margin": f"{safety_margin} ppg"
                    },
                    result=f"{kmw_with_safety:.2f} ppg (including safety)",
                    formula="KMW = OMW + [SIDPP / (0.052 × TVD)]"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    KMW = {kmw:.2f} ppg<br>
                    <span style="font-size: 1rem;">With safety: {kmw_with_safety:.2f} ppg</span>
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    <strong>Step 1:</strong> Calculate MW increase needed<br>
                    Increase = SIDPP / (0.052 × TVD)<br>
                    Increase = {sidpp} / (0.052 × {tvd:,})<br>
                    Increase = {sidpp} / {0.052 * tvd:.2f}<br>
                    Increase = <strong>{increase:.4f} ppg</strong><br><br>
                    
                    <strong>Step 2:</strong> Add to original MW<br>
                    KMW = {omw} + {increase:.4f}<br>
                    KMW = <strong>{kmw:.2f} ppg</strong><br><br>
                    
                    <strong>Step 3:</strong> Add safety margin<br>
                    Final KMW = {kmw:.2f} + {safety_margin}<br>
                    Final KMW = <strong>{kmw_with_safety:.2f} ppg</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"""
                **Kill Plan Summary:**
                - Original MW: {omw} ppg
                - Kill MW (calculated): {kmw:.2f} ppg
                - Recommended KMW: **{kmw_with_safety:.2f} ppg**
                - Formation Pressure: {fp:,.0f} psi
                - MW increase needed: {kmw_with_safety - omw:.2f} ppg
                - Barite needed (approx): {(kmw_with_safety - omw) * 15:.0f} lb/bbl
                """)
                
                if kmw_with_safety - omw > 3:
                    st.warning("⚠️ Large MW increase (>3 ppg)! Consider staged approach or watch for losses.")
                if kmw_with_safety > 18:
                    st.warning("⚠️ Very heavy mud required! Check hole stability and ECD.")
            else:
                st.error("TVD must be greater than 0")
    
    with col2:
        st.markdown("### 💡 Safety Margins")
        
        st.info("""
        **Typical Safety Margins:**
        - Normal operations: 0.3-0.5 ppg
        - High risk zones: 0.5-1.0 ppg
        - Uncertain data: 1.0-2.0 ppg
        
        **Why add safety?**
        - Pressure uncertainties
        - Gauge errors (±50-100 psi)
        - Temperature effects
        - Gas-cut mud correction
        """)
        
        st.warning("""
        **⚠️ Watch out for:**
        - Too high KMW → Losses/fractures
        - Too low KMW → Another kick
        - Balance is key!
        
        **Typical Barite:**
        - ~15 lb/bbl per 0.1 ppg increase
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 4: ECD
# ═══════════════════════════════════════════════════════

elif "ECD" in calc_type:
    st.markdown("## ⚡ ECD (Equivalent Circulating Density)")
    
    st.markdown("""
    <div class="formula-box">
        <strong>ECD = MW + [APL / (0.052 × TVD)]</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        mw = st.number_input("Static MW (ppg):", 0.0, 25.0, 12.0, 0.1)
        apl = st.number_input("Annular Pressure Loss (psi):", 0, 2000, 260, 10)
        tvd = st.number_input("TVD (ft):", 0, 40000, 10000, 100)
        
        if st.button("🧮 Calculate ECD", type="primary", use_container_width=True):
            if tvd > 0:
                increase = apl / (0.052 * tvd)
                ecd = mw + increase
                bhp_static = 0.052 * mw * tvd
                bhp_dynamic = 0.052 * ecd * tvd
                
                save_calculation(
                    calc_type="ECD",
                    inputs={
                        "Static MW": f"{mw} ppg",
                        "APL": f"{apl} psi",
                        "TVD": f"{tvd:,} ft"
                    },
                    result=f"{ecd:.2f} ppg (+{increase:.2f} ppg)",
                    formula="ECD = MW + [APL / (0.052 × TVD)]"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    ECD = {ecd:.2f} ppg
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    <strong>Step 1:</strong> Calculate ECD increase<br>
                    Increase = APL / (0.052 × TVD)<br>
                    Increase = {apl} / (0.052 × {tvd:,})<br>
                    Increase = {apl} / {0.052 * tvd:.2f}<br>
                    Increase = <strong>{increase:.4f} ppg</strong><br><br>
                    
                    <strong>Step 2:</strong> Add to static MW<br>
                    ECD = {mw} + {increase:.4f}<br>
                    ECD = <strong>{ecd:.2f} ppg</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"""
                **ECD Analysis:**
                - Static MW: {mw} ppg
                - Dynamic ECD: **{ecd:.2f} ppg**
                - Increase: {increase:.2f} ppg ({increase/mw*100:.1f}%)
                - BHP (static): {bhp_static:,.0f} psi
                - BHP (circulating): {bhp_dynamic:,.0f} psi
                - Additional BHP: {apl} psi
                """)
                
                if increase > 1.0:
                    st.warning("⚠️ High ECD increase (>1 ppg)! Risk of losses. Consider reducing pump rate.")
                if increase > 1.5:
                    st.error("❌ Very high ECD! May fracture formation. Reduce circulation rate immediately.")
            else:
                st.error("TVD must be greater than 0")
    
    with col2:
        st.markdown("### 💡 Understanding ECD")
        
        st.info("""
        **ECD is always > static MW** because:
        - Friction from circulation
        - Added pressure at bottom
        
        **ECD increases with:**
        - Higher pump rate ⬆️
        - Thicker mud (viscosity) ⬆️
        - Smaller annulus ⬆️
        - Longer sections ⬆️
        - Cuttings loading ⬆️
        """)
        
        st.success("""
        **To reduce ECD:**
        - Decrease pump rate ⬇️
        - Thin the mud ⬇️
        - Enlarge hole size ⬇️
        - Reduce string size ⬇️
        - Better hole cleaning ⬇️
        """)
        
        st.warning("""
        **Critical in narrow margins!**
        
        If: ECD > Fracture Gradient
        → Lost circulation
        → Underground blowout risk
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 5: MAASP
# ═══════════════════════════════════════════════════════

elif "MAASP" in calc_type:
    st.markdown("## 🔒 MAASP (Maximum Allowable Annular Surface Pressure)")
    
    st.markdown("""
    <div class="formula-box">
        <strong>MAASP = (LOT EMW - Current MW) × 0.052 × Shoe TVD</strong><br>
        or<br>
        <strong>MAASP = LOT Pressure - HP at Shoe</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        input_type = st.radio(
            "Input format:",
            ["LOT/FIT as EMW (ppg)", "LOT/FIT as Pressure (psi)"],
            horizontal=True
        )
        
        if input_type == "LOT/FIT as EMW (ppg)":
            lot_emw = st.number_input("LOT/FIT EMW (ppg):", 0.0, 25.0, 15.0, 0.1)
            shoe_tvd = st.number_input("Shoe TVD (ft):", 0, 40000, 5000, 100)
            current_mw = st.number_input("Current MW (ppg):", 0.0, 25.0, 12.0, 0.1)
            safety_factor = st.slider("Safety Factor:", 0.8, 1.0, 0.9, 0.05)
            
            if st.button("🧮 Calculate MAASP", type="primary", use_container_width=True):
                maasp = (lot_emw - current_mw) * 0.052 * shoe_tvd
                maasp_with_safety = maasp * safety_factor
                margin_ppg = lot_emw - current_mw
                
                save_calculation(
                    calc_type="MAASP",
                    inputs={
                        "LOT EMW": f"{lot_emw} ppg",
                        "Current MW": f"{current_mw} ppg",
                        "Shoe TVD": f"{shoe_tvd:,} ft",
                        "Safety Factor": f"{safety_factor*100:.0f}%"
                    },
                    result=f"{maasp_with_safety:,.0f} psi (working)",
                    formula="MAASP = (LOT - MW) × 0.052 × Shoe TVD"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    MAASP = {maasp:,.0f} psi<br>
                    <span style="font-size: 1rem;">Working ({safety_factor*100:.0f}%): {maasp_with_safety:,.0f} psi</span>
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    <strong>Formula:</strong> MAASP = (LOT EMW - Current MW) × 0.052 × Shoe TVD<br><br>
                    
                    MAASP = ({lot_emw} - {current_mw}) × 0.052 × {shoe_tvd:,}<br>
                    MAASP = {margin_ppg:.2f} × 0.052 × {shoe_tvd:,}<br>
                    MAASP = {margin_ppg:.2f} × {0.052 * shoe_tvd:.2f}<br>
                    MAASP = <strong>{maasp:,.0f} psi</strong><br><br>
                    
                    <strong>With {safety_factor*100:.0f}% safety factor:</strong><br>
                    Working MAASP = {maasp:,.0f} × {safety_factor}<br>
                    Working MAASP = <strong>{maasp_with_safety:,.0f} psi</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Assessment
                if maasp < 500:
                    st.error("❌ **Very Low MAASP!** High risk during kick. Consider setting deeper casing.")
                elif maasp < 1000:
                    st.warning("⚠️ **Low MAASP.** Careful pressure management required during kill.")
                else:
                    st.success("✅ **Adequate MAASP** for normal kill operations.")
                
                st.info(f"""
                **MAASP Summary:**
                - Available margin: {margin_ppg:.2f} ppg
                - Calculated MAASP: {maasp:,.0f} psi
                - Working MAASP: **{maasp_with_safety:,.0f} psi**
                - If SICP > MAASP: **STOP and assess!**
                """)
        
        else:  # Pressure input
            lot_pressure = st.number_input("LOT/FIT Pressure (psi):", 0, 20000, 8000, 100)
            shoe_tvd = st.number_input("Shoe TVD (ft):", 0, 40000, 5000, 100, key="shoe_psi")
            current_mw = st.number_input("Current MW (ppg):", 0.0, 25.0, 12.0, 0.1, key="mw_psi")
            safety_factor = st.slider("Safety Factor:", 0.8, 1.0, 0.9, 0.05, key="sf_psi")
            
            if st.button("🧮 Calculate MAASP", type="primary", use_container_width=True, key="calc_maasp_psi"):
                hp_at_shoe = 0.052 * current_mw * shoe_tvd
                maasp = lot_pressure - hp_at_shoe
                maasp_with_safety = maasp * safety_factor
                
                save_calculation(
                    calc_type="MAASP (from pressure)",
                    inputs={
                        "LOT Pressure": f"{lot_pressure:,} psi",
                        "Current MW": f"{current_mw} ppg",
                        "Shoe TVD": f"{shoe_tvd:,} ft"
                    },
                    result=f"{maasp_with_safety:,.0f} psi (working)",
                    formula="MAASP = LOT - HP at Shoe"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    MAASP = {maasp:,.0f} psi
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    <strong>Step 1:</strong> Calculate HP at shoe<br>
                    HP = 0.052 × {current_mw} × {shoe_tvd:,}<br>
                    HP = {hp_at_shoe:,.0f} psi<br><br>
                    
                    <strong>Step 2:</strong> Calculate MAASP<br>
                    MAASP = LOT - HP<br>
                    MAASP = {lot_pressure:,} - {hp_at_shoe:,.0f}<br>
                    MAASP = <strong>{maasp:,.0f} psi</strong><br><br>
                    
                    <strong>Working MAASP ({safety_factor*100:.0f}%):</strong> {maasp_with_safety:,.0f} psi
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💡 MAASP Guidelines")
        
        st.info("""
        **What is MAASP?**
        
        Maximum surface pressure before fracturing formation at casing shoe.
        
        **Critical during:**
        - Kick control operations
        - Pressure testing
        - Wait & Weight method
        """)
        
        st.warning("""
        **If SICP approaches MAASP:**
        - Reduce pump rate
        - Open choke carefully
        - Consider volumetric method
        
        **If SICP exceeds MAASP:**
        - Formation may fracture
        - Lost circulation risk
        - Underground blowout possible
        """)
        
        st.success("""
        **Best Practices:**
        - Always apply 10% safety
        - Recalculate with MW changes
        - Monitor continuously during kill
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 6: ICP & FCP
# ═══════════════════════════════════════════════════════

elif "ICP & FCP" in calc_type:
    st.markdown("## ⚡ ICP & FCP Calculator")
    
    tab1, tab2, tab3 = st.tabs(["📈 ICP Calculation", "📉 FCP Calculation", "📊 Both Together"])
    
    with tab1:
        st.markdown("### Initial Circulating Pressure (ICP)")
        
        st.markdown("""
        <div class="formula-box">
            <strong>ICP = SIDPP + SCR</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            sidpp_icp = st.number_input("SIDPP (psi):", 0, 5000, 400, 10, key="sidpp_icp")
            scr_icp = st.number_input("SCR Pressure (psi):", 0, 3000, 500, 10, key="scr_icp")
            
            if st.button("Calculate ICP", type="primary", use_container_width=True, key="calc_icp"):
                icp = sidpp_icp + scr_icp
                
                save_calculation(
                    calc_type="ICP",
                    inputs={"SIDPP": f"{sidpp_icp} psi", "SCR": f"{scr_icp} psi"},
                    result=f"{icp} psi",
                    formula="ICP = SIDPP + SCR"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    ICP = {icp} psi
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    ICP = SIDPP + SCR<br>
                    ICP = {sidpp_icp} + {scr_icp}<br>
                    ICP = <strong>{icp} psi</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.info("""
            **ICP is used:**
            - At START of kill operation
            - To maintain constant BHP
            - In both Driller's & W&W methods
            
            **Driller's Method:**
            Hold ICP constant during 1st circulation
            
            **W&W Method:**
            Start at ICP, reduce to FCP
            """)
    
    with tab2:
        st.markdown("### Final Circulating Pressure (FCP)")
        
        st.markdown("""
        <div class="formula-box">
            <strong>FCP = SCR × (KMW / OMW)</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            scr_fcp = st.number_input("SCR Pressure (psi):", 0, 3000, 500, 10, key="scr_fcp")
            kmw_fcp = st.number_input("Kill MW (ppg):", 0.0, 25.0, 10.5, 0.1, key="kmw_fcp")
            omw_fcp = st.number_input("Original MW (ppg):", 0.0, 25.0, 10.0, 0.1, key="omw_fcp")
            
            if st.button("Calculate FCP", type="primary", use_container_width=True, key="calc_fcp"):
                if omw_fcp > 0:
                    fcp = scr_fcp * (kmw_fcp / omw_fcp)
                    
                    save_calculation(
                        calc_type="FCP",
                        inputs={
                            "SCR": f"{scr_fcp} psi",
                            "KMW": f"{kmw_fcp} ppg",
                            "OMW": f"{omw_fcp} ppg"
                        },
                        result=f"{fcp:.0f} psi",
                        formula="FCP = SCR × (KMW / OMW)"
                    )
                    
                    st.markdown(f"""
                    <div class="result-box">
                        FCP = {fcp:.0f} psi
                    </div>
                    <span class="saved-badge">✓ Saved to History</span>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="step-box">
                        FCP = SCR × (KMW / OMW)<br>
                        FCP = {scr_fcp} × ({kmw_fcp} / {omw_fcp})<br>
                        FCP = {scr_fcp} × {kmw_fcp/omw_fcp:.4f}<br>
                        FCP = <strong>{fcp:.0f} psi</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Original MW must be > 0")
        
        with col2:
            st.info("""
            **FCP is reached when:**
            - Kill mud reaches the bit
            - Heavy mud fills drillstring
            
            **Then:**
            Hold FCP constant until kill mud reaches surface
            """)
    
    with tab3:
        st.markdown("### Complete ICP & FCP Calculation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sidpp_both = st.number_input("SIDPP (psi):", 0, 5000, 400, 10, key="sidpp_both")
            scr_both = st.number_input("SCR Pressure (psi):", 0, 3000, 500, 10, key="scr_both")
            kmw_both = st.number_input("Kill MW (ppg):", 0.0, 25.0, 10.5, 0.1, key="kmw_both")
            omw_both = st.number_input("Original MW (ppg):", 0.0, 25.0, 10.0, 0.1, key="omw_both")
            
            if st.button("🧮 Calculate Both", type="primary", use_container_width=True):
                if omw_both > 0:
                    icp = sidpp_both + scr_both
                    fcp = scr_both * (kmw_both / omw_both)
                    
                    save_calculation(
                        calc_type="ICP & FCP",
                        inputs={
                            "SIDPP": f"{sidpp_both} psi",
                            "SCR": f"{scr_both} psi",
                            "KMW": f"{kmw_both} ppg",
                            "OMW": f"{omw_both} ppg"
                        },
                        result=f"ICP: {icp} psi | FCP: {fcp:.0f} psi",
                        formula="ICP = SIDPP + SCR | FCP = SCR × (KMW/OMW)"
                    )
                    
                    st.markdown(f"""
                    <div class="result-box">
                        ICP = {icp} psi<br>
                        FCP = {fcp:.0f} psi
                    </div>
                    <span class="saved-badge">✓ Saved to History</span>
                    """, unsafe_allow_html=True)
                    
                    st.success(f"""
                    **Kill Sheet Summary:**
                    - **ICP:** {icp} psi (start pressure)
                    - **FCP:** {fcp:.0f} psi (when kill mud at bit)
                    - **Pressure drop:** {icp - fcp:.0f} psi
                    - **Drop %:** {(icp - fcp) / icp * 100:.1f}%
                    """)
        
        with col2:
            st.info("""
            **Kill Process:**
            
            1️⃣ Shut in well
            2️⃣ Record SIDPP, SICP
            3️⃣ Calculate KMW
            4️⃣ Calculate ICP & FCP
            5️⃣ Start pumping at ICP
            6️⃣ Reduce to FCP as kill mud fills string
            7️⃣ Hold FCP until surface
            """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 7: Pressure Schedule
# ═══════════════════════════════════════════════════════

elif "Pressure Schedule" in calc_type:
    st.markdown("## 📊 Pressure Schedule Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>Pressure at any point = ICP - [(ICP - FCP) × (Strokes / Total Strokes to Bit)]</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        icp = st.number_input("ICP (psi):", 0, 5000, 900, 10)
        fcp = st.number_input("FCP (psi):", 0, 5000, 550, 10)
        strokes_to_bit = st.number_input("Strokes to Bit:", 0, 20000, 4000, 100)
        num_intervals = st.slider("Number of intervals:", 4, 20, 10)
        
        if st.button("🧮 Generate Pressure Schedule", type="primary", use_container_width=True):
            if strokes_to_bit > 0:
                st.markdown("### 📋 Kill Sheet Pressure Schedule")
                
                # Calculate pressure drop per stroke
                pressure_drop_per_stroke = (icp - fcp) / strokes_to_bit
                
                # Generate schedule
                schedule_data = []
                for i in range(num_intervals + 1):
                    fraction = i / num_intervals
                    strokes = int(strokes_to_bit * fraction)
                    pressure = icp - ((icp - fcp) * fraction)
                    schedule_data.append({
                        'Interval': f"{fraction*100:.0f}%",
                        'Strokes': strokes,
                        'Pressure (psi)': round(pressure)
                    })
                
                # Save calculation
                save_calculation(
                    calc_type="Pressure Schedule",
                    inputs={
                        "ICP": f"{icp} psi",
                        "FCP": f"{fcp} psi",
                        "Strokes to Bit": f"{strokes_to_bit:,}"
                    },
                    result=f"Schedule: {icp} → {fcp} psi over {strokes_to_bit:,} strokes",
                    formula="Linear decrease from ICP to FCP"
                )
                
                # Display as table
                import pandas as pd
                df = pd.DataFrame(schedule_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Visual representation
                st.markdown("### 📈 Pressure Profile")
                
                import plotly.graph_objects as go
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[d['Strokes'] for d in schedule_data],
                    y=[d['Pressure (psi)'] for d in schedule_data],
                    mode='lines+markers',
                    name='Drillpipe Pressure',
                    line=dict(color='#8B5CF6', width=3),
                    marker=dict(size=10)
                ))
                
                fig.update_layout(
                    xaxis_title="Strokes",
                    yaxis_title="Pressure (psi)",
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.success(f"""
                **Schedule Summary:**
                - Start at: **{icp} psi** (ICP)
                - End at: **{fcp} psi** (FCP)
                - Total drop: **{icp - fcp} psi**
                - Drop per stroke: **{pressure_drop_per_stroke:.4f} psi/stk**
                - Drop per 100 strokes: **{pressure_drop_per_stroke * 100:.2f} psi**
                """)
                
                st.markdown('<span class="saved-badge">✓ Saved to History</span>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💡 Using the Schedule")
        
        st.info("""
        **Purpose:**
        Track drillpipe pressure during Wait & Weight kill
        
        **Key Points:**
        - Linear decrease ICP → FCP
        - Pressure at bit position = FCP
        - Hold FCP to surface
        """)
        
        st.warning("""
        **If pressure deviates:**
        
        **Too high:**
        - Open choke slightly
        - Check for plugging
        
        **Too low:**
        - Close choke slightly
        - Check pump speed
        
        **Large deviation:**
        - Stop and assess
        - Check for complications
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 8: Strokes to Bit
# ═══════════════════════════════════════════════════════

elif "Strokes to Bit" in calc_type:
    st.markdown("## 🔄 Strokes to Bit Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>Strokes = Pipe Volume (bbls) / Pump Output (bbl/stk)</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Step 1: Calculate Pipe Volume")
        
        # Add multiple sections
        num_sections = st.number_input("Number of pipe sections:", 1, 5, 2)
        
        total_volume = 0
        section_details = []
        
        for i in range(num_sections):
            with st.expander(f"Section {i+1}", expanded=(i==0)):
                col_a, col_b = st.columns(2)
                with col_a:
                    pipe_id = st.number_input(
                        f"Pipe ID (inches):",
                        0.0, 10.0, 4.276 if i == 0 else 3.0,
                        0.001,
                        format="%.3f",
                        key=f"id_{i}"
                    )
                with col_b:
                    pipe_length = st.number_input(
                        f"Length (ft):",
                        0, 40000, 10000 if i == 0 else 500,
                        100,
                        key=f"len_{i}"
                    )
                
                capacity = (pipe_id ** 2) / 1029.4
                volume = capacity * pipe_length
                total_volume += volume
                section_details.append({
                    'Section': f"Section {i+1}",
                    'ID': f"{pipe_id}\"",
                    'Length': f"{pipe_length:,} ft",
                    'Capacity': f"{capacity:.6f} bbl/ft",
                    'Volume': f"{volume:.2f} bbls"
                })
        
        st.markdown(f"**Total Pipe Volume: {total_volume:.2f} bbls**")
        
        st.markdown("### 📝 Step 2: Calculate Strokes")
        
        pump_output = st.number_input(
            "Pump Output (bbl/stk):",
            0.001, 1.0, 0.117, 0.001,
            format="%.3f"
        )
        
        if st.button("🧮 Calculate Strokes to Bit", type="primary", use_container_width=True):
            strokes = total_volume / pump_output
            
            save_calculation(
                calc_type="Strokes to Bit",
                inputs={
                    "Total Pipe Volume": f"{total_volume:.2f} bbls",
                    "Pump Output": f"{pump_output:.3f} bbl/stk"
                },
                result=f"{strokes:,.0f} strokes",
                formula="Strokes = Volume / Pump Output"
            )
            
            st.markdown(f"""
            <div class="result-box">
                Strokes to Bit = {strokes:,.0f}
            </div>
            <span class="saved-badge">✓ Saved to History</span>
            """, unsafe_allow_html=True)
            
            # Show section breakdown
            import pandas as pd
            df = pd.DataFrame(section_details)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown(f"""
            <div class="step-box">
                <strong>Calculation:</strong><br>
                Strokes = Total Volume / Pump Output<br>
                Strokes = {total_volume:.2f} / {pump_output:.3f}<br>
                Strokes = <strong>{strokes:,.0f}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Time estimates
            st.markdown("### ⏱️ Time Estimates")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("At 30 SPM", f"{strokes/30:.1f} min")
            with col_b:
                st.metric("At 40 SPM", f"{strokes/40:.1f} min")
            with col_c:
                st.metric("At 60 SPM", f"{strokes/60:.1f} min")
    
    with col2:
        st.markdown("### 💡 Common Pump Outputs")
        
        st.info("""
        **Triplex Pumps:**
        - 5" liner: 0.072 bbl/stk
        - 5½" liner: 0.087 bbl/stk
        - 6" liner: 0.104 bbl/stk
        - 6½" liner: 0.122 bbl/stk
        - 7" liner: 0.141 bbl/stk
        
        **Duplex Pumps:**
        - 6" liner: 0.112 bbl/stk
        - 6½" liner: 0.117 bbl/stk
        - 7" liner: 0.136 bbl/stk
        """)
        
        st.warning("""
        **Remember:**
        - Measure pump efficiency
        - Account for liner wear
        - Use actual calibration
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 9: Annular Volume
# ═══════════════════════════════════════════════════════

elif "Annular Volume" in calc_type:
    st.markdown("## 📐 Annular Volume Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>Capacity = (Hole ID² - Pipe OD²) / 1029.4 (bbl/ft)</strong><br>
        <strong>Volume = Capacity × Length</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Input Values")
        
        hole_id = st.number_input(
            "Hole/Casing ID (inches):",
            0.0, 36.0, 12.25, 0.25
        )
        
        pipe_od = st.number_input(
            "Pipe OD (inches):",
            0.0, 20.0, 5.0, 0.25
        )
        
        length = st.number_input(
            "Length (ft):",
            0, 40000, 10000, 100
        )
        
        if st.button("🧮 Calculate Annular Volume", type="primary", use_container_width=True):
            if hole_id > pipe_od:
                capacity = (hole_id**2 - pipe_od**2) / 1029.4
                volume = capacity * length
                volume_gal = volume * 42
                
                save_calculation(
                    calc_type="Annular Volume",
                    inputs={
                        "Hole ID": f"{hole_id}\"",
                        "Pipe OD": f"{pipe_od}\"",
                        "Length": f"{length:,} ft"
                    },
                    result=f"{volume:.2f} bbls",
                    formula="(ID² - OD²) / 1029.4 × Length"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    Annular Volume = {volume:.2f} bbls
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="step-box">
                    <strong>Step 1:</strong> Calculate capacity<br>
                    Capacity = (ID² - OD²) / 1029.4<br>
                    Capacity = ({hole_id}² - {pipe_od}²) / 1029.4<br>
                    Capacity = ({hole_id**2:.2f} - {pipe_od**2:.2f}) / 1029.4<br>
                    Capacity = <strong>{capacity:.6f} bbl/ft</strong><br><br>
                    
                    <strong>Step 2:</strong> Calculate volume<br>
                    Volume = {capacity:.6f} × {length:,}<br>
                    Volume = <strong>{volume:.2f} bbls</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"""
                **Volume Summary:**
                - Capacity: {capacity:.6f} bbl/ft
                - Total: **{volume:.2f} bbls**
                - In gallons: {volume_gal:,.0f} gal
                - Per 1000 ft: {capacity * 1000:.2f} bbls
                """)
            else:
                st.error("Hole ID must be greater than Pipe OD")
    
    with col2:
        st.markdown("### 💡 Common Values")
        
        st.info("""
        **Open Hole Annulus:**
        - 8½" × 5" DP = 0.0459 bbl/ft
        - 12¼" × 5" DP = 0.1215 bbl/ft
        - 17½" × 5" DP = 0.2731 bbl/ft
        
        **Cased Hole:**
        - 9⅝" csg × 5" DP = 0.0653 bbl/ft
        - 13⅜" csg × 5" DP = 0.1489 bbl/ft
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 10: Pipe Volume
# ═══════════════════════════════════════════════════════

elif "Pipe Volume" in calc_type:
    st.markdown("## 🔧 Pipe Volume Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>Capacity = ID² / 1029.4 (bbl/ft)</strong><br>
        <strong>Volume = Capacity × Length</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        pipe_id = st.number_input(
            "Pipe ID (inches):",
            0.0, 10.0, 4.276, 0.001,
            format="%.3f"
        )
        
        pipe_length = st.number_input(
            "Pipe Length (ft):",
            0, 40000, 10000, 100
        )
        
        if st.button("🧮 Calculate Pipe Volume", type="primary", use_container_width=True):
            capacity = (pipe_id ** 2) / 1029.4
            volume = capacity * pipe_length
            
            save_calculation(
                calc_type="Pipe Volume",
                inputs={
                    "Pipe ID": f"{pipe_id}\"",
                    "Length": f"{pipe_length:,} ft"
                },
                result=f"{volume:.2f} bbls",
                formula="ID² / 1029.4 × Length"
            )
            
            st.markdown(f"""
            <div class="result-box">
                Pipe Volume = {volume:.2f} bbls
            </div>
            <span class="saved-badge">✓ Saved to History</span>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="step-box">
                Capacity = {pipe_id}² / 1029.4 = <strong>{capacity:.6f} bbl/ft</strong><br>
                Volume = {capacity:.6f} × {pipe_length:,} = <strong>{volume:.2f} bbls</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.info("""
        **Common Pipe Capacities:**
        - 3½" DP: 0.0080 bbl/ft
        - 4" DP: 0.0119 bbl/ft
        - 4½" DP: 0.0142 bbl/ft
        - 5" DP: 0.0178 bbl/ft
        - 5½" DP: 0.0216 bbl/ft
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 11: Displacement
# ═══════════════════════════════════════════════════════

elif "Displacement" in calc_type:
    st.markdown("## ⚖️ Pipe Displacement Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>Displacement = (OD² - ID²) / 1029.4 (bbl/ft)</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        pipe_od = st.number_input("Pipe OD (inches):", 0.0, 20.0, 5.0, 0.25)
        pipe_id = st.number_input("Pipe ID (inches):", 0.0, 10.0, 4.276, 0.001, format="%.3f")
        length = st.number_input("Length (ft):", 0, 40000, 10000, 100)
        
        if st.button("🧮 Calculate Displacement", type="primary", use_container_width=True):
            if pipe_od > pipe_id:
                displacement = (pipe_od**2 - pipe_id**2) / 1029.4
                total = displacement * length
                
                save_calculation(
                    calc_type="Pipe Displacement",
                    inputs={
                        "OD": f"{pipe_od}\"",
                        "ID": f"{pipe_id}\"",
                        "Length": f"{length:,} ft"
                    },
                    result=f"{total:.2f} bbls",
                    formula="(OD² - ID²) / 1029.4 × Length"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    Displacement = {total:.2f} bbls
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.success(f"""
                **Displacement Summary:**
                - Per foot: {displacement:.6f} bbl/ft
                - Total: **{total:.2f} bbls**
                - When pulling out: Need {total:.2f} bbls mud
                """)
            else:
                st.error("OD must be greater than ID")
    
    with col2:
        st.info("""
        **What is Displacement?**
        
        Volume of steel in the pipe.
        
        **Pulling out:** Need this much mud to fill hole
        
        **Running in:** This much mud displaced out
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 12: Strokes Calculation
# ═══════════════════════════════════════════════════════

elif "Strokes Calculation" in calc_type:
    st.markdown("## 🔄 Strokes Calculator")
    
    st.markdown("""
    <div class="formula-box">
        <strong>Strokes = Volume (bbls) / Pump Output (bbl/stk)</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        volume = st.number_input("Volume to pump (bbls):", 0.0, 10000.0, 500.0, 10.0)
        pump_output = st.number_input("Pump output (bbl/stk):", 0.001, 1.0, 0.117, 0.001, format="%.3f")
        
        if st.button("🧮 Calculate Strokes", type="primary", use_container_width=True):
            strokes = volume / pump_output
            
            save_calculation(
                calc_type="Strokes",
                inputs={
                    "Volume": f"{volume:.2f} bbls",
                    "Pump Output": f"{pump_output:.3f} bbl/stk"
                },
                result=f"{strokes:,.0f} strokes",
                formula="Strokes = Volume / Pump Output"
            )
            
            st.markdown(f"""
            <div class="result-box">
                {strokes:,.0f} strokes
            </div>
            <span class="saved-badge">✓ Saved to History</span>
            """, unsafe_allow_html=True)
            
            # Time at different SPM
            st.markdown("### ⏱️ Time at Different Rates")
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("30 SPM", f"{strokes/30:.1f} min")
            with col_b:
                st.metric("40 SPM", f"{strokes/40:.1f} min")
            with col_c:
                st.metric("50 SPM", f"{strokes/50:.1f} min")
            with col_d:
                st.metric("60 SPM", f"{strokes/60:.1f} min")
    
    with col2:
        st.info("""
        **Common Uses:**
        - Circulate bottoms up
        - Spot pills at depth
        - Track kill mud
        - Displace well
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 13: Circulation Time
# ═══════════════════════════════════════════════════════

elif "Circulation Time" in calc_type:
    st.markdown("## ⏱️ Circulation Time Calculator")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        pipe_vol = st.number_input("Drill String Volume (bbls):", 0.0, 5000.0, 178.0, 10.0)
        annular_vol = st.number_input("Annular Volume (bbls):", 0.0, 10000.0, 1200.0, 10.0)
        pump_output = st.number_input("Pump Output (bbl/stk):", 0.001, 1.0, 0.117, 0.001, format="%.3f")
        spm = st.number_input("Pump Rate (SPM):", 1, 120, 40, 5)
        
        if st.button("🧮 Calculate Circulation Times", type="primary", use_container_width=True):
            total_vol = pipe_vol + annular_vol
            bpm = pump_output * spm
            
            time_to_bit = pipe_vol / bpm
            lag_time = annular_vol / bpm
            total_time = total_vol / bpm
            
            strokes_to_bit = pipe_vol / pump_output
            strokes_lag = annular_vol / pump_output
            strokes_total = total_vol / pump_output
            
            save_calculation(
                calc_type="Circulation Time",
                inputs={
                    "Drill String": f"{pipe_vol} bbls",
                    "Annulus": f"{annular_vol} bbls",
                    "Pump Rate": f"{spm} SPM @ {pump_output} bbl/stk"
                },
                result=f"Total: {total_time:.1f} min | Lag: {lag_time:.1f} min",
                formula="Time = Volume / (Pump Output × SPM)"
            )
            
            st.markdown(f"""
            <div class="result-box">
                Total Circulation = {total_time:.1f} min<br>
                <span style="font-size: 1rem;">({int(total_time//60)}h {int(total_time%60)}m)</span>
            </div>
            <span class="saved-badge">✓ Saved to History</span>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("🔽 To Bit", f"{time_to_bit:.1f} min", f"{strokes_to_bit:,.0f} stks")
            with col_b:
                st.metric("🔼 Lag Time", f"{lag_time:.1f} min", f"{strokes_lag:,.0f} stks")
            with col_c:
                st.metric("🔄 Total", f"{total_time:.1f} min", f"{strokes_total:,.0f} stks")
    
    with col2:
        st.info("""
        **Lag Time:**
        Time for fluid at bit to reach surface.
        
        **Why important?**
        - Cuttings analysis
        - Gas readings
        - Kick detection timing
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 14: Trip Speed
# ═══════════════════════════════════════════════════════

elif "Trip Speed" in calc_type:
    st.markdown("## 🚀 Trip Speed Calculator")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        current_mw = st.number_input("Current MW (ppg):", 0.0, 25.0, 12.0, 0.1)
        fp_emw = st.number_input("Formation Pressure EMW (ppg):", 0.0, 25.0, 11.5, 0.1)
        safety = st.number_input("Safety Margin (ppg):", 0.0, 3.0, 0.5, 0.1)
        swab_factor = st.number_input("Swab Factor (ppg per ft/sec):", 0.01, 1.0, 0.15, 0.01)
        
        if st.button("🧮 Calculate Max Trip Speed", type="primary", use_container_width=True):
            available = current_mw - fp_emw - safety
            
            if available > 0 and swab_factor > 0:
                max_fps = available / swab_factor
                max_fpm = max_fps * 60
                
                save_calculation(
                    calc_type="Trip Speed",
                    inputs={
                        "Current MW": f"{current_mw} ppg",
                        "FP EMW": f"{fp_emw} ppg",
                        "Safety": f"{safety} ppg",
                        "Swab Factor": f"{swab_factor}"
                    },
                    result=f"{max_fps:.1f} ft/sec ({max_fpm:.0f} ft/min)",
                    formula="Max Speed = Available Margin / Swab Factor"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    Max Speed = {max_fps:.1f} ft/sec<br>
                    <span style="font-size: 1rem;">({max_fpm:.0f} ft/min)</span>
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                st.success(f"""
                **Recommendations:**
                - Max calculated: {max_fps:.1f} ft/sec
                - Recommended (80%): **{max_fps*0.8:.1f} ft/sec**
                - Conservative (60%): {max_fps*0.6:.1f} ft/sec
                """)
            else:
                st.error("Insufficient margin! Cannot trip safely.")
    
    with col2:
        st.warning("""
        **Swabbing:**
        - Pulling too fast
        - Creates suction
        - Reduces BHP → Kick
        
        **Surging:**
        - Running too fast
        - Increases pressure
        - Raises BHP → Losses
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 15: Boyle's Law
# ═══════════════════════════════════════════════════════

elif "Boyle's Law" in calc_type:
    st.markdown("## 💨 Gas Expansion Calculator (Boyle's Law)")
    
    st.markdown("""
    <div class="formula-box">
        <strong>P₁ × V₁ = P₂ × V₂</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        calc_mode = st.radio("Calculate:", ["Final Volume (V₂)", "Final Pressure (P₂)"], horizontal=True)
        
        if calc_mode == "Final Volume (V₂)":
            p1 = st.number_input("Initial Pressure P₁ (psi):", 0, 20000, 6000, 100)
            v1 = st.number_input("Initial Volume V₁ (bbls):", 0.0, 1000.0, 10.0, 1.0)
            p2 = st.number_input("Final Pressure P₂ (psi):", 1, 20000, 600, 100)
            
            if st.button("🧮 Calculate V₂", type="primary", use_container_width=True):
                v2 = (p1 * v1) / p2
                expansion = v2 / v1
                
                save_calculation(
                    calc_type="Boyle's Law (V₂)",
                    inputs={
                        "P₁": f"{p1:,} psi",
                        "V₁": f"{v1} bbls",
                        "P₂": f"{p2:,} psi"
                    },
                    result=f"{v2:.2f} bbls ({expansion:.1f}× expansion)",
                    formula="V₂ = (P₁ × V₁) / P₂"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    V₂ = {v2:.2f} bbls<br>
                    <span style="font-size: 1rem;">Expansion: {expansion:.1f}×</span>
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
                
                if expansion > 50:
                    st.error("⚠️ Massive expansion! Critical gas kick!")
                elif expansion > 10:
                    st.warning("⚠️ Large expansion. Careful control needed.")
        
        else:
            p1 = st.number_input("Initial Pressure P₁ (psi):", 0, 20000, 6000, 100, key="p1_p2")
            v1 = st.number_input("Initial Volume V₁ (bbls):", 0.0, 1000.0, 10.0, 1.0, key="v1_p2")
            v2 = st.number_input("Final Volume V₂ (bbls):", 0.1, 10000.0, 100.0, 10.0)
            
            if st.button("🧮 Calculate P₂", type="primary", use_container_width=True):
                p2 = (p1 * v1) / v2
                
                save_calculation(
                    calc_type="Boyle's Law (P₂)",
                    inputs={
                        "P₁": f"{p1:,} psi",
                        "V₁": f"{v1} bbls",
                        "V₂": f"{v2} bbls"
                    },
                    result=f"{p2:.0f} psi",
                    formula="P₂ = (P₁ × V₁) / V₂"
                )
                
                st.markdown(f"""
                <div class="result-box">
                    P₂ = {p2:.0f} psi
                </div>
                <span class="saved-badge">✓ Saved to History</span>
                """, unsafe_allow_html=True)
    
    with col2:
        st.warning("""
        **Gas Expansion:**
        
        10 bbls at 5,000 psi
        = **3,333 bbls at 15 psi!**
        
        Most expansion in last 2,000 ft!
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 16: Gas Migration
# ═══════════════════════════════════════════════════════

elif "Gas Migration" in calc_type:
    st.markdown("## 🌡️ Gas Migration Calculator")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        gas_depth = st.number_input("Current Gas Depth (ft):", 0, 40000, 8000, 100)
        migration_rate = st.number_input("Migration Rate (ft/hr):", 100, 5000, 1000, 100)
        
        if st.button("🧮 Calculate Migration Time", type="primary", use_container_width=True):
            time_hrs = gas_depth / migration_rate
            time_min = time_hrs * 60
            
            save_calculation(
                calc_type="Gas Migration",
                inputs={
                    "Gas Depth": f"{gas_depth:,} ft",
                    "Migration Rate": f"{migration_rate} ft/hr"
                },
                result=f"{time_hrs:.1f} hours to surface",
                formula="Time = Depth / Migration Rate"
            )
            
            st.markdown(f"""
            <div class="result-box">
                Time to Surface = {time_hrs:.1f} hours<br>
                <span style="font-size: 1rem;">({int(time_hrs)}h {int((time_hrs%1)*60)}m)</span>
            </div>
            <span class="saved-badge">✓ Saved to History</span>
            """, unsafe_allow_html=True)
            
            st.warning(f"""
            ⚠️ **Action Required:**
            - Monitor SICP every 15-30 min
            - Use volumetric method if needed
            - Decision time: **{time_hrs:.1f} hours**
            """)
    
    with col2:
        st.info("""
        **Typical Migration Rates:**
        - In water: 2,000-3,000 ft/hr
        - In mud: 500-2,000 ft/hr
        - Common assumption: **1,000 ft/hr**
        """)

# ═══════════════════════════════════════════════════════
# CALCULATOR 17: Unit Conversions
# ═══════════════════════════════════════════════════════

elif "Unit Conversions" in calc_type:
    st.markdown("## 🔀 Unit Conversion Calculator")
    
    conv_type = st.selectbox(
        "Select conversion type:",
        ["Pressure", "Mud Weight", "Volume", "Length", "Temperature", "Flow Rate"]
    )
    
    if conv_type == "Pressure":
        st.markdown("### Pressure Conversions")
        psi = st.number_input("Enter PSI:", 0.0, 100000.0, 1000.0, 10.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Bar", f"{psi/14.5:.2f}")
        with col2:
            st.metric("kPa", f"{psi*6.895:.0f}")
        with col3:
            st.metric("kg/cm²", f"{psi*0.0703:.2f}")
        
        if st.button("💾 Save Conversion", use_container_width=True):
            save_calculation(
                calc_type="Pressure Conversion",
                inputs={"PSI": f"{psi}"},
                result=f"{psi/14.5:.2f} bar | {psi*6.895:.0f} kPa",
                formula="1 psi = 0.0689 bar = 6.895 kPa"
            )
            st.success("✓ Saved!")
    
    elif conv_type == "Mud Weight":
        st.markdown("### Mud Weight Conversions")
        ppg = st.number_input("Enter PPG:", 0.0, 25.0, 10.0, 0.1)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("SG", f"{ppg/8.33:.3f}")
        with col2:
            st.metric("lb/ft³", f"{ppg*7.48:.1f}")
        with col3:
            st.metric("Gradient (psi/ft)", f"{ppg*0.052:.4f}")
        
        if st.button("💾 Save Conversion", use_container_width=True, key="save_mw"):
            save_calculation(
                calc_type="MW Conversion",
                inputs={"PPG": f"{ppg}"},
                result=f"SG: {ppg/8.33:.3f} | {ppg*0.052:.4f} psi/ft",
                formula="Gradient = 0.052 × ppg"
            )
            st.success("✓ Saved!")
    
    elif conv_type == "Volume":
        st.markdown("### Volume Conversions")
        bbl = st.number_input("Enter Barrels:", 0.0, 10000.0, 100.0, 10.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Gallons", f"{bbl*42:.0f}")
        with col2:
            st.metric("m³", f"{bbl*0.159:.2f}")
        with col3:
            st.metric("Liters", f"{bbl*159:.0f}")
        
        if st.button("💾 Save Conversion", use_container_width=True, key="save_vol"):
            save_calculation(
                calc_type="Volume Conversion",
                inputs={"Barrels": f"{bbl}"},
                result=f"{bbl*42:.0f} gal | {bbl*0.159:.2f} m³",
                formula="1 bbl = 42 gal = 0.159 m³"
            )
            st.success("✓ Saved!")
    
    elif conv_type == "Length":
        st.markdown("### Length Conversions")
        ft = st.number_input("Enter Feet:", 0.0, 100000.0, 10000.0, 100.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Meters", f"{ft*0.3048:.2f}")
        with col2:
            st.metric("Inches", f"{ft*12:.0f}")
        with col3:
            st.metric("Kilometers", f"{ft*0.0003048:.3f}")
        
        if st.button("💾 Save Conversion", use_container_width=True, key="save_len"):
            save_calculation(
                calc_type="Length Conversion",
                inputs={"Feet": f"{ft}"},
                result=f"{ft*0.3048:.2f} m",
                formula="1 ft = 0.3048 m"
            )
            st.success("✓ Saved!")
    
    elif conv_type == "Temperature":
        st.markdown("### Temperature Conversions")
        f_temp = st.number_input("Enter Fahrenheit:", -100.0, 500.0, 68.0, 1.0)
        c_temp = (f_temp - 32) * 5/9
        k_temp = c_temp + 273.15
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Celsius", f"{c_temp:.2f}")
        with col2:
            st.metric("Kelvin", f"{k_temp:.2f}")
        
        if st.button("💾 Save Conversion", use_container_width=True, key="save_temp"):
            save_calculation(
                calc_type="Temperature Conversion",
                inputs={"Fahrenheit": f"{f_temp}"},
                result=f"{c_temp:.2f}°C | {k_temp:.2f} K",
                formula="°C = (°F - 32) × 5/9"
            )
            st.success("✓ Saved!")
    
    else:  # Flow Rate
        st.markdown("### Flow Rate Conversions")
        gpm = st.number_input("Enter GPM:", 0.0, 2000.0, 400.0, 10.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("bbl/min", f"{gpm/42:.2f}")
        with col2:
            st.metric("L/min", f"{gpm*3.785:.1f}")
        with col3:
            st.metric("m³/hr", f"{gpm*0.227:.2f}")
        
        if st.button("💾 Save Conversion", use_container_width=True, key="save_flow"):
            save_calculation(
                calc_type="Flow Rate Conversion",
                inputs={"GPM": f"{gpm}"},
                result=f"{gpm/42:.2f} bbl/min",
                formula="1 bbl = 42 gal"
            )
            st.success("✓ Saved!")

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")

# Show history count
if st.session_state.calc_history:
    st.markdown(f"""
    <div style="text-align: center; background: #F3F4F6; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;">
        📊 <strong>{len(st.session_state.calc_history)}</strong> calculations saved this session
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p style="margin: 0;">🧮 <strong>Elshamy IWCF Calculator</strong></p>
    <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">
        All calculations with step-by-step solutions • Created by Eng. Ahmed Elshamy
    </p>
</div>
""", unsafe_allow_html=True)