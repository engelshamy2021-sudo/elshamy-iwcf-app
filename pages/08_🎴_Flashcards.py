import streamlit as st
import random
from datetime import datetime

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Flashcards - IWCF Mastery",
    page_icon="🎴",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .flashcard-header {
        background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    .flashcard {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        transition: all 0.6s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .flashcard-front {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
    }
    
    .flashcard-back {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: white;
    }
    
    .flashcard:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
    }
    
    .card-content {
        font-size: 1.4rem;
        line-height: 1.8;
    }
    
    .card-label {
        position: absolute;
        top: 1rem;
        left: 1rem;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    
    .card-number {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #7C3AED;
    }
    
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .category-badge:hover {
        transform: translateY(-2px);
    }
    
    .progress-ring {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: conic-gradient(#10B981 var(--progress), #E5E7EB 0);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    
    .progress-ring-inner {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #1F2937;
    }
    
    .action-btn {
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .action-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    .know-btn {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
    }
    
    .dont-know-btn {
        background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
        color: white;
    }
    
    .hint-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #F59E0B;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎴 FLASHCARDS DATA
# ═══════════════════════════════════════════════════════

FLASHCARDS = {
    "Pressure Basics": [
        {
            "question": "What is the formula for Hydrostatic Pressure?",
            "answer": "HP = 0.052 × MW × TVD\n\nWhere:\n• HP = Hydrostatic Pressure (psi)\n• MW = Mud Weight (ppg)\n• TVD = True Vertical Depth (ft)",
            "hint": "Think: 0.052 is the conversion constant"
        },
        {
            "question": "What is Formation Pressure?",
            "answer": "The pressure exerted by fluids within the pore spaces of a formation.\n\nAlso called: Pore Pressure\n\nNormal gradient: 0.433 - 0.465 psi/ft",
            "hint": "Fluids trapped in rock pores"
        },
        {
            "question": "What is Overbalance?",
            "answer": "When Hydrostatic Pressure > Formation Pressure\n\n✅ This is the normal, safe drilling condition\n\n⚠️ Too much overbalance can cause:\n• Lost circulation\n• Differential sticking\n• Formation damage",
            "hint": "HP > FP = Safe"
        },
        {
            "question": "What is Underbalance?",
            "answer": "When Formation Pressure > Hydrostatic Pressure\n\n⚠️ This is dangerous!\n\n❌ Can cause:\n• Kick\n• Blowout if not controlled",
            "hint": "FP > HP = Danger!"
        },
        {
            "question": "What is Pressure Gradient?",
            "answer": "The rate of pressure change per unit of depth.\n\n• Water: 0.433 psi/ft\n• Normal formation: 0.433-0.465 psi/ft\n• Abnormal (over): > 0.465 psi/ft\n• Subnormal: < 0.433 psi/ft",
            "hint": "Pressure per foot of depth"
        }
    ],
    
    "Kill Methods": [
        {
            "question": "What are the main Kill Methods?",
            "answer": "1️⃣ Driller's Method\n   - Two circulations\n   - Simple but longer\n\n2️⃣ Wait & Weight Method\n   - One circulation\n   - Faster but complex\n\n3️⃣ Concurrent Method\n   - Combination of both",
            "hint": "Think: D, W&W, C"
        },
        {
            "question": "What is the formula for ICP?",
            "answer": "ICP = SIDPP + SCR\n\nWhere:\n• ICP = Initial Circulating Pressure\n• SIDPP = Shut-In Drill Pipe Pressure\n• SCR = Slow Circulating Rate pressure",
            "hint": "Start pressure = Kick pressure + Pump pressure"
        },
        {
            "question": "What is the formula for FCP?",
            "answer": "FCP = SCR × (KMW ÷ OMW)\n\nWhere:\n• FCP = Final Circulating Pressure\n• SCR = Slow Circulating Rate\n• KMW = Kill Mud Weight\n• OMW = Original Mud Weight",
            "hint": "Final pressure uses ratio of weights"
        },
        {
            "question": "What is the formula for Kill Mud Weight?",
            "answer": "KMW = OMW + (SIDPP ÷ (0.052 × TVD))\n\nOr:\nKMW = OMW + (SIDPP ÷ HP per ppg)\n\n⚠️ Don't forget to add Safety Margin (+0.5 ppg)",
            "hint": "Original + Extra needed"
        },
        {
            "question": "When to use Driller's Method?",
            "answer": "✅ Use when:\n• Kill mud NOT available immediately\n• Less experienced crew\n• Simple kick situation\n• Time to prepare KMW needed\n\n❌ Not ideal when:\n• Weak formation at shoe\n• Time is critical",
            "hint": "Kill mud not ready? Use Driller's"
        },
        {
            "question": "When to use Wait & Weight Method?",
            "answer": "✅ Use when:\n• Kill mud available quickly\n• Experienced crew\n• Formation is weak\n• Time is critical\n\n❌ Not ideal when:\n• Crew inexperienced\n• Complex calculations difficult",
            "hint": "Kill mud ready? Use W&W"
        }
    ],
    
    "Kick Detection": [
        {
            "question": "What are the PRIMARY Kick Signs?",
            "answer": "🚨 PRIMARY SIGNS (Act immediately!):\n\n1. Pit Gain (increase in mud volume)\n2. Flow Rate Increase\n3. Flow with Pumps Off\n4. Sudden Drilling Break",
            "hint": "Volume or flow changes = Primary"
        },
        {
            "question": "What are the SECONDARY Kick Signs?",
            "answer": "⚠️ SECONDARY SIGNS:\n\n1. Pump Pressure Decrease\n2. Pump Stroke Increase\n3. Cut Mud (gas/water cut)\n4. Change in cuttings\n5. Chloride content increase",
            "hint": "Pressure or mud property changes"
        },
        {
            "question": "What causes a Kick?",
            "answer": "Main causes:\n\n1. Underbalance (HP < FP)\n2. Swabbing while tripping\n3. Lost Circulation\n4. Insufficient mud weight\n5. Not filling hole while tripping\n6. Abnormal pressure zones",
            "hint": "Anything that reduces HP or enters high pressure"
        },
        {
            "question": "What is Swabbing?",
            "answer": "Reduction in bottom hole pressure caused by pulling pipe too fast.\n\n⚠️ Creates temporary underbalance\n\n⚠️ Can cause kick\n\n✅ Prevention:\n• Pull slowly\n• Use proper trip margin\n• Monitor flow",
            "hint": "Pulling pipe = Sucking effect"
        }
    ],
    
    "BOP Equipment": [
        {
            "question": "What are the main BOP components?",
            "answer": "1️⃣ Annular Preventer (top)\n   - Closes on any shape\n\n2️⃣ Pipe Rams\n   - Close on specific pipe size\n\n3️⃣ Blind Rams\n   - Close open hole\n\n4️⃣ Shear Rams\n   - Cut pipe and seal (emergency)",
            "hint": "A-P-B-S from top"
        },
        {
            "question": "How often to Function Test BOP?",
            "answer": "Function Test: Every 7 days\n\n(Some regulations: 14 days)\n\n✅ Test all components\n✅ No pressure required\n✅ Check opening/closing",
            "hint": "Weekly function test"
        },
        {
            "question": "How often to Pressure Test BOP?",
            "answer": "Pressure Test:\n\n• After installation\n• After repairs\n• Every 21 days\n• When required by regulations\n\nTest to rated working pressure",
            "hint": "21 days or after changes"
        },
        {
            "question": "When to use Shear Rams?",
            "answer": "⚠️ LAST RESORT ONLY!\n\nUse when:\n• All other options failed\n• Emergency disconnect needed\n• Abandoning well\n\n❌ Destroys drill pipe\n❌ Very expensive\n❌ Only for emergencies",
            "hint": "Emergency only - cuts pipe!"
        }
    ],
    
    "Subsea Operations": [
        {
            "question": "What is Choke Line Friction (CLF)?",
            "answer": "Pressure loss due to friction in the long choke line from seabed to surface.\n\n⚠️ Must ADD CLF to surface readings!\n\nTrue SICP = Surface SICP + CLF",
            "hint": "Long line = Friction loss"
        },
        {
            "question": "What is Riser Margin?",
            "answer": "Extra mud weight to keep riser full if disconnected.\n\nFormula:\nRM = (MW - Seawater) × 0.052 × Water Depth\n\nMinimum: 200 psi\nRecommended: 400-600 psi",
            "hint": "Safety for disconnect"
        },
        {
            "question": "What is MAASP?",
            "answer": "Maximum Allowable Annular Surface Pressure\n\nThe maximum pressure allowed at surface before breaking formation at shoe.\n\n⚠️ SICP must always be < MAASP\n\n❌ Exceeding causes underground blowout",
            "hint": "Maximum safe surface pressure"
        },
        {
            "question": "What is the weak point in Subsea wells?",
            "answer": "Usually the WELLHEAD (not shoe)\n\n⚠️ In subsea:\n• Wellhead rating may be limiting\n• Seawater reduces HP\n• MAASP is lower\n\n✅ Always check both shoe AND wellhead",
            "hint": "Wellhead, not always shoe"
        }
    ]
}

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'current_category' not in st.session_state:
    st.session_state.current_category = None

if 'current_card_index' not in st.session_state:
    st.session_state.current_card_index = 0

if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

if 'cards_known' not in st.session_state:
    st.session_state.cards_known = []

if 'cards_unknown' not in st.session_state:
    st.session_state.cards_unknown = []

if 'session_cards' not in st.session_state:
    st.session_state.session_cards = []

if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False

if 'study_mode' not in st.session_state:
    st.session_state.study_mode = "normal"  # normal, shuffle, unknown_only

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="flashcard-header">
    <h1>🎴 Flashcards - Quick Review</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Master IWCF concepts with interactive flashcards
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Click card to flip • Swipe through categories • Track your progress
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 STATS
# ═══════════════════════════════════════════════════════

total_cards = sum(len(cards) for cards in FLASHCARDS.values())
known_count = len(st.session_state.cards_known)
unknown_count = len(st.session_state.cards_unknown)
mastery = (known_count / total_cards * 100) if total_cards > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #7C3AED; margin: 0;">📚 {total_cards}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Total Cards</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #10B981; margin: 0;">✅ {known_count}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Mastered</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #EF4444; margin: 0;">🔄 {unknown_count}</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Need Review</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="color: #F59E0B; margin: 0;">🎯 {mastery:.0f}%</h3>
        <p style="color: #6B7280; margin-top: 0.5rem;">Mastery</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📂 CATEGORY SELECTION
# ═══════════════════════════════════════════════════════

if st.session_state.current_category is None:
    st.markdown("## 📂 Choose a Category")
    st.markdown("*Select a topic to start reviewing flashcards*")
    
    # Category cards
    cols = st.columns(3)
    
    category_colors = {
        "Pressure Basics": "#3B82F6",
        "Kill Methods": "#10B981",
        "Kick Detection": "#EF4444",
        "BOP Equipment": "#F59E0B",
        "Subsea Operations": "#8B5CF6"
    }
    
    category_icons = {
        "Pressure Basics": "📊",
        "Kill Methods": "🎯",
        "Kick Detection": "⚠️",
        "BOP Equipment": "🛡️",
        "Subsea Operations": "🌊"
    }
    
    for idx, (category, cards) in enumerate(FLASHCARDS.items()):
        with cols[idx % 3]:
            color = category_colors.get(category, "#7C3AED")
            icon = category_icons.get(category, "📚")
            
            # Count known cards in this category
            known_in_cat = sum(1 for c in st.session_state.cards_known if c.startswith(category))
            cat_progress = (known_in_cat / len(cards) * 100) if cards else 0
            
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                        border-top: 5px solid {color}; margin: 1rem 0;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; color: #1F2937;">{icon} {category}</h3>
                <p style="color: #6B7280; margin: 0.5rem 0;">{len(cards)} cards</p>
                <div style="background: #E5E7EB; height: 8px; border-radius: 4px; margin: 0.5rem 0;">
                    <div style="background: {color}; height: 100%; width: {cat_progress}%; border-radius: 4px;"></div>
                </div>
                <p style="color: {color}; font-weight: 600; margin: 0;">{cat_progress:.0f}% mastered</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📖 Study {category}", key=f"cat_{idx}", use_container_width=True):
                st.session_state.current_category = category
                st.session_state.current_card_index = 0
                st.session_state.show_answer = False
                st.session_state.session_cards = list(range(len(cards)))
                st.rerun()
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔀 Random Category", use_container_width=True):
            random_cat = random.choice(list(FLASHCARDS.keys()))
            st.session_state.current_category = random_cat
            st.session_state.current_card_index = 0
            st.session_state.session_cards = list(range(len(FLASHCARDS[random_cat])))
            random.shuffle(st.session_state.session_cards)
            st.rerun()
    
    with col2:
        if st.button("📚 All Cards Shuffled", use_container_width=True):
            st.info("Coming soon! Study all cards mixed together.")
    
    with col3:
        if st.button("🔄 Review Unknown Only", use_container_width=True):
            if st.session_state.cards_unknown:
                st.info("Coming soon! Review only cards you marked as unknown.")
            else:
                st.success("Great! No unknown cards to review! 🎉")

# ═══════════════════════════════════════════════════════
# 🎴 FLASHCARD STUDY MODE
# ═══════════════════════════════════════════════════════

else:
    category = st.session_state.current_category
    cards = FLASHCARDS[category]
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to Categories"):
            st.session_state.current_category = None
            st.session_state.show_answer = False
            st.session_state.show_hint = False
            st.rerun()
    
    with col2:
        st.markdown(f"### 📂 {category}")
    
    with col3:
        if st.button("🔀 Shuffle Cards"):
            random.shuffle(st.session_state.session_cards)
            st.session_state.current_card_index = 0
            st.session_state.show_answer = False
            st.rerun()
    
    st.markdown("---")
    
    # Current card
    if st.session_state.session_cards:
        actual_index = st.session_state.session_cards[st.session_state.current_card_index]
        current_card = cards[actual_index]
        card_id = f"{category}::{actual_index}"
        
        is_known = card_id in st.session_state.cards_known
        
        # Card display
        if not st.session_state.show_answer:
            # Question side
            st.markdown(f"""
            <div class="flashcard flashcard-front">
                <span class="card-label">❓ Question</span>
                <span class="card-number">{st.session_state.current_card_index + 1}/{len(st.session_state.session_cards)}</span>
                <div class="card-content">
                    <strong>{current_card['question']}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hint
            if st.session_state.show_hint:
                st.markdown(f"""
                <div class="hint-box">
                    💡 <strong>Hint:</strong> {current_card.get('hint', 'No hint available')}
                </div>
                """, unsafe_allow_html=True)
            
            # Actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💡 Show Hint", use_container_width=True):
                    st.session_state.show_hint = not st.session_state.show_hint
                    st.rerun()
            
            with col2:
                if st.button("🔄 Flip Card", use_container_width=True, type="primary"):
                    st.session_state.show_answer = True
                    st.session_state.show_hint = False
                    st.rerun()
            
            with col3:
                if st.button("⏭️ Skip", use_container_width=True):
                    st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(st.session_state.session_cards)
                    st.session_state.show_hint = False
                    st.rerun()
        
        else:
            # Answer side
            st.markdown(f"""
            <div class="flashcard flashcard-back">
                <span class="card-label">✅ Answer</span>
                <span class="card-number">{st.session_state.current_card_index + 1}/{len(st.session_state.session_cards)}</span>
                <div class="card-content">
                    {current_card['answer'].replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Did you know this?")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ I Knew It!", use_container_width=True, type="primary"):
                    if card_id not in st.session_state.cards_known:
                        st.session_state.cards_known.append(card_id)
                    if card_id in st.session_state.cards_unknown:
                        st.session_state.cards_unknown.remove(card_id)
                    
                    st.session_state.show_answer = False
                    st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(st.session_state.session_cards)
                    st.rerun()
            
            with col2:
                if st.button("🔄 Flip Back", use_container_width=True):
                    st.session_state.show_answer = False
                    st.rerun()
            
            with col3:
                if st.button("❌ Need More Practice", use_container_width=True):
                    if card_id not in st.session_state.cards_unknown:
                        st.session_state.cards_unknown.append(card_id)
                    if card_id in st.session_state.cards_known:
                        st.session_state.cards_known.remove(card_id)
                    
                    st.session_state.show_answer = False
                    st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(st.session_state.session_cards)
                    st.rerun()
        
        # Navigation
        st.markdown("---")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⏮️ First", use_container_width=True):
                st.session_state.current_card_index = 0
                st.session_state.show_answer = False
                st.rerun()
        
        with col2:
            if st.button("◀️ Previous", use_container_width=True):
                st.session_state.current_card_index = (st.session_state.current_card_index - 1) % len(st.session_state.session_cards)
                st.session_state.show_answer = False
                st.rerun()
        
        with col3:
            st.markdown(f"**Card {st.session_state.current_card_index + 1} of {len(st.session_state.session_cards)}**")
        
        with col4:
            if st.button("▶️ Next", use_container_width=True):
                st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(st.session_state.session_cards)
                st.session_state.show_answer = False
                st.rerun()
        
        with col5:
            if st.button("⏭️ Last", use_container_width=True):
                st.session_state.current_card_index = len(st.session_state.session_cards) - 1
                st.session_state.show_answer = False
                st.rerun()
        
        # Progress for this category
        st.markdown("---")
        
        known_in_cat = sum(1 for c in st.session_state.cards_known if c.startswith(category))
        cat_progress = (known_in_cat / len(cards) * 100) if cards else 0
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <p style="margin: 0 0 0.5rem 0;"><strong>Category Progress: {cat_progress:.0f}%</strong></p>
            <div style="background: #E5E7EB; height: 10px; border-radius: 5px;">
                <div style="background: linear-gradient(90deg, #10B981 0%, #34D399 100%); height: 100%; width: {cat_progress}%; border-radius: 5px;"></div>
            </div>
            <p style="margin: 0.5rem 0 0 0; color: #6B7280; font-size: 0.9rem;">
                {known_in_cat} of {len(cards)} cards mastered
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
        🎴 <strong>Elshamy IWCF Mastery Method™ - Flashcards</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Repetition is the mother of learning" 📚
    </p>
</div>
""", unsafe_allow_html=True)