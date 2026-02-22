import streamlit as st
import pandas as pd
import json
import random
from datetime import datetime

# ═══════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Formulas - Elshamy IWCF",
    page_icon="📖",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# التصميم
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .formulas-header {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .formula-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #10B981;
        transition: all 0.3s ease;
    }
    
    .formula-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-left-width: 8px;
    }
    
    .formula-equation {
        background: #F3F4F6;
        padding: 1.2rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 1.3rem;
        font-weight: bold;
        color: #1E40AF;
        margin: 1rem 0;
        text-align: center;
        border: 2px solid #E5E7EB;
    }
    
    .formula-variables {
        background: #DBEAFE;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .formula-example {
        background: #D1FAE5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #10B981;
    }
    
    .formula-tip {
        background: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .category-badge {
        display: inline-block;
        background: #3B82F6;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 0.5rem;
    }
    
    .favorite-icon {
        cursor: pointer;
        font-size: 1.5rem;
        transition: transform 0.2s;
    }
    
    .favorite-icon:hover {
        transform: scale(1.2);
    }
    
    .print-card {
        background: white;
        padding: 1rem;
        border: 2px dashed #9CA3AF;
        border-radius: 8px;
        margin: 0.5rem 0;
        page-break-inside: avoid;
    }
    
    .fotd-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    .calculator-box {
        background: #F0FDF4;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #10B981;
        margin: 1rem 0;
    }
    
    .result-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    @media print {
        .no-print {
            display: none !important;
        }
        .formula-card {
            page-break-inside: avoid;
        }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# Session State للـ Favorites و Study Mode
# ═══════════════════════════════════════════════════════

if 'favorite_formulas' not in st.session_state:
    st.session_state.favorite_formulas = []

if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False

if 'random_formula' not in st.session_state:
    st.session_state.random_formula = None

if 'study_mode' not in st.session_state:
    st.session_state.study_mode = "📖 Browse All"

# ═══════════════════════════════════════════════════════
# بنك المعادلات الكامل (موسّع)
# ═══════════════════════════════════════════════════════

FORMULAS = {
    "🔵 Pressure Calculations": [
        {
            "id": "hp",
            "name": "Hydrostatic Pressure",
            "formula": "HP = 0.052 × MW × TVD",
            "variables": {
                "HP": "Hydrostatic Pressure (psi)",
                "MW": "Mud Weight (ppg)",
                "TVD": "True Vertical Depth (ft)",
                "0.052": "Conversion constant (psi/ft per ppg)"
            },
            "example": "MW = 10 ppg, TVD = 5,000 ft\nHP = 0.052 × 10 × 5,000\nHP = 2,600 psi",
            "tip": "For 10 ppg: multiply depth by 0.52\nFor 12 ppg: multiply depth by 0.624",
            "units": "Imperial: psi, ppg, ft | Metric: bar, kg/l, m",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["fp", "bhp"]
        },
        {
            "id": "fp",
            "name": "Formation Pressure",
            "formula": "FP = SIDPP + (0.052 × OMW × TVD)",
            "variables": {
                "FP": "Formation Pressure (psi)",
                "SIDPP": "Shut-In Drill Pipe Pressure (psi)",
                "OMW": "Original Mud Weight (ppg)",
                "TVD": "True Vertical Depth (ft)"
            },
            "example": "SIDPP = 500 psi, OMW = 10 ppg, TVD = 10,000 ft\nFP = 500 + (0.052 × 10 × 10,000)\nFP = 500 + 5,200 = 5,700 psi",
            "tip": "SIDPP directly shows the pressure difference between formation and hydrostatic",
            "units": "psi, ppg, ft",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["hp", "kmw"]
        },
        {
            "id": "gradient",
            "name": "Pressure Gradient",
            "formula": "Gradient = 0.052 × MW",
            "variables": {
                "Gradient": "Pressure Gradient (psi/ft)",
                "MW": "Mud Weight (ppg)"
            },
            "example": "MW = 12 ppg\nGradient = 0.052 × 12 = 0.624 psi/ft",
            "tip": "Normal formation gradient ≈ 0.465 psi/ft (equivalent to 8.94 ppg)",
            "units": "psi/ft, ppg",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["hp"]
        },
        {
            "id": "bhp_static",
            "name": "Bottom Hole Pressure (Static)",
            "formula": "BHP = 0.052 × MW × TVD",
            "variables": {
                "BHP": "Bottom Hole Pressure (psi)",
                "MW": "Mud Weight (ppg)",
                "TVD": "True Vertical Depth (ft)"
            },
            "example": "Same as Hydrostatic Pressure when pumps are OFF",
            "tip": "BHP static = HP (no circulation)",
            "units": "psi, ppg, ft",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "Medium",
            "related": ["hp", "bhp_dynamic"]
        },
        {
            "id": "bhp_dynamic",
            "name": "Bottom Hole Pressure (Circulating)",
            "formula": "BHP = HP + APL",
            "variables": {
                "BHP": "Bottom Hole Pressure (psi)",
                "HP": "Hydrostatic Pressure (psi)",
                "APL": "Annular Pressure Loss (psi)"
            },
            "example": "HP = 5,200 psi, APL = 300 psi\nBHP = 5,200 + 300 = 5,500 psi",
            "tip": "Always higher when circulating due to friction losses",
            "units": "psi",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["ecd"]
        },
        {
            "id": "ecd",
            "name": "Equivalent Circulating Density (ECD)",
            "formula": "ECD = MW + [APL / (0.052 × TVD)]",
            "variables": {
                "ECD": "Equivalent Circulating Density (ppg)",
                "MW": "Static Mud Weight (ppg)",
                "APL": "Annular Pressure Loss (psi)",
                "TVD": "True Vertical Depth (ft)"
            },
            "example": "MW = 10 ppg, APL = 260 psi, TVD = 10,000 ft\nECD = 10 + [260 / (0.052 × 10,000)]\nECD = 10 + 0.5 = 10.5 ppg",
            "tip": "ECD > MW when circulating. If ECD exceeds fracture gradient → losses!",
            "units": "ppg, psi, ft",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["bhp_dynamic"]
        }
    ],
    
    "⚡ Kill Sheet Calculations": [
        {
            "id": "kmw",
            "name": "Kill Mud Weight (KMW)",
            "formula": "KMW = [SIDPP / (0.052 × TVD)] + OMW",
            "variables": {
                "KMW": "Kill Mud Weight (ppg)",
                "SIDPP": "Shut-In Drill Pipe Pressure (psi)",
                "TVD": "True Vertical Depth (ft)",
                "OMW": "Original Mud Weight (ppg)"
            },
            "example": "SIDPP = 500 psi, TVD = 10,000 ft, OMW = 10 ppg\nKMW = [500 / (0.052 × 10,000)] + 10\nKMW = [500 / 520] + 10\nKMW = 0.96 + 10 = 10.96 ppg",
            "tip": "⚠️ NEVER forget to ADD the OMW at the end! Common exam trap!",
            "units": "ppg, psi, ft",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["fp", "icp", "fcp"]
        },
        {
            "id": "icp",
            "name": "Initial Circulating Pressure (ICP)",
            "formula": "ICP = SIDPP + SCR",
            "variables": {
                "ICP": "Initial Circulating Pressure (psi)",
                "SIDPP": "Shut-In Drill Pipe Pressure (psi)",
                "SCR": "Slow Circulating Rate pressure (psi)"
            },
            "example": "SIDPP = 500 psi, SCR = 400 psi\nICP = 500 + 400 = 900 psi",
            "tip": "This is your STARTING pressure for kill operation. Hold constant in Driller's Method first circulation.",
            "units": "psi",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["fcp", "kmw"]
        },
        {
            "id": "fcp",
            "name": "Final Circulating Pressure (FCP)",
            "formula": "FCP = SCR × (KMW / OMW)",
            "variables": {
                "FCP": "Final Circulating Pressure (psi)",
                "SCR": "Slow Circulating Rate pressure (psi)",
                "KMW": "Kill Mud Weight (ppg)",
                "OMW": "Original Mud Weight (ppg)"
            },
            "example": "SCR = 400 psi, KMW = 10.5 ppg, OMW = 10 ppg\nFCP = 400 × (10.5 / 10)\nFCP = 400 × 1.05 = 420 psi",
            "tip": "FCP is proportional to mud weight ratio. Heavier mud = higher pressure.",
            "units": "psi, ppg",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["icp", "kmw"]
        },
        {
            "id": "maasp",
            "name": "Maximum Allowable Annular Surface Pressure (MAASP)",
            "formula": "MAASP = Fracture Pressure - (0.052 × MW × Shoe TVD)",
            "variables": {
                "MAASP": "Maximum Allowable Annular Surface Pressure (psi)",
                "Fracture Pressure": "At casing shoe (psi)",
                "MW": "Current Mud Weight (ppg)",
                "Shoe TVD": "Casing shoe depth (ft)"
            },
            "example": "Frac = 8,000 psi, MW = 12 ppg, Shoe = 5,000 ft\nMAASP = 8,000 - (0.052 × 12 × 5,000)\nMAASP = 8,000 - 3,120 = 4,880 psi",
            "tip": "⚠️ NEVER exceed MAASP during kill! Will fracture formation and cause underground blowout.",
            "units": "psi, ppg, ft",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["fit"]
        },
        {
            "id": "pressure_schedule",
            "name": "Pressure Schedule (Wait & Weight)",
            "formula": "P = ICP - [(ICP - FCP) × (Strokes / Total Strokes)]",
            "variables": {
                "P": "Drillpipe pressure at any point (psi)",
                "ICP": "Initial Circulating Pressure (psi)",
                "FCP": "Final Circulating Pressure (psi)",
                "Strokes": "Strokes pumped so far",
                "Total Strokes": "Total strokes to bit"
            },
            "example": "ICP = 900 psi, FCP = 550 psi, Total = 4,000\nAt 2,000 strokes:\nP = 900 - [(900-550) × (2,000/4,000)]\nP = 900 - 175 = 725 psi",
            "tip": "Linear decrease from ICP to FCP as kill mud reaches bit",
            "units": "psi, strokes",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["icp", "fcp"]
        }
    ],
    
    "📐 Volume Calculations": [
        {
            "id": "annular_capacity",
            "name": "Annular Capacity",
            "formula": "Capacity = (ID² - OD²) / 1029.4",
            "variables": {
                "Capacity": "Annular Capacity (bbl/ft)",
                "ID": "Hole/Casing Inside Diameter (inches)",
                "OD": "Pipe Outside Diameter (inches)",
                "1029.4": "Conversion constant"
            },
            "example": "ID = 12.25 in, OD = 5 in\nCapacity = (12.25² - 5²) / 1029.4\nCapacity = (150.06 - 25) / 1029.4\nCapacity = 0.1215 bbl/ft",
            "tip": "Use ID for holes/casing, OD for pipes. Constant is 1029.4 (NOT 1029!)",
            "units": "bbl/ft, inches",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["annular_volume"]
        },
        {
            "id": "annular_volume",
            "name": "Annular Volume",
            "formula": "Volume = Capacity × Length",
            "variables": {
                "Volume": "Annular Volume (bbls)",
                "Capacity": "Annular Capacity (bbl/ft)",
                "Length": "Section Length (ft)"
            },
            "example": "Capacity = 0.1215 bbl/ft, Length = 10,000 ft\nVolume = 0.1215 × 10,000 = 1,215 bbls",
            "tip": "Convert to gallons: multiply by 42",
            "units": "bbls, bbl/ft, ft",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["annular_capacity", "strokes"]
        },
        {
            "id": "pipe_capacity",
            "name": "Pipe Capacity (Internal)",
            "formula": "Capacity = ID² / 1029.4",
            "variables": {
                "Capacity": "Pipe Internal Capacity (bbl/ft)",
                "ID": "Pipe Inside Diameter (inches)"
            },
            "example": "5 inch DP, ID = 4.276 in\nCapacity = 4.276² / 1029.4\nCapacity = 18.28 / 1029.4 = 0.0178 bbl/ft",
            "tip": "Common values: 5\" DP ≈ 0.0178 bbl/ft, 4.5\" DP ≈ 0.0142 bbl/ft",
            "units": "bbl/ft, inches",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["strokes"]
        },
        {
            "id": "displacement",
            "name": "Pipe Displacement",
            "formula": "Displacement = (OD² - ID²) / 1029.4",
            "variables": {
                "Displacement": "Pipe Displacement (bbl/ft)",
                "OD": "Pipe Outside Diameter (inches)",
                "ID": "Pipe Inside Diameter (inches)"
            },
            "example": "5 inch DP: OD = 5 in, ID = 4.276 in\nDisp = (25 - 18.28) / 1029.4\nDisp = 6.72 / 1029.4 = 0.0065 bbl/ft",
            "tip": "Displacement = steel volume. When pulling out, hole needs this much mud to fill.",
            "units": "bbl/ft, inches",
            "importance": "⭐⭐⭐",
            "exam_frequency": "Medium",
            "related": ["annular_capacity"]
        }
    ],
    
    "🔄 Strokes & Time": [
        {
            "id": "strokes",
            "name": "Strokes Required",
            "formula": "Strokes = Volume / Pump Output",
            "variables": {
                "Strokes": "Number of strokes required",
                "Volume": "Volume to pump (bbls)",
                "Pump Output": "Pump output (bbl/stk)"
            },
            "example": "Volume = 500 bbls, Output = 0.117 bbl/stk\nStrokes = 500 / 0.117 = 4,274 strokes",
            "tip": "Check pump output card! Common outputs: 0.112, 0.117, 0.136 bbl/stk",
            "units": "strokes, bbls, bbl/stk",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["circulation_time"]
        },
        {
            "id": "circulation_time",
            "name": "Circulation Time",
            "formula": "Time (min) = Strokes / SPM",
            "variables": {
                "Time": "Time required (minutes)",
                "Strokes": "Total strokes",
                "SPM": "Strokes Per Minute (pump rate)"
            },
            "example": "Strokes = 4,000, SPM = 40\nTime = 4,000 / 40 = 100 minutes\n= 1 hour 40 minutes",
            "tip": "Convert to hours: divide by 60. Typical SPM: 30-60",
            "units": "minutes, strokes, SPM",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["strokes"]
        },
        {
            "id": "lag_time",
            "name": "Lag Time",
            "formula": "Lag Time = Annular Volume / (Pump Output × SPM)",
            "variables": {
                "Lag Time": "Time for fluid from bit to surface (minutes)",
                "Annular Volume": "Annular volume (bbls)",
                "Pump Output": "Pump output (bbl/stk)",
                "SPM": "Strokes per minute"
            },
            "example": "Annular = 1,200 bbls, Output = 0.117, SPM = 40\nLag = 1,200 / (0.117 × 40)\nLag = 1,200 / 4.68 = 256 minutes",
            "tip": "Critical for kick detection! Cuttings/gas from bit take this long to surface.",
            "units": "minutes, bbls, bbl/stk, SPM",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "Medium",
            "related": ["circulation_time"]
        }
    ],
    
    "🌊 Subsea Calculations": [
        {
            "id": "clf",
            "name": "Choke Line Friction (CLF) Correction",
            "formula": "True SICP = Surface SICP + CLF",
            "variables": {
                "True SICP": "Actual casing pressure at BOP (psi)",
                "Surface SICP": "Measured at surface (psi)",
                "CLF": "Choke Line Friction pressure loss (psi)"
            },
            "example": "Surface SICP = 800 psi, CLF = 150 psi\nTrue SICP = 800 + 150 = 950 psi",
            "tip": "Always ADD friction for subsea! Surface reading is LESS than actual.",
            "units": "psi",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High (Subsea wells)",
            "related": ["riser_margin"]
        },
        {
            "id": "riser_margin",
            "name": "Riser Margin",
            "formula": "RM = (MW - Seawater) × 0.052 × Water Depth",
            "variables": {
                "RM": "Riser Margin (psi)",
                "MW": "Mud Weight in riser (ppg)",
                "Seawater": "Seawater gradient (8.6 ppg typical)",
                "Water Depth": "Depth to mudline (ft)"
            },
            "example": "MW = 12 ppg, Seawater = 8.6 ppg, Depth = 5,000 ft\nRM = (12 - 8.6) × 0.052 × 5,000\nRM = 3.4 × 260 = 884 psi",
            "tip": "Typical minimum: 200 psi. Normal: 400-600 psi. Prevents U-tubing on disconnect.",
            "units": "psi, ppg, ft",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High (Subsea wells)",
            "related": ["clf"]
        }
    ],
    
    "🔀 Unit Conversions": [
        {
            "id": "pressure_conv",
            "name": "Pressure Conversions",
            "formula": "1 psi = 0.0689 bar = 6.895 kPa = 0.0703 kg/cm²",
            "variables": {
                "psi": "Pounds per square inch",
                "bar": "Metric pressure unit",
                "kPa": "Kilopascals",
                "kg/cm²": "Kilograms per square centimeter"
            },
            "example": "1,000 psi = 68.9 bar = 6,895 kPa = 70.3 kg/cm²",
            "tip": "Quick: 1 bar ≈ 14.5 psi (easy to remember)",
            "units": "psi, bar, kPa, kg/cm²",
            "importance": "⭐⭐⭐",
            "exam_frequency": "Medium",
            "related": ["mw_conv"]
        },
        {
            "id": "mw_conv",
            "name": "Mud Weight Conversions",
            "formula": "1 ppg = 0.12 sg = 7.48 lb/ft³ = 119.83 kg/m³",
            "variables": {
                "ppg": "Pounds per gallon",
                "sg": "Specific gravity",
                "lb/ft³": "Pounds per cubic foot",
                "kg/m³": "Kilograms per cubic meter"
            },
            "example": "10 ppg = 1.2 sg = 74.8 lb/ft³ = 1,198 kg/m³",
            "tip": "Quick: 1 sg = 8.33 ppg (water specific gravity)",
            "units": "ppg, sg, lb/ft³, kg/m³",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["pressure_conv"]
        },
        {
            "id": "volume_conv",
            "name": "Volume Conversions",
            "formula": "1 bbl = 42 US gal = 0.159 m³ = 159 L = 35 Imp gal",
            "variables": {
                "bbl": "Barrels (oil field)",
                "US gal": "US Gallons",
                "m³": "Cubic meters",
                "L": "Liters",
                "Imp gal": "Imperial Gallons"
            },
            "example": "100 bbl = 4,200 gal = 15.9 m³ = 15,900 L",
            "tip": "Remember: 1 barrel = 42 gallons (oil price barrel)",
            "units": "bbl, gal, m³, L",
            "importance": "⭐⭐⭐",
            "exam_frequency": "Medium",
            "related": ["annular_volume"]
        },
        {
            "id": "length_conv",
            "name": "Length Conversions",
            "formula": "1 ft = 0.3048 m = 12 in = 30.48 cm",
            "variables": {
                "ft": "Feet",
                "m": "Meters",
                "in": "Inches",
                "cm": "Centimeters"
            },
            "example": "10,000 ft = 3,048 m = 120,000 in",
            "tip": "Quick: 1 meter ≈ 3.28 feet",
            "units": "ft, m, in, cm",
            "importance": "⭐⭐⭐",
            "exam_frequency": "Medium",
            "related": []
        }
    ],
    
    "💨 Gas Behavior": [
        {
            "id": "boyles_law",
            "name": "Boyle's Law (Gas Expansion)",
            "formula": "P₁ × V₁ = P₂ × V₂",
            "variables": {
                "P₁": "Initial pressure (psi)",
                "V₁": "Initial volume (bbls)",
                "P₂": "Final pressure (psi)",
                "V₂": "Final volume (bbls)"
            },
            "example": "Gas at 6,000 psi, 10 bbls expands to 600 psi\nV₂ = P₁ × V₁ / P₂\nV₂ = 6,000 × 10 / 600 = 100 bbls\n10× expansion!",
            "tip": "At constant temperature! Small kick at depth = HUGE at surface.",
            "units": "psi, bbls (any consistent units)",
            "importance": "⭐⭐⭐⭐⭐",
            "exam_frequency": "Very High",
            "related": ["gas_migration"]
        },
        {
            "id": "gas_migration",
            "name": "Gas Migration Rate",
            "formula": "Time (hrs) = Depth (ft) / Migration Rate (ft/hr)",
            "variables": {
                "Time": "Time for gas to reach surface (hours)",
                "Depth": "Current gas depth (ft)",
                "Migration Rate": "Typical: 500-2,000 ft/hr (avg: 1,000)"
            },
            "example": "Gas at 8,000 ft, migration = 1,000 ft/hr\nTime = 8,000 / 1,000 = 8 hours to surface",
            "tip": "While shut-in, gas rises and pressure increases! Must use volumetric method or circulate.",
            "units": "hours, ft, ft/hr",
            "importance": "⭐⭐⭐⭐",
            "exam_frequency": "High",
            "related": ["boyles_law"]
        }
    ]
}

# ═══════════════════════════════════════════════════════
# SIDEBAR - Study Mode
# ═══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🎓 Study Controls")
    
    st.session_state.study_mode = st.radio(
        "Select study mode:",
        ["📖 Browse All", "🎲 Random Formula", "📝 Quiz Mode"],
        index=0
    )
    
    if st.session_state.study_mode == "🎲 Random Formula":
        if st.button("🎲 Show Random Formula", use_container_width=True):
            all_formulas = [f for formulas in FORMULAS.values() for f in formulas]
            st.session_state.random_formula = random.choice(all_formulas)
    
    elif st.session_state.study_mode == "📝 Quiz Mode":
        st.info("🧠 Test yourself! Try to recall the formula before revealing.")
        st.session_state.quiz_mode = True
    else:
        st.session_state.quiz_mode = False
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    total_formulas = sum(len(formulas) for formulas in FORMULAS.values())
    favorites_count = len(st.session_state.favorite_formulas)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📚 Total", total_formulas)
    with col2:
        st.metric("⭐ Favorites", favorites_count)
    
    # Progress bar
    if st.session_state.favorite_formulas:
        progress_pct = favorites_count / total_formulas
        st.progress(progress_pct)
        st.caption(f"Marked {progress_pct*100:.0f}% as favorites")
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    if st.button("📥 Download All Formulas", use_container_width=True):
        st.session_state.show_download = True
    if st.button("🖨️ Print Cheat Sheet", use_container_width=True):
        st.session_state.show_cheatsheet = True

# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="formulas-header">
    <h1>📖 IWCF Complete Formulas Reference</h1>
    <p>Your comprehensive guide to all well control calculations • Updated 2026</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 💡 FORMULA OF THE DAY
# ═══════════════════════════════════════════════════════

# Set seed based on date for consistent daily formula
random.seed(datetime.now().strftime("%Y-%m-%d"))
all_formulas_list = [f for formulas in FORMULAS.values() for f in formulas]
formula_of_day = random.choice(all_formulas_list)

st.markdown(f"""
<div class="fotd-card">
    <h3 style="margin: 0;">💡 Formula of the Day</h3>
    <h2 style="margin: 0.5rem 0;">{formula_of_day['name']}</h2>
    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0; font-family: monospace; font-size: 1.2rem;">
        {formula_of_day['formula']}
    </div>
    <p style="margin: 0; opacity: 0.9;">💡 {formula_of_day['tip'].split(chr(10))[0]}</p>
</div>
""", unsafe_allow_html=True)

# Reset random seed
random.seed()

# ═══════════════════════════════════════════════════════
# RANDOM FORMULA DISPLAY (if selected)
# ═══════════════════════════════════════════════════════

if st.session_state.study_mode == "🎲 Random Formula" and st.session_state.random_formula:
    rf = st.session_state.random_formula
    st.markdown("---")
    st.markdown("## 🎲 Random Formula")
    
    st.markdown(f"""
    <div class="formula-card" style="border-left-color: #8B5CF6;">
        <h2 style="color: #8B5CF6;">{rf['name']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="formula-equation" style="border-color: #8B5CF6;">
        {rf['formula']}
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 See Details"):
        st.markdown("**Variables:**")
        for var, desc in rf['variables'].items():
            st.markdown(f"- **`{var}`**: {desc}")
        
        st.markdown("**Example:**")
        st.code(rf['example'])
        
        st.info(f"💡 **Tip:** {rf['tip']}")
    
    if st.button("🎲 Get Another Random Formula"):
        st.session_state.random_formula = random.choice(all_formulas_list)
        st.rerun()
    
    st.markdown("---")

# ═══════════════════════════════════════════════════════
# SEARCH & FILTER
# ═══════════════════════════════════════════════════════

st.markdown("## 🔍 Search & Filter")

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    search_term = st.text_input(
        "🔍 Search formulas by name, variable, or keyword...",
        placeholder="e.g., 'pressure', 'SIDPP', 'kill'...",
        label_visibility="collapsed"
    )

with col2:
    category_filter = st.selectbox(
        "📁 Filter by category:",
        ["All Categories"] + list(FORMULAS.keys()),
        label_visibility="collapsed"
    )

with col3:
    show_favorites = st.checkbox("⭐ Favorites Only", value=False)

# ═══════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════

total_formulas = sum(len(formulas) for formulas in FORMULAS.values())
total_categories = len(FORMULAS)
favorites_count = len(st.session_state.favorite_formulas)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Total Formulas", total_formulas)
with col2:
    st.metric("📁 Categories", total_categories)
with col3:
    st.metric("⭐ Favorites", favorites_count)
with col4:
    if st.button("🖨️ Print Mode", use_container_width=True):
        st.info("💡 Use Ctrl+P / Cmd+P for best results!")

# ═══════════════════════════════════════════════════════
# DISPLAY FORMULAS
# ═══════════════════════════════════════════════════════

st.markdown("---")

# Filter categories
categories_to_show = FORMULAS.keys() if category_filter == "All Categories" else [category_filter]

# Track formulas shown
formulas_shown = 0

for category in categories_to_show:
    if category not in FORMULAS:
        continue
        
    formulas = FORMULAS[category]
    
    # Filter by search
    if search_term:
        formulas = [f for f in formulas if 
                   search_term.lower() in f['name'].lower() or
                   search_term.lower() in f['formula'].lower() or
                   any(search_term.lower() in var.lower() or search_term.lower() in desc.lower() 
                       for var, desc in f['variables'].items())]
    
    # Filter by favorites
    if show_favorites:
        formulas = [f for f in formulas if f['id'] in st.session_state.favorite_formulas]
    
    if not formulas:
        continue
    
    # Category header
    st.markdown(f"## {category}")
    st.caption(f"{len(formulas)} formula{'s' if len(formulas) != 1 else ''} in this category")
    
    # Display each formula
    for formula in formulas:
        formulas_shown += 1
        
        # Check if favorited
        is_favorite = formula['id'] in st.session_state.favorite_formulas
        
        col_main, col_fav = st.columns([20, 1])
        
        with col_fav:
            if st.button("⭐" if is_favorite else "☆", key=f"fav_{formula['id']}", help="Add to favorites"):
                if is_favorite:
                    st.session_state.favorite_formulas.remove(formula['id'])
                else:
                    st.session_state.favorite_formulas.append(formula['id'])
                st.rerun()
        
        with col_main:
            st.markdown(f"""
            <div class="formula-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #1F2937;">{formula['name']}</h3>
                        <span class="category-badge">{category.split()[1] if len(category.split()) > 1 else category}</span>
                        <span style="margin-left: 0.5rem; font-size: 0.9rem;">
                            Importance: {formula['importance']}
                        </span>
                    </div>
                    <div style="text-align: right; font-size: 0.85rem; color: #6B7280;">
                        <div>Exam: {formula['exam_frequency']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quiz Mode - Hide formula initially
            if st.session_state.quiz_mode:
                if st.button(f"👁️ Reveal Formula", key=f"reveal_{formula['id']}"):
                    st.markdown(f"""
                    <div class="formula-equation">
                        {formula['formula']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Normal mode - show formula
                st.markdown(f"""
                <div class="formula-equation">
                    {formula['formula']}
                </div>
                """, unsafe_allow_html=True)
            
            # ═══════════════════════════════════════════════════════
            # 🧮 QUICK CALCULATOR (NEW!)
            # ═══════════════════════════════════════════════════════
            
            with st.expander(f"🧮 Quick Calculate: {formula['name']}"):
                st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
                
                if formula['id'] == 'hp':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        mw_calc = st.number_input("MW (ppg):", 0.0, 25.0, 10.0, 0.1, key=f"calc_mw_{formula['id']}")
                        tvd_calc = st.number_input("TVD (ft):", 0, 50000, 10000, 100, key=f"calc_tvd_{formula['id']}")
                    with col_b:
                        if st.button("Calculate HP", key=f"btn_{formula['id']}", type="primary"):
                            result = 0.052 * mw_calc * tvd_calc
                            st.markdown(f'<div class="result-box">HP = {result:,.2f} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**Calculation:** 0.052 × {mw_calc} × {tvd_calc:,} = {result:,.2f} psi")
                
                elif formula['id'] == 'fp':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        sidpp_fp = st.number_input("SIDPP (psi):", 0, 5000, 500, 10, key=f"calc_sidpp_fp_{formula['id']}")
                        omw_fp = st.number_input("OMW (ppg):", 0.0, 25.0, 10.0, 0.1, key=f"calc_omw_fp_{formula['id']}")
                        tvd_fp = st.number_input("TVD (ft):", 0, 50000, 10000, 100, key=f"calc_tvd_fp_{formula['id']}")
                    with col_b:
                        if st.button("Calculate FP", key=f"btn_{formula['id']}", type="primary"):
                            hp = 0.052 * omw_fp * tvd_fp
                            result = sidpp_fp + hp
                            st.markdown(f'<div class="result-box">FP = {result:,.2f} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**HP** = 0.052 × {omw_fp} × {tvd_fp:,} = {hp:,.2f} psi")
                            st.caption(f"**FP** = {sidpp_fp} + {hp:,.2f} = {result:,.2f} psi")
                
                elif formula['id'] == 'kmw':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        sidpp_calc = st.number_input("SIDPP (psi):", 0, 5000, 500, 10, key=f"calc_sidpp_{formula['id']}")
                        tvd_kmw = st.number_input("TVD (ft):", 0, 50000, 10000, 100, key=f"calc_tvd_kmw_{formula['id']}")
                        omw_calc = st.number_input("OMW (ppg):", 0.0, 25.0, 10.0, 0.1, key=f"calc_omw_{formula['id']}")
                    with col_b:
                        if st.button("Calculate KMW", key=f"btn_{formula['id']}", type="primary"):
                            increase = sidpp_calc / (0.052 * tvd_kmw)
                            kmw_result = increase + omw_calc
                            st.markdown(f'<div class="result-box">KMW = {kmw_result:.2f} ppg</div>', unsafe_allow_html=True)
                            st.caption(f"**Increase** = {sidpp_calc} ÷ (0.052 × {tvd_kmw:,}) = {increase:.2f} ppg")
                            st.caption(f"**KMW** = {increase:.2f} + {omw_calc} = {kmw_result:.2f} ppg")
                            st.warning("⚠️ Remember: ALWAYS add OMW at the end!")
                
                elif formula['id'] == 'icp':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        sidpp_icp = st.number_input("SIDPP (psi):", 0, 5000, 500, 10, key=f"calc_sidpp_icp_{formula['id']}")
                        scr_calc = st.number_input("SCR (psi):", 0, 3000, 400, 10, key=f"calc_scr_{formula['id']}")
                    with col_b:
                        if st.button("Calculate ICP", key=f"btn_{formula['id']}", type="primary"):
                            icp_result = sidpp_icp + scr_calc
                            st.markdown(f'<div class="result-box">ICP = {icp_result:,} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**ICP** = {sidpp_icp} + {scr_calc} = {icp_result:,} psi")
                
                elif formula['id'] == 'fcp':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        scr_fcp = st.number_input("SCR (psi):", 0, 3000, 400, 10, key=f"calc_scr_fcp_{formula['id']}")
                        kmw_fcp = st.number_input("KMW (ppg):", 0.0, 25.0, 10.5, 0.1, key=f"calc_kmw_fcp_{formula['id']}")
                        omw_fcp = st.number_input("OMW (ppg):", 0.0, 25.0, 10.0, 0.1, key=f"calc_omw_fcp_{formula['id']}")
                    with col_b:
                        if st.button("Calculate FCP", key=f"btn_{formula['id']}", type="primary"):
                            ratio = kmw_fcp / omw_fcp
                            fcp_result = scr_fcp * ratio
                            st.markdown(f'<div class="result-box">FCP = {fcp_result:.0f} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**Ratio** = {kmw_fcp} ÷ {omw_fcp} = {ratio:.4f}")
                            st.caption(f"**FCP** = {scr_fcp} × {ratio:.4f} = {fcp_result:.0f} psi")
                
                elif formula['id'] == 'maasp':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        frac_p = st.number_input("Fracture Pressure (psi):", 0, 20000, 8000, 100, key=f"calc_frac_{formula['id']}")
                        mw_maasp = st.number_input("MW (ppg):", 0.0, 25.0, 12.0, 0.1, key=f"calc_mw_maasp_{formula['id']}")
                        shoe_tvd = st.number_input("Shoe TVD (ft):", 0, 30000, 5000, 100, key=f"calc_shoe_{formula['id']}")
                    with col_b:
                        if st.button("Calculate MAASP", key=f"btn_{formula['id']}", type="primary"):
                            hp_shoe = 0.052 * mw_maasp * shoe_tvd
                            maasp_result = frac_p - hp_shoe
                            st.markdown(f'<div class="result-box">MAASP = {maasp_result:,.0f} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**HP at shoe** = 0.052 × {mw_maasp} × {shoe_tvd:,} = {hp_shoe:,.0f} psi")
                            st.caption(f"**MAASP** = {frac_p:,} - {hp_shoe:,.0f} = {maasp_result:,.0f} psi")
                            st.error("⚠️ NEVER exceed MAASP during kill operations!")
                
                elif formula['id'] == 'ecd':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        mw_ecd = st.number_input("MW (ppg):", 0.0, 25.0, 10.0, 0.1, key=f"calc_mw_ecd_{formula['id']}")
                        apl_ecd = st.number_input("APL (psi):", 0, 2000, 260, 10, key=f"calc_apl_ecd_{formula['id']}")
                        tvd_ecd = st.number_input("TVD (ft):", 0, 50000, 10000, 100, key=f"calc_tvd_ecd_{formula['id']}")
                    with col_b:
                        if st.button("Calculate ECD", key=f"btn_{formula['id']}", type="primary"):
                            ecd_increase = apl_ecd / (0.052 * tvd_ecd)
                            ecd_result = mw_ecd + ecd_increase
                            st.markdown(f'<div class="result-box">ECD = {ecd_result:.2f} ppg</div>', unsafe_allow_html=True)
                            st.caption(f"**Increase** = {apl_ecd} ÷ (0.052 × {tvd_ecd:,}) = {ecd_increase:.2f} ppg")
                            st.caption(f"**ECD** = {mw_ecd} + {ecd_increase:.2f} = {ecd_result:.2f} ppg")
                
                elif formula['id'] == 'annular_capacity':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        id_cap = st.number_input("Hole/Casing ID (in):", 0.0, 30.0, 12.25, 0.25, key=f"calc_id_{formula['id']}")
                        od_cap = st.number_input("Pipe OD (in):", 0.0, 15.0, 5.0, 0.25, key=f"calc_od_{formula['id']}")
                    with col_b:
                        if st.button("Calculate Capacity", key=f"btn_{formula['id']}", type="primary"):
                            cap_result = (id_cap**2 - od_cap**2) / 1029.4
                            st.markdown(f'<div class="result-box">Capacity = {cap_result:.4f} bbl/ft</div>', unsafe_allow_html=True)
                            st.caption(f"**Calculation:** ({id_cap}² - {od_cap}²) ÷ 1029.4")
                            st.caption(f"= ({id_cap**2:.2f} - {od_cap**2:.2f}) ÷ 1029.4 = {cap_result:.4f} bbl/ft")
                
                elif formula['id'] == 'strokes':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        vol_stk = st.number_input("Volume (bbls):", 0.0, 5000.0, 500.0, 10.0, key=f"calc_vol_{formula['id']}")
                        output_stk = st.number_input("Pump Output (bbl/stk):", 0.0, 0.5, 0.117, 0.001, key=f"calc_output_{formula['id']}")
                    with col_b:
                        if st.button("Calculate Strokes", key=f"btn_{formula['id']}", type="primary"):
                            strokes_result = vol_stk / output_stk
                            st.markdown(f'<div class="result-box">Strokes = {strokes_result:,.0f}</div>', unsafe_allow_html=True)
                            st.caption(f"**Strokes** = {vol_stk} ÷ {output_stk} = {strokes_result:,.0f} strokes")
                
                elif formula['id'] == 'boyles_law':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        p1_boyle = st.number_input("P₁ Initial (psi):", 0, 20000, 6000, 100, key=f"calc_p1_{formula['id']}")
                        v1_boyle = st.number_input("V₁ Initial (bbls):", 0.0, 500.0, 10.0, 1.0, key=f"calc_v1_{formula['id']}")
                        p2_boyle = st.number_input("P₂ Final (psi):", 0, 20000, 600, 100, key=f"calc_p2_{formula['id']}")
                    with col_b:
                        if st.button("Calculate V₂", key=f"btn_{formula['id']}", type="primary"):
                            v2_result = (p1_boyle * v1_boyle) / p2_boyle
                            expansion = v2_result / v1_boyle
                            st.markdown(f'<div class="result-box">V₂ = {v2_result:,.1f} bbls</div>', unsafe_allow_html=True)
                            st.caption(f"**V₂** = ({p1_boyle:,} × {v1_boyle}) ÷ {p2_boyle} = {v2_result:,.1f} bbls")
                            st.warning(f"⚠️ **{expansion:.0f}× expansion!** Small kick at depth = HUGE at surface!")
                
                elif formula['id'] == 'clf':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        surface_sicp = st.number_input("Surface SICP (psi):", 0, 5000, 800, 10, key=f"calc_surf_{formula['id']}")
                        clf_val = st.number_input("CLF (psi):", 0, 1000, 150, 10, key=f"calc_clf_{formula['id']}")
                    with col_b:
                        if st.button("Calculate True SICP", key=f"btn_{formula['id']}", type="primary"):
                            true_sicp = surface_sicp + clf_val
                            st.markdown(f'<div class="result-box">True SICP = {true_sicp:,} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**True SICP** = {surface_sicp} + {clf_val} = {true_sicp:,} psi")
                            st.info("💡 Always ADD CLF for subsea wells!")
                
                elif formula['id'] == 'riser_margin':
                    col_a, col_b = st.columns(2)
                    with col_a:
                        mw_rm = st.number_input("MW (ppg):", 0.0, 25.0, 12.0, 0.1, key=f"calc_mw_rm_{formula['id']}")
                        sw_rm = st.number_input("Seawater (ppg):", 8.0, 9.0, 8.6, 0.1, key=f"calc_sw_rm_{formula['id']}")
                        wd_rm = st.number_input("Water Depth (ft):", 0, 15000, 5000, 100, key=f"calc_wd_rm_{formula['id']}")
                    with col_b:
                        if st.button("Calculate RM", key=f"btn_{formula['id']}", type="primary"):
                            rm_result = (mw_rm - sw_rm) * 0.052 * wd_rm
                            st.markdown(f'<div class="result-box">RM = {rm_result:,.0f} psi</div>', unsafe_allow_html=True)
                            st.caption(f"**RM** = ({mw_rm} - {sw_rm}) × 0.052 × {wd_rm:,}")
                            st.caption(f"= {mw_rm - sw_rm:.1f} × {0.052 * wd_rm:.0f} = {rm_result:,.0f} psi")
                            if rm_result < 200:
                                st.error("⚠️ RM below minimum 200 psi!")
                            elif rm_result < 400:
                                st.warning("⚠️ RM is low. Typical: 400-600 psi")
                            else:
                                st.success("✅ Adequate riser margin")
                
                else:
                    st.info(f"💡 Use the main Calculator page for detailed calculations of {formula['name']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Create tabs for organized info
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Variables", "📝 Example", "💡 Tips", "ℹ️ Info"])
            
            with tab1:
                st.markdown('<div class="formula-variables">', unsafe_allow_html=True)
                for var, desc in formula['variables'].items():
                    st.markdown(f"**`{var}`** — {desc}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown(f"""
                <div class="formula-example">
                    <pre style="margin: 0; white-space: pre-wrap; font-family: 'Courier New';">{formula['example']}</pre>
                </div>
                """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown(f"""
                <div class="formula-tip">
                    {formula['tip'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
            
            with tab4:
                st.info(f"""
                **Units:** {formula['units']}
                
                **Exam Frequency:** {formula['exam_frequency']}
                
                **Related Formulas:** {', '.join(formula['related']) if formula['related'] else 'None'}
                """)
            
            st.markdown("<br>", unsafe_allow_html=True)

# Show message if no results
if formulas_shown == 0:
    if show_favorites:
        st.warning("📭 No favorites yet! Click the ⭐ icon next to formulas to add them.")
    elif search_term:
        st.warning(f"🔍 No formulas found for '{search_term}'. Try different keywords.")
    else:
        st.info("Select a category or search for formulas.")

# ═══════════════════════════════════════════════════════
# 🔄 FORMULA COMPARISON TABLE (NEW!)
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🔄 Formula Comparison Guide")

tab_comp1, tab_comp2, tab_comp3 = st.tabs(["⚖️ ICP vs FCP", "📊 HP vs BHP vs ECD", "🌊 Surface vs Subsea"])

with tab_comp1:
    st.markdown("""
    | Aspect | ICP (Initial) | FCP (Final) |
    |--------|---------------|-------------|
    | **When** | Start of kill | When kill mud at bit |
    | **Formula** | SIDPP + SCR | SCR × (KMW/OMW) |
    | **Depends on** | Formation pressure | Mud weight ratio |
    | **Typical value** | Higher | Lower (if KMW > OMW slightly) |
    | **Hold constant** | Driller's 1st circ | W&W 2nd part |
    | **Purpose** | Maintain BHP = FP | Maintain BHP with heavy mud |
    
    **💡 Key Point:** ICP → FCP = Linear decrease as kill mud fills string
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **ICP Example:**
        - SIDPP = 500 psi
        - SCR = 400 psi
        - **ICP = 900 psi** ✅
        """)
    
    with col2:
        st.info("""
        **FCP Example:**
        - SCR = 400 psi
        - KMW = 10.5 ppg
        - OMW = 10 ppg
        - **FCP = 420 psi** ✅
        """)

with tab_comp2:
    st.markdown("""
    | Pressure Type | Condition | Formula | When to Use |
    |---------------|-----------|---------|-------------|
    | **HP** | Static (no pumps) | 0.052 × MW × TVD | Basic calculations |
    | **BHP Static** | Same as HP | 0.052 × MW × TVD | Formation balance |
    | **BHP Dynamic** | Circulating | HP + APL | While drilling |
    | **ECD** | Circulating | MW + [APL/(0.052×TVD)] | Fracture check |
    
    **⚡ Critical:**
    - HP = BHP (static only)
    - BHP (circulating) > HP (friction added)
    - ECD > MW (always when pumping)
    - If ECD > Fracture Gradient → LOSSES! ⚠️
    """)

with tab_comp3:
    st.markdown("""
    | Item | Surface Wells | Subsea Wells |
    |------|---------------|--------------|
    | **SICP reading** | Actual pressure | Lower than actual |
    | **Correction** | None needed | ADD Choke Line Friction |
    | **Formula** | SICP (as is) | SICP + CLF |
    | **Riser Margin** | N/A | (MW - Seawater) × 0.052 × WD |
    | **Minimum RM** | N/A | 200 psi (typical: 400-600) |
    
    **🌊 Subsea Special:**
    - Always ADD CLF (choke line friction)
    - Surface reads LESS than reality
    - Maintain riser margin for safety
    """)

# ═══════════════════════════════════════════════════════
# QUICK REFERENCE TABLE
# ═══════════════════════════════════════════════════════

if not search_term and not show_favorites:
    st.markdown("---")
    st.markdown("## 📊 Quick Reference Table")
    
    tab1, tab2 = st.tabs(["📋 All Formulas", "⭐ Most Important"])
    
    with tab1:
        table_data = []
        for category, formulas in FORMULAS.items():
            for f in formulas:
                table_data.append({
                    'Category': category,
                    'Name': f['name'],
                    'Formula': f['formula'],
                    'Importance': f['importance'],
                    'Exam Freq': f['exam_frequency']
                })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="iwcf_formulas_complete.csv",
            mime="text/csv"
        )
    
    with tab2:
        important = [f for formulas in FORMULAS.values() for f in formulas if f['importance'] == "⭐⭐⭐⭐⭐"]
        st.markdown(f"**{len(important)} Critical Formulas - Must Know!**")
        
        for f in important:
            st.markdown(f"""
            <div class="print-card">
                <strong>{f['name']}</strong><br>
                <code>{f['formula']}</code>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📄 PRINTABLE CHEAT SHEET (NEW!)
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📄 Printable Cheat Sheet")

if st.button("📥 Generate Exam Day Cheat Sheet", type="primary", use_container_width=True):
    
    cheat_sheet = """
╔══════════════════════════════════════════════════════════════╗
║        IWCF FORMULAS - EXAM DAY CHEAT SHEET                 ║
║        Created by Eng. Ahmed Elshamy                        ║
╚══════════════════════════════════════════════════════════════╝

🔵 PRESSURE CALCULATIONS (THE BIG 5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HP = 0.052 × MW × TVD
   (Hydrostatic Pressure)

2. FP = SIDPP + (0.052 × OMW × TVD)
   (Formation Pressure)

3. ECD = MW + [APL / (0.052 × TVD)]
   (Equivalent Circulating Density)

4. Gradient = 0.052 × MW
   (Pressure Gradient)

5. BHP(circ) = HP + APL
   (Bottom Hole Pressure - Circulating)

⚡ KILL SHEET (CRITICAL!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. KMW = [SIDPP / (0.052 × TVD)] + OMW
   ⚠️ DON'T FORGET + OMW!

7. ICP = SIDPP + SCR
   (Initial Circulating Pressure)

8. FCP = SCR × (KMW / OMW)
   (Final Circulating Pressure)

9. MAASP = Fracture - (0.052 × MW × Shoe TVD)
   (Max Allowable Annular Surface Pressure)

📐 VOLUME CALCULATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

10. Annular Capacity = (ID² - OD²) / 1029.4
    (bbl/ft)

11. Pipe Capacity = ID² / 1029.4
    (bbl/ft)

12. Volume = Capacity × Length
    (bbls)

🔄 TIME & STROKES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

13. Strokes = Volume / Pump Output

14. Time (min) = Strokes / SPM

💨 GAS BEHAVIOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

15. P₁ × V₁ = P₂ × V₂
    (Boyle's Law - constant temperature)

🌊 SUBSEA (if applicable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

16. True SICP = Surface SICP + CLF
    (ADD choke line friction!)

17. Riser Margin = (MW - 8.6) × 0.052 × Water Depth

🔢 QUICK CONSTANTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 0.052 = Conversion constant (psi/ft per ppg)
• 1029.4 = Volume constant (bbl/ft)
• 0.433 = Water gradient (psi/ft)
• 0.465 = Normal formation gradient (psi/ft)
• 8.6 ppg = Seawater weight
• 42 gal = 1 barrel

⚠️ TOP 5 EXAM MISTAKES TO AVOID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Using MD instead of TVD
❌ Forgetting + OMW in KMW formula
❌ Using SICP instead of SIDPP for FP
❌ Wrong constant (1029 instead of 1029.4)
❌ Forgetting to ADD CLF in subsea

🧠 MEMORY TRICKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Happy Muddy TV" → HP = 0.052 × MW × TVD
"SID Plus Original" → KMW = [...] + OMW
"I Start, F Finish" → ICP starts, FCP finishes
"ADD for Accuracy" → ADD CLF in subsea

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Good Luck! You've got this! 💪
Elshamy IWCF Mastery Method™ - 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Cheat Sheet (TXT)",
            data=cheat_sheet,
            file_name="IWCF_Formulas_CheatSheet.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True
        )
    with col2:
        st.info("💡 Print this and review before your exam!")
    
    st.text_area("Preview:", cheat_sheet, height=400)

# ═══════════════════════════════════════════════════════
# MEMORY AIDS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🧠 Memory Tricks & Mnemonics")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    **🎯 Hydrostatic Pressure**
    
    **"Happy Muddy TV"**
    - **H**P = 0.052 × **M**W × **TV**D
    
    **"Five Two Rule"**
    - 0.052 × 10 = 0.52 psi/ft
    - Multiply depth by 0.52 for 10 ppg
    
    **"Double Nickels"**
    - 10 ppg at 10,000 ft = 5,200 psi
    - (10 × 10 × 52)
    """)
    
    st.info("""
    **🎯 Kill Mud Weight**
    
    **"SID Plus Original"**
    - **SID**PP ÷ constant **+ O**riginal
    - ⚠️ Don't forget the "+O"!
    
    **Two-Step Dance:**
    1. Calculate increase needed
    2. Add to what you had
    """)
    
    st.warning("""
    **🎯 Boyle's Law**
    
    **"PiVi = PiFi"** (like WiFi)
    - P₁V₁ = P₂V₂
    
    **"Pressure Down, Volume Up"**
    - Gas rises → Pressure drops → Volume UP!
    """)

with col2:
    st.info("""
    **🎯 ICP & FCP**
    
    **"I Start, F Finish"**
    - **I**CP = where you **start**
    - **F**CP = where you **finish**
    
    **"SID plus Slow = I go"**
    - SIDPP + SCR = ICP
    
    **"Ratio Rules the F"**
    - FCP = SCR × (Heavy/Light)
    """)
    
    st.success("""
    **🎯 Subsea Wells**
    
    **"ADD for Accuracy"**
    - Always **ADD** choke line friction
    - Surface reads LESS than reality
    
    **"Riser = Cushion"**
    - Riser Margin = Safety cushion
    - Heavy mud - Seawater × depth
    """)
    
    st.warning("""
    **🎯 MAASP**
    
    **"Max Allowed At Shoe Pressure"**
    - Fracture - Hydrostatic = MAASP
    - ⚠️ NEVER exceed this!
    
    **"Break the Shoe, Lose the Show"**
    - Exceed MAASP → Underground blowout
    """)

# ═══════════════════════════════════════════════════════
# COMMON MISTAKES
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## ⚠️ Top 10 Exam Mistakes to Avoid")

mistakes = [
    {"#": 1, "mistake": "Using MD instead of TVD", "correct": "Always use TRUE VERTICAL DEPTH for pressure calculations"},
    {"#": 2, "mistake": "Forgetting 0.052 constant", "correct": "HP = 0.052 × MW × TVD (NOT just MW × TVD)"},
    {"#": 3, "mistake": "Not adding OMW in KMW formula", "correct": "KMW = [SIDPP / ...] + OMW ← Don't forget the + OMW!"},
    {"#": 4, "mistake": "Using SICP for formation pressure", "correct": "Use SIDPP, not SICP (SICP is affected by kick fluid)"},
    {"#": 5, "mistake": "Wrong units (sg instead of ppg)", "correct": "Convert: 1 sg = 8.33 ppg before calculating"},
    {"#": 6, "mistake": "NOT adding CLF in subsea", "correct": "True pressure = Surface + CLF (ADD the friction!)"},
    {"#": 7, "mistake": "Confusing ICP with FCP", "correct": "ICP = Start (SIDPP+SCR), FCP = Finish (ratio based)"},
    {"#": 8, "mistake": "Wrong capacity constant", "correct": "Use 1029.4 for bbl/ft (NOT 1029 or 1030)"},
    {"#": 9, "mistake": "Forgetting Boyle's Law applies", "correct": "P₁V₁ = P₂V₂ for gas expansion (constant temp)"},
    {"#": 10, "mistake": "Using ID for pipe OD", "correct": "Annular: ID (hole) - OD (pipe), NOT ID - ID!"},
]

for m in mistakes:
    with st.expander(f"❌ **Mistake #{m['#']}: {m['mistake']}**"):
        st.success(f"✅ **Correct:** {m['correct']}")

# ═══════════════════════════════════════════════════════
# EXAM TIPS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🎓 Exam Day Formula Tips")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Before the Exam:**
    
    ✅ Memorize the "Big 5":
    1. HP = 0.052 × MW × TVD
    2. KMW = [SIDPP / (0.052 × TVD)] + OMW
    3. ICP = SIDPP + SCR
    4. FCP = SCR × (KMW / OMW)
    5. P₁V₁ = P₂V₂
    
    ✅ Write formulas on scratch paper immediately
    
    ✅ Practice mental math:
    - 0.052 × 10 = 0.52
    - 0.052 × 12 = 0.624
    """)

with col2:
    st.warning("""
    **During the Exam:**
    
    ⚡ **Always:**
    - Write formula first
    - Substitute values
    - Show your work
    - Include units
    
    ⏰ **Time Management:**
    - Quick questions first
    - Flag hard calculations
    - Return to flagged items
    
    🔍 **Double Check:**
    - TVD vs MD?
    - Correct constant?
    - Units match?
    - Answer reasonable?
    """)

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">
        🎓 Elshamy IWCF Mastery Method™
    </p>
    <p style="margin: 0.5rem 0;">
        Complete Formulas Reference Guide • IWCF 2026 Standards
    </p>
    <p style="margin: 1rem 0 0 0; font-size: 0.9rem;">
        Created by <strong>Eng. Ahmed Elshamy</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; font-style: italic;">
        "Master the formulas, master the exam" 💪
    </p>
</div>
""", unsafe_allow_html=True)