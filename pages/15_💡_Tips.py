import streamlit as st
from datetime import datetime
import random

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Tips & Tricks - IWCF Mastery",
    page_icon="💡",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .tips-header {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }
    
    .tip-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .tip-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .tip-gold {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-left: 5px solid #F59E0B;
    }
    
    .tip-exam {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        border-left: 5px solid #EF4444;
    }
    
    .tip-memory {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        border-left: 5px solid #3B82F6;
    }
    
    .tip-calculation {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border-left: 5px solid #10B981;
    }
    
    .tip-time {
        background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
        border-left: 5px solid #7C3AED;
    }
    
    .trick-box {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #F59E0B;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .quote-box {
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        font-style: italic;
    }
    
    .category-section {
        background: #F9FAFB;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .stat-badge {
        display: inline-block;
        background: #EF4444;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .do-box {
        background: #D1FAE5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        margin: 0.5rem 0;
    }
    
    .dont-box {
        background: #FEE2E2;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #EF4444;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 💡 TIPS & TRICKS DATA
# ═══════════════════════════════════════════════════════

EXAM_TIPS = [
    {
        "title": "Read Questions Twice",
        "icon": "👀",
        "content": "Always read the question at least twice before answering. Look for keywords like 'EXCEPT', 'NOT', 'ALWAYS', 'NEVER'. These change the entire meaning!",
        "category": "exam"
    },
    {
        "title": "Time Management is Key",
        "icon": "⏰",
        "content": "Allocate your time wisely:\n• Quick scan: 2 minutes\n• Easy questions first: 30-40 minutes\n• Difficult questions: Return later\n• Review: Last 10 minutes\n\nDon't spend more than 2 minutes on any single question on first pass.",
        "category": "time"
    },
    {
        "title": "Use Process of Elimination",
        "icon": "❌",
        "content": "In multiple choice:\n1. Cross out obviously wrong answers\n2. Choose from remaining options\n3. Trust your first instinct (usually correct)\n4. Don't overthink!\n\nEven eliminating one wrong answer increases your chances by 33%!",
        "category": "exam"
    },
    {
        "title": "Never Leave Blank Answers",
        "icon": "✍️",
        "content": "Even if you're not sure, make an educated guess. No penalty for wrong answers in most IWCF exams. 25% chance is better than 0%!",
        "category": "exam"
    },
    {
        "title": "Flag for Review",
        "icon": "🚩",
        "content": "Use the flag/bookmark feature for questions you're unsure about. Come back to them after finishing easier ones. Fresh perspective helps!",
        "category": "exam"
    }
]

CALCULATION_TRICKS = [
    {
        "title": "Quick HP Mental Math",
        "icon": "🧮",
        "content": "For 10 ppg mud: Multiply depth by 0.52\nFor 12 ppg mud: Multiply depth by 0.624\n\nExample: 8,000 ft × 0.52 = 4,160 psi (for 10 ppg)\n\nThis saves time during exams!",
        "category": "calculation"
    },
    {
        "title": "KMW Quick Check",
        "icon": "✅",
        "content": "After calculating KMW, ask yourself:\n• Is it higher than OMW? (Must be!)\n• Is the increase reasonable? (Usually 0.5-2 ppg)\n• Does it exceed formation breakdown? (Check MAASP!)\n\nIf any answer is 'no', recheck your calculation!",
        "category": "calculation"
    },
    {
        "title": "Write Down the Formula First",
        "icon": "📝",
        "content": "Before calculating:\n1. Write the formula\n2. Write what you know\n3. Write what you're solving for\n4. Calculate\n5. Check units\n\nThis prevents silly mistakes and helps if you get stuck!",
        "category": "calculation"
    },
    {
        "title": "Double-Check Units",
        "icon": "📏",
        "content": "Common unit mistakes:\n• psi vs bar (1 bar ≈ 14.5 psi)\n• ppg vs kg/m³\n• ft vs m\n• bbl vs m³\n\nAlways verify your answer is in the requested units!",
        "category": "calculation"
    },
    {
        "title": "Rounding Rules",
        "icon": "🔢",
        "content": "For KMW: Always round UP to nearest 0.5 ppg\nFor pressures: Round to nearest whole number\nFor volumes: One decimal place is enough\n\nExample: KMW = 11.23 → Use 11.5 ppg (safety margin)",
        "category": "calculation"
    }
]

MEMORY_TRICKS = [
    {
        "title": "KICK Detection Mnemonic",
        "icon": "🧠",
        "content": "PRIMARY signs = 'PIT FLOW DRILL'\n\n• **P**it gain\n• **I**ncrease in flow rate\n• **T**otal flow (with pumps off)\n• **F**ast drilling (drilling break)\n• **L**ow pump pressure\n• **O**dd cuttings\n• **W**ater/gas cut\n\nRemember: First 4 are CRITICAL - act within 30 seconds!",
        "category": "memory"
    },
    {
        "title": "BOP Stack from Top",
        "icon": "🛡️",
        "content": "Remember: 'A Pizza Boy Brings Cheese'\n\n• **A**nnular (top)\n• **P**ipe Rams\n• **B**lind/Shear Rams\n• **B**ackup Pipe Rams\n• **C**hoke & Kill Lines (bottom)\n\nAlways close Annular first in normal situations!",
        "category": "memory"
    },
    {
        "title": "Kill Methods Choice",
        "icon": "🎯",
        "content": "Remember: 'DEWS'\n\n**D**riller's = **D**on't have kill mud ready\n**E**asy crew\n**W**ait & Weight = **W**ell experienced crew\n**S**peedy (one circulation)\n\nChoose based on situation, crew, and mud availability!",
        "category": "memory"
    },
    {
        "title": "Subsea Differences",
        "icon": "🌊",
        "content": "Remember: 'CLR'\n\n• **C**LF - Always ADD to surface readings\n• **L**ower MAASP than surface wells\n• **R**iser Margin - Must maintain 400-600 psi\n\nSubsea = More complex, more careful!",
        "category": "memory"
    },
    {
        "title": "Kick Type Identification",
        "icon": "⚠️",
        "content": "Remember: 'GAS > OIL > WATER'\n\nSICP comparison to SIDPP:\n• **G**as: SICP **>** SIDPP (lightest)\n• **O**il: SICP **≈** SIDPP (medium)\n• **W**ater: SICP **<** SIDPP (heaviest)\n\nGas is most dangerous - migrates and expands!",
        "category": "memory"
    }
]

STUDY_TIPS = [
    {
        "title": "Active Recall > Passive Reading",
        "icon": "📚",
        "content": "Don't just read - TEST yourself!\n\n✅ DO:\n• Close the book and recall\n• Solve practice questions\n• Teach concepts to someone\n• Use flashcards actively\n\n❌ DON'T:\n• Just highlight text\n• Read without testing\n• Copy notes mindlessly",
        "category": "memory"
    },
    {
        "title": "Pomodoro Technique",
        "icon": "🍅",
        "content": "Study in focused bursts:\n\n1. Study: 25 minutes (100% focus)\n2. Break: 5 minutes (walk, water)\n3. Repeat 4 times\n4. Long break: 15-30 minutes\n\nThis prevents burnout and improves retention!",
        "category": "time"
    },
    {
        "title": "Practice Under Exam Conditions",
        "icon": "📝",
        "content": "Take mock exams seriously:\n\n✅ DO:\n• Set timer (strict!)\n• No notes/books\n• Complete in one sitting\n• Realistic environment\n\n❌ DON'T:\n• Pause and look up answers\n• Take breaks during exam\n• Use calculator for mental math",
        "category": "exam"
    },
    {
        "title": "Review Mistakes Immediately",
        "icon": "🔍",
        "content": "After each quiz/exam:\n\n1. Review WRONG answers first\n2. Understand WHY you got it wrong\n3. Write the correct answer\n4. Redo the question next day\n\nLearn from mistakes - they're your best teachers!",
        "category": "gold"
    },
    {
        "title": "Sleep is Non-Negotiable",
        "icon": "😴",
        "content": "Your brain consolidates learning during sleep!\n\n✅ DO:\n• Sleep 7-8 hours\n• Consistent sleep schedule\n• Review before bed\n• No all-nighters!\n\n❌ DON'T:\n• Stay up late studying\n• Sacrifice sleep for extra hour\n• Use caffeine excessively\n\nWell-rested brain > Tired brain with more hours!",
        "category": "gold"
    }
]

GOLDEN_RULES = [
    "Always use TVD, never MD in calculations",
    "Add CLF to surface readings in subsea operations",
    "Never leave exam answers blank - guess if needed",
    "Double-check that KMW > OMW (always!)",
    "Shut in well within 30 seconds of kick detection",
    "Read 'EXCEPT' and 'NOT' carefully in questions",
    "Shear rams = LAST RESORT only",
    "SICP must always be < MAASP",
    "Maintain riser margin 400-600 psi (subsea)",
    "Round KMW UP for safety margin"
]

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="tips-header">
    <h1>💡 Expert Tips & Tricks</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Insider secrets, exam hacks, and proven strategies
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Learn smarter, not harder - Master IWCF like a pro!
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎯 DAILY TIP
# ═══════════════════════════════════════════════════════

st.markdown("## 🌟 Tip of the Day")

# Random daily tip
random.seed(datetime.now().strftime("%Y-%m-%d"))
all_tips = EXAM_TIPS + CALCULATION_TRICKS + MEMORY_TRICKS + STUDY_TIPS
daily_tip = random.choice(all_tips)

st.markdown(f"""
<div class="quote-box">
    <div style="font-size: 3rem; margin-bottom: 1rem;">{daily_tip['icon']}</div>
    <h2 style="margin: 0;">{daily_tip['title']}</h2>
    <p style="margin-top: 1rem; font-size: 1.1rem; opacity: 0.9;">
        {daily_tip['content'].replace(chr(10), '<br>')}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🏆 GOLDEN RULES
# ═══════════════════════════════════════════════════════

st.markdown("## 🏆 Golden Rules - Never Forget!")

st.markdown("""
<div class="category-section">
    <h3 style="color: #F59E0B; margin: 0 0 1rem 0;">⭐ The 10 Commandments of IWCF</h3>
    <p style="color: #6B7280; margin-bottom: 1.5rem;">
        Memorize these - they'll save you in the exam!
    </p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(2)

for idx, rule in enumerate(GOLDEN_RULES):
    with cols[idx % 2]:
        st.markdown(f"""
        <div class="trick-box">
            <strong style="color: #F59E0B;">{idx + 1}.</strong> {rule}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📝 EXAM TIPS
# ═══════════════════════════════════════════════════════

st.markdown("## 📝 Exam Success Tips")

for tip in EXAM_TIPS:
    st.markdown(f"""
    <div class="tip-card tip-{tip['category']}">
        <h3 style="margin: 0; color: #1F2937;">
            {tip['icon']} {tip['title']}
            <span class="stat-badge">HIGH IMPACT</span>
        </h3>
        <p style="margin-top: 1rem; color: #374151; line-height: 1.8;">
            {tip['content'].replace(chr(10), '<br>')}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🧮 CALCULATION SHORTCUTS
# ═══════════════════════════════════════════════════════

st.markdown("## 🧮 Calculation Shortcuts")

for trick in CALCULATION_TRICKS:
    st.markdown(f"""
    <div class="tip-card tip-calculation">
        <h3 style="margin: 0; color: #1F2937;">
            {trick['icon']} {trick['title']}
        </h3>
        <p style="margin-top: 1rem; color: #374151; line-height: 1.8; font-family: 'Courier New', monospace;">
            {trick['content'].replace(chr(10), '<br>')}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🧠 MEMORY TRICKS
# ═══════════════════════════════════════════════════════

st.markdown("## 🧠 Memory Tricks & Mnemonics")

for trick in MEMORY_TRICKS:
    st.markdown(f"""
    <div class="tip-card tip-memory">
        <h3 style="margin: 0; color: #1F2937;">
            {trick['icon']} {trick['title']}
        </h3>
        <p style="margin-top: 1rem; color: #374151; line-height: 1.8;">
            {trick['content'].replace(chr(10), '<br>')}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📚 STUDY STRATEGIES
# ═══════════════════════════════════════════════════════

st.markdown("## 📚 Proven Study Strategies")

for tip in STUDY_TIPS:
    st.markdown(f"""
    <div class="tip-card tip-gold">
        <h3 style="margin: 0; color: #1F2937;">
            {tip['icon']} {tip['title']}
        </h3>
        <p style="margin-top: 1rem; color: #374151; line-height: 1.8;">
            {tip['content'].replace(chr(10), '<br>')}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# ✅ DO'S AND DON'TS
# ═══════════════════════════════════════════════════════

st.markdown("## ✅ Do's and ❌ Don'ts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ DO These")
    
    dos = [
        "Practice 20+ questions daily",
        "Review mistakes immediately",
        "Use all practice tools (quiz, scenarios, flashcards)",
        "Sleep 7-8 hours before exam",
        "Arrive 30 minutes early",
        "Read questions twice",
        "Start with easy questions",
        "Flag difficult questions for review",
        "Double-check calculations",
        "Trust your preparation"
    ]
    
    for do in dos:
        st.markdown(f"""
        <div class="do-box">
            ✅ {do}
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### ❌ DON'T Do These")
    
    donts = [
        "Cram the night before",
        "Skip practice exams",
        "Only read without testing",
        "Leave answers blank",
        "Spend too long on one question",
        "Change answers (unless very sure)",
        "Panic if you don't know something",
        "Compare with others during exam",
        "Use MD instead of TVD",
        "Forget to add CLF in subsea"
    ]
    
    for dont in donts:
        st.markdown(f"""
        <div class="dont-box">
            ❌ {dont}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# ⏰ EXAM DAY CHECKLIST
# ═══════════════════════════════════════════════════════

st.markdown("## ⏰ Exam Day Checklist")

st.markdown("""
<div class="category-section">
    <h3 style="color: #EF4444; margin: 0 0 1rem 0;">📋 The Night Before</h3>
</div>
""", unsafe_allow_html=True)

checklist_before = [
    ("Review cheat sheets (30 min)", "📄"),
    ("Quick flashcard review (20 min)", "🎴"),
    ("Light dinner, no heavy food", "🍽️"),
    ("Prepare documents & calculator", "📝"),
    ("Set 2 alarms", "⏰"),
    ("Sleep by 10 PM", "😴"),
    ("No late-night cramming!", "🚫")
]

for item, icon in checklist_before:
    st.checkbox(f"{icon} {item}", key=f"before_{item}")

st.markdown("""
<div class="category-section">
    <h3 style="color: #10B981; margin: 0 0 1rem 0;">🌅 Exam Morning</h3>
</div>
""", unsafe_allow_html=True)

checklist_morning = [
    ("Wake up 3 hours before exam", "⏰"),
    ("Eat good breakfast", "🥐"),
    ("Review golden rules (10 min)", "🏆"),
    ("Arrive 30 min early", "🚗"),
    ("Use bathroom", "🚻"),
    ("Turn off phone", "📱"),
    ("Take deep breaths", "🧘"),
    ("Stay confident!", "💪")
]

for item, icon in checklist_morning:
    st.checkbox(f"{icon} {item}", key=f"morning_{item}")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 💬 MOTIVATIONAL QUOTES
# ═══════════════════════════════════════════════════════

st.markdown("## 💬 Words of Wisdom")

quotes = [
    {"text": "Success is the sum of small efforts repeated day in and day out", "author": "Robert Collier"},
    {"text": "The expert in anything was once a beginner", "author": "Helen Hayes"},
    {"text": "It's not about being the best. It's about being better than you were yesterday", "author": "Unknown"},
    {"text": "Study while others are sleeping; work while others are relaxing", "author": "William A. Ward"},
    {"text": "Your limitation—it's only your imagination", "author": "Unknown"}
]

selected_quote = random.choice(quotes)

st.markdown(f"""
<div class="quote-box">
    <div style="font-size: 2.5rem; margin-bottom: 1rem;">💭</div>
    <h3 style="margin: 0; font-style: italic;">"{selected_quote['text']}"</h3>
    <p style="margin-top: 1rem; opacity: 0.8;">— {selected_quote['author']}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🚀 FINAL MESSAGE
# ═══════════════════════════════════════════════════════

st.markdown("## 🎓 Final Message from Eng. Elshamy")

st.markdown("""
<div style="background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%); 
            padding: 2rem; border-radius: 15px; color: white;">
    <h3 style="margin: 0;">Dear Future IWCF Professional,</h3>
    <p style="margin-top: 1rem; line-height: 1.8; font-size: 1.05rem;">
        You've made it this far, which means you're serious about your success. Remember:
    </p>
    <ul style="margin-top: 1rem; line-height: 2;">
        <li>📚 <strong>Consistent effort</strong> beats last-minute cramming</li>
        <li>🎯 <strong>Understanding</strong> beats memorization</li>
        <li>💪 <strong>Practice</strong> beats theory alone</li>
        <li>✅ <strong>Belief in yourself</strong> beats doubt</li>
    </ul>
    <p style="margin-top: 1.5rem; font-size: 1.1rem;">
        You have all the tools. You have the knowledge. You have the preparation.
    </p>
    <p style="margin-top: 0.5rem; font-size: 1.3rem; font-weight: bold;">
        Now go ace that exam! 🚀
    </p>
    <p style="margin-top: 1.5rem; text-align: right; opacity: 0.9;">
        — Eng. Ahmed Elshamy<br>
        <span style="font-size: 0.9rem;">"Your Success is My Mission"</span>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎯 QUICK ACTIONS
# ═══════════════════════════════════════════════════════

st.markdown("## 🎯 Ready to Apply These Tips?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Start Learning", use_container_width=True, type="primary"):
        st.switch_page("pages/01_📚_Learn.py")

with col2:
    if st.button("❓ Practice Quiz", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")

with col3:
    if st.button("📝 Mock Exam", use_container_width=True):
        st.switch_page("pages/03_📝_Mock_Exam.py")

with col4:
    if st.button("🎴 Flashcards", use_container_width=True):
        st.switch_page("pages/08_🎴_Flashcards.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        💡 <strong>Elshamy IWCF Mastery Method™ - Tips & Tricks</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Smart work beats hard work - Work smart AND hard!" 🎯
    </p>
</div>
""", unsafe_allow_html=True)