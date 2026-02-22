import streamlit as st
from datetime import datetime, timedelta
import random

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Achievements - IWCF Mastery",
    page_icon="🏆",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .achievement-header {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid #F59E0B;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .level-card {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(30, 64, 175, 0.3);
    }
    
    .badge-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .badge-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .badge-card.locked {
        opacity: 0.5;
        filter: grayscale(100%);
    }
    
    .badge-card.unlocked {
        border: 3px solid #10B981;
    }
    
    .badge-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .streak-card {
        background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    .milestone-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #E5E7EB;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .milestone-item.completed {
        border-left-color: #10B981;
        background: linear-gradient(to right, #F0FDF4 0%, white 100%);
    }
    
    .xp-bar {
        background: #E5E7EB;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .xp-fill {
        background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .reward-card {
        background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    .leaderboard-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .leaderboard-item.current-user {
        background: linear-gradient(to right, #DBEAFE 0%, white 100%);
        border: 2px solid #3B82F6;
    }
    
    .rank-1 { border-left: 4px solid #FFD700; }
    .rank-2 { border-left: 4px solid #C0C0C0; }
    .rank-3 { border-left: 4px solid #CD7F32; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🏆 ACHIEVEMENTS DATA
# ═══════════════════════════════════════════════════════

BADGES = {
    "first_steps": {
        "icon": "👶",
        "name": "First Steps",
        "description": "Complete your first lesson",
        "xp": 50,
        "category": "Learning"
    },
    "quiz_beginner": {
        "icon": "🎯",
        "name": "Quiz Beginner",
        "description": "Complete your first quiz",
        "xp": 50,
        "category": "Quiz"
    },
    "quiz_master": {
        "icon": "🏅",
        "name": "Quiz Master",
        "description": "Score 100% on any quiz",
        "xp": 200,
        "category": "Quiz"
    },
    "scenario_survivor": {
        "icon": "🎬",
        "name": "Scenario Survivor",
        "description": "Complete your first scenario",
        "xp": 100,
        "category": "Scenarios"
    },
    "scenario_expert": {
        "icon": "🎖️",
        "name": "Scenario Expert",
        "description": "Complete all scenarios with 80%+ score",
        "xp": 500,
        "category": "Scenarios"
    },
    "flashcard_fan": {
        "icon": "🎴",
        "name": "Flashcard Fan",
        "description": "Review 50 flashcards",
        "xp": 100,
        "category": "Flashcards"
    },
    "memory_master": {
        "icon": "🧠",
        "name": "Memory Master",
        "description": "Master all flashcards in a category",
        "xp": 200,
        "category": "Flashcards"
    },
    "calculator_pro": {
        "icon": "🧮",
        "name": "Calculator Pro",
        "description": "Use all calculators at least once",
        "xp": 100,
        "category": "Tools"
    },
    "formula_wizard": {
        "icon": "📐",
        "name": "Formula Wizard",
        "description": "View all formulas",
        "xp": 75,
        "category": "Learning"
    },
    "streak_starter": {
        "icon": "🔥",
        "name": "Streak Starter",
        "description": "Study for 3 days in a row",
        "xp": 100,
        "category": "Dedication"
    },
    "streak_warrior": {
        "icon": "⚡",
        "name": "Streak Warrior",
        "description": "Study for 7 days in a row",
        "xp": 250,
        "category": "Dedication"
    },
    "streak_legend": {
        "icon": "👑",
        "name": "Streak Legend",
        "description": "Study for 30 days in a row",
        "xp": 1000,
        "category": "Dedication"
    },
    "early_bird": {
        "icon": "🌅",
        "name": "Early Bird",
        "description": "Study before 7 AM",
        "xp": 50,
        "category": "Special"
    },
    "night_owl": {
        "icon": "🦉",
        "name": "Night Owl",
        "description": "Study after 11 PM",
        "xp": 50,
        "category": "Special"
    },
    "pressure_master": {
        "icon": "📊",
        "name": "Pressure Master",
        "description": "Complete all pressure calculation lessons",
        "xp": 200,
        "category": "Learning"
    },
    "kick_expert": {
        "icon": "⚠️",
        "name": "Kick Expert",
        "description": "Master kick detection module",
        "xp": 200,
        "category": "Learning"
    },
    "kill_method_guru": {
        "icon": "🎯",
        "name": "Kill Method Guru",
        "description": "Master all kill methods",
        "xp": 300,
        "category": "Learning"
    },
    "bop_specialist": {
        "icon": "🛡️",
        "name": "BOP Specialist",
        "description": "Complete BOP equipment module",
        "xp": 200,
        "category": "Learning"
    },
    "subsea_diver": {
        "icon": "🌊",
        "name": "Subsea Diver",
        "description": "Complete subsea operations module",
        "xp": 250,
        "category": "Learning"
    },
    "mock_exam_passed": {
        "icon": "📝",
        "name": "Mock Exam Champion",
        "description": "Pass a mock exam with 70%+",
        "xp": 300,
        "category": "Exams"
    },
    "perfect_exam": {
        "icon": "💯",
        "name": "Perfect Score",
        "description": "Score 100% on a mock exam",
        "xp": 500,
        "category": "Exams"
    },
    "ai_student": {
        "icon": "🤖",
        "name": "AI Student",
        "description": "Ask 10 questions to AI Tutor",
        "xp": 100,
        "category": "Tools"
    },
    "completionist": {
        "icon": "🏆",
        "name": "Completionist",
        "description": "Complete all modules",
        "xp": 1000,
        "category": "Ultimate"
    },
    "iwcf_ready": {
        "icon": "🎓",
        "name": "IWCF Ready",
        "description": "Achieve 80%+ predicted score",
        "xp": 500,
        "category": "Ultimate"
    }
}

LEVELS = [
    {"level": 1, "name": "Newcomer", "min_xp": 0, "icon": "🌱"},
    {"level": 2, "name": "Learner", "min_xp": 100, "icon": "📚"},
    {"level": 3, "name": "Student", "min_xp": 300, "icon": "🎒"},
    {"level": 4, "name": "Practitioner", "min_xp": 600, "icon": "⚙️"},
    {"level": 5, "name": "Skilled", "min_xp": 1000, "icon": "🔧"},
    {"level": 6, "name": "Advanced", "min_xp": 1500, "icon": "📈"},
    {"level": 7, "name": "Expert", "min_xp": 2200, "icon": "🎯"},
    {"level": 8, "name": "Master", "min_xp": 3000, "icon": "🏅"},
    {"level": 9, "name": "Elite", "min_xp": 4000, "icon": "⭐"},
    {"level": 10, "name": "Legend", "min_xp": 5500, "icon": "👑"},
    {"level": 11, "name": "IWCF Champion", "min_xp": 7500, "icon": "🏆"}
]

MILESTONES = [
    {"id": 1, "name": "Complete 1 Module", "target": 1, "type": "modules", "xp": 100},
    {"id": 2, "name": "Complete 5 Modules", "target": 5, "type": "modules", "xp": 300},
    {"id": 3, "name": "Complete All Modules", "target": 8, "type": "modules", "xp": 500},
    {"id": 4, "name": "Answer 50 Questions", "target": 50, "type": "questions", "xp": 150},
    {"id": 5, "name": "Answer 200 Questions", "target": 200, "type": "questions", "xp": 400},
    {"id": 6, "name": "Answer 500 Questions", "target": 500, "type": "questions", "xp": 750},
    {"id": 7, "name": "Pass 1 Mock Exam", "target": 1, "type": "exams", "xp": 200},
    {"id": 8, "name": "Pass 5 Mock Exams", "target": 5, "type": "exams", "xp": 500},
    {"id": 9, "name": "Complete 1 Scenario", "target": 1, "type": "scenarios", "xp": 100},
    {"id": 10, "name": "Complete All Scenarios", "target": 5, "type": "scenarios", "xp": 400},
    {"id": 11, "name": "7-Day Streak", "target": 7, "type": "streak", "xp": 250},
    {"id": 12, "name": "30-Day Streak", "target": 30, "type": "streak", "xp": 1000},
]

# Fake leaderboard data
LEADERBOARD = [
    {"rank": 1, "name": "Ahmed M.", "xp": 8500, "level": 11, "country": "🇪🇬"},
    {"rank": 2, "name": "Mohammed K.", "xp": 7200, "level": 10, "country": "🇸🇦"},
    {"rank": 3, "name": "Omar S.", "xp": 6800, "level": 10, "country": "🇦🇪"},
    {"rank": 4, "name": "Khalid A.", "xp": 5500, "level": 9, "country": "🇰🇼"},
    {"rank": 5, "name": "Hassan R.", "xp": 4800, "level": 9, "country": "🇶🇦"},
    {"rank": 6, "name": "Ali T.", "xp": 4200, "level": 8, "country": "🇧🇭"},
    {"rank": 7, "name": "Youssef H.", "xp": 3600, "level": 8, "country": "🇪🇬"},
    {"rank": 8, "name": "Mahmoud F.", "xp": 3100, "level": 7, "country": "🇯🇴"},
    {"rank": 9, "name": "Ibrahim N.", "xp": 2700, "level": 7, "country": "🇴🇲"},
    {"rank": 10, "name": "Tariq W.", "xp": 2300, "level": 6, "country": "🇸🇦"},
]

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'total_xp' not in st.session_state:
    st.session_state.total_xp = 450  # Starting XP for demo

if 'unlocked_badges' not in st.session_state:
    st.session_state.unlocked_badges = ['first_steps', 'quiz_beginner', 'flashcard_fan']

if 'current_streak' not in st.session_state:
    st.session_state.current_streak = 5

if 'longest_streak' not in st.session_state:
    st.session_state.longest_streak = 12

if 'modules_completed' not in st.session_state:
    st.session_state.modules_completed = 3

if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 127

if 'exams_passed' not in st.session_state:
    st.session_state.exams_passed = 1

if 'scenarios_completed' not in st.session_state:
    st.session_state.scenarios_completed = 2

if 'user_name' not in st.session_state:
    st.session_state.user_name = "You"

# ═══════════════════════════════════════════════════════
# 🔧 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def get_current_level(xp):
    """Get current level based on XP"""
    current_level = LEVELS[0]
    for level in LEVELS:
        if xp >= level['min_xp']:
            current_level = level
        else:
            break
    return current_level

def get_next_level(xp):
    """Get next level info"""
    for i, level in enumerate(LEVELS):
        if xp < level['min_xp']:
            return level
    return None

def get_xp_progress(xp):
    """Get progress to next level"""
    current = get_current_level(xp)
    next_lvl = get_next_level(xp)
    
    if next_lvl is None:
        return 100, 0, 0  # Max level
    
    xp_in_level = xp - current['min_xp']
    xp_needed = next_lvl['min_xp'] - current['min_xp']
    progress = (xp_in_level / xp_needed) * 100
    
    return progress, xp_in_level, xp_needed

def check_milestone_progress(milestone):
    """Check progress on a milestone"""
    milestone_type = milestone['type']
    target = milestone['target']
    
    if milestone_type == 'modules':
        current = st.session_state.modules_completed
    elif milestone_type == 'questions':
        current = st.session_state.questions_answered
    elif milestone_type == 'exams':
        current = st.session_state.exams_passed
    elif milestone_type == 'scenarios':
        current = st.session_state.scenarios_completed
    elif milestone_type == 'streak':
        current = st.session_state.longest_streak
    else:
        current = 0
    
    return min(current, target), target, current >= target

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="achievement-header">
    <h1>🏆 Achievements & Rewards</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Track your progress, unlock badges, and climb the leaderboard!
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Every step forward earns you XP and brings you closer to mastery
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 MAIN STATS
# ═══════════════════════════════════════════════════════

current_level = get_current_level(st.session_state.total_xp)
next_level = get_next_level(st.session_state.total_xp)
progress, xp_in_level, xp_needed = get_xp_progress(st.session_state.total_xp)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div class="level-card">
        <div style="font-size: 4rem;">{current_level['icon']}</div>
        <h2 style="margin: 0.5rem 0;">Level {current_level['level']}: {current_level['name']}</h2>
        <p style="font-size: 1.5rem; margin: 0.5rem 0;">⭐ {st.session_state.total_xp} XP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # XP Progress bar
    if next_level:
        st.markdown(f"""
        <div style="margin-top: 1rem;">
            <p style="text-align: center; color: #6B7280; margin-bottom: 0.5rem;">
                {xp_in_level} / {xp_needed} XP to Level {next_level['level']} ({next_level['name']})
            </p>
            <div class="xp-bar">
                <div class="xp-fill" style="width: {progress}%;">{progress:.0f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="margin-top: 1rem; text-align: center;">
            <p style="color: #F59E0B; font-size: 1.2rem;">🎉 Maximum Level Reached!</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="streak-card">
        <div style="font-size: 3rem;">🔥</div>
        <h3 style="margin: 0.5rem 0;">{st.session_state.current_streak} Day Streak</h3>
        <p style="opacity: 0.9;">Best: {st.session_state.longest_streak} days</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    unlocked_count = len(st.session_state.unlocked_badges)
    total_badges = len(BADGES)
    
    st.markdown(f"""
    <div class="reward-card">
        <div style="font-size: 2.5rem;">🎖️</div>
        <h3 style="margin: 0.5rem 0;">{unlocked_count}/{total_badges} Badges</h3>
        <p style="opacity: 0.9;">{(unlocked_count/total_badges*100):.0f}% Unlocked</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎖️ BADGES SECTION
# ═══════════════════════════════════════════════════════

st.markdown("## 🎖️ Badges Collection")

# Filter tabs
badge_filter = st.selectbox(
    "Filter badges:",
    ["All", "Unlocked", "Locked", "Learning", "Quiz", "Scenarios", "Flashcards", "Tools", "Dedication", "Exams", "Special", "Ultimate"]
)

# Display badges in grid
cols = st.columns(4)

badge_items = list(BADGES.items())
col_idx = 0

for badge_id, badge_data in badge_items:
    is_unlocked = badge_id in st.session_state.unlocked_badges
    
    # Apply filter
    if badge_filter == "Unlocked" and not is_unlocked:
        continue
    if badge_filter == "Locked" and is_unlocked:
        continue
    if badge_filter not in ["All", "Unlocked", "Locked"] and badge_data['category'] != badge_filter:
        continue
    
    with cols[col_idx % 4]:
        status_class = "unlocked" if is_unlocked else "locked"
        
        st.markdown(f"""
        <div class="badge-card {status_class}">
            <div class="badge-icon">{badge_data['icon']}</div>
            <h4 style="margin: 0; color: #1F2937;">{badge_data['name']}</h4>
            <p style="color: #6B7280; font-size: 0.85rem; margin: 0.5rem 0;">
                {badge_data['description']}
            </p>
            <p style="color: #F59E0B; font-weight: 600; margin: 0;">
                +{badge_data['xp']} XP
            </p>
            <span style="background: {'#D1FAE5' if is_unlocked else '#F3F4F6'}; 
                        color: {'#065F46' if is_unlocked else '#6B7280'};
                        padding: 0.2rem 0.6rem; border-radius: 10px; font-size: 0.75rem;">
                {'✅ Unlocked' if is_unlocked else '🔒 Locked'}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    col_idx += 1

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎯 MILESTONES
# ═══════════════════════════════════════════════════════

st.markdown("## 🎯 Milestones")

for milestone in MILESTONES:
    current, target, completed = check_milestone_progress(milestone)
    progress_pct = (current / target) * 100
    
    status_class = "completed" if completed else ""
    
    st.markdown(f"""
    <div class="milestone-item {status_class}">
        <div style="font-size: 1.5rem;">{'✅' if completed else '⭕'}</div>
        <div style="flex: 1;">
            <strong>{milestone['name']}</strong>
            <div style="background: #E5E7EB; height: 8px; border-radius: 4px; margin-top: 0.5rem;">
                <div style="background: {'#10B981' if completed else '#3B82F6'}; 
                            height: 100%; width: {progress_pct}%; border-radius: 4px;"></div>
            </div>
            <span style="color: #6B7280; font-size: 0.85rem;">{current}/{target}</span>
        </div>
        <div style="text-align: right;">
            <span style="color: #F59E0B; font-weight: 600;">+{milestone['xp']} XP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📊 QUICK STATS
# ═══════════════════════════════════════════════════════

st.markdown("## 📊 Your Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">📚</div>
        <h3 style="color: #1E40AF; margin: 0.5rem 0;">{st.session_state.modules_completed}/8</h3>
        <p style="color: #6B7280;">Modules Completed</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">❓</div>
        <h3 style="color: #10B981; margin: 0.5rem 0;">{st.session_state.questions_answered}</h3>
        <p style="color: #6B7280;">Questions Answered</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">📝</div>
        <h3 style="color: #F59E0B; margin: 0.5rem 0;">{st.session_state.exams_passed}</h3>
        <p style="color: #6B7280;">Exams Passed</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">🎬</div>
        <h3 style="color: #7C3AED; margin: 0.5rem 0;">{st.session_state.scenarios_completed}/5</h3>
        <p style="color: #6B7280;">Scenarios Done</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🏅 LEADERBOARD
# ═══════════════════════════════════════════════════════

st.markdown("## 🏅 Leaderboard")
st.markdown("*See how you compare with other IWCF learners*")

# Add current user to leaderboard
user_rank = 15  # Demo rank
user_entry = {
    "rank": user_rank,
    "name": st.session_state.user_name,
    "xp": st.session_state.total_xp,
    "level": current_level['level'],
    "country": "🇪🇬"
}

for entry in LEADERBOARD:
    rank_class = ""
    if entry['rank'] == 1:
        rank_class = "rank-1"
        rank_icon = "🥇"
    elif entry['rank'] == 2:
        rank_class = "rank-2"
        rank_icon = "🥈"
    elif entry['rank'] == 3:
        rank_class = "rank-3"
        rank_icon = "🥉"
    else:
        rank_icon = f"#{entry['rank']}"
    
    st.markdown(f"""
    <div class="leaderboard-item {rank_class}">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 1.2rem; font-weight: bold; width: 40px;">{rank_icon}</span>
            <span style="font-size: 1.2rem;">{entry['country']}</span>
            <span style="font-weight: 600;">{entry['name']}</span>
        </div>
        <div style="text-align: right;">
            <span style="color: #F59E0B; font-weight: 600;">⭐ {entry['xp']} XP</span>
            <span style="color: #6B7280; margin-left: 1rem;">Lvl {entry['level']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Show user's position
st.markdown(f"""
<div style="text-align: center; margin: 1rem 0; color: #6B7280;">• • •</div>
<div class="leaderboard-item current-user">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 1.2rem; font-weight: bold; width: 40px;">#{user_rank}</span>
        <span style="font-size: 1.2rem;">{user_entry['country']}</span>
        <span style="font-weight: 600;">{user_entry['name']} (You)</span>
    </div>
    <div style="text-align: right;">
        <span style="color: #F59E0B; font-weight: 600;">⭐ {user_entry['xp']} XP</span>
        <span style="color: #6B7280; margin-left: 1rem;">Lvl {user_entry['level']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎁 DAILY REWARDS
# ═══════════════════════════════════════════════════════

st.markdown("## 🎁 Daily Rewards")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10B981 0%, #34D399 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 2.5rem;">📅</div>
        <h3>Daily Check-in</h3>
        <p>Visit every day to maintain your streak!</p>
        <p style="font-size: 1.2rem; font-weight: bold;">+25 XP</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✅ Claim Daily Reward", use_container_width=True, type="primary"):
        st.session_state.total_xp += 25
        st.session_state.current_streak += 1
        st.balloons()
        st.success("🎉 +25 XP! Streak extended!")
        st.rerun()

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 2.5rem;">🎯</div>
        <h3>Daily Challenge</h3>
        <p>Complete 10 questions today!</p>
        <p style="font-size: 1.2rem; font-weight: bold;">+50 XP</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Daily Challenge", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        🏆 <strong>Elshamy IWCF Mastery Method™ - Achievements</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Every expert was once a beginner" - Keep earning XP! ⭐
    </p>
</div>
""", unsafe_allow_html=True)