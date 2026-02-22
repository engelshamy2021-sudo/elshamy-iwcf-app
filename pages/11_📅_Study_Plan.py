import streamlit as st
from datetime import datetime, timedelta
import json

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Study Plan - IWCF Mastery",
    page_icon="📅",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .plan-header {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(5, 150, 105, 0.3);
    }
    
    .countdown-card {
        background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid #10B981;
    }
    
    .week-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #3B82F6;
    }
    
    .day-item {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #E5E7EB;
    }
    
    .day-item.completed {
        border-left-color: #10B981;
        background: #F0FDF4;
    }
    
    .day-item.today {
        border-left-color: #F59E0B;
        background: #FFFBEB;
        border: 2px solid #F59E0B;
    }
    
    .goal-card {
        background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#10B981 var(--progress), #E5E7EB 0);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    
    .progress-ring-inner {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📅 STUDY PLAN DATA
# ═══════════════════════════════════════════════════════

MODULES_SCHEDULE = [
    {
        "week": 1,
        "title": "Foundation Week",
        "modules": ["Introduction to Well Control", "Pressure Fundamentals"],
        "daily_hours": 2,
        "focus": "Understanding basics and pressure concepts"
    },
    {
        "week": 2,
        "title": "Detection Week",
        "modules": ["Kick Detection & Warning Signs", "Shut-in Procedures"],
        "daily_hours": 2.5,
        "focus": "Recognizing kicks and proper shut-in"
    },
    {
        "week": 3,
        "title": "Kill Methods Week",
        "modules": ["Kill Methods (Driller's & W&W)"],
        "daily_hours": 3,
        "focus": "Mastering kill calculations and procedures"
    },
    {
        "week": 4,
        "title": "Equipment Week",
        "modules": ["BOP Equipment & Testing"],
        "daily_hours": 2.5,
        "focus": "BOP components and operations"
    },
    {
        "week": 5,
        "title": "Advanced Week",
        "modules": ["Subsea Well Control", "Advanced Topics"],
        "daily_hours": 3,
        "focus": "Subsea operations and complications"
    },
    {
        "week": 6,
        "title": "Review & Practice",
        "modules": ["All Modules Review", "Mock Exams"],
        "daily_hours": 4,
        "focus": "Intensive review and exam practice"
    }
]

DAILY_TASKS = {
    "Saturday": ["Study new material (1.5 hrs)", "Practice questions (30 mins)", "Review flashcards (15 mins)"],
    "Sunday": ["Study new material (1.5 hrs)", "Scenario practice (30 mins)", "Calculator practice (15 mins)"],
    "Monday": ["Study new material (1 hr)", "Quiz practice (45 mins)", "AI Tutor Q&A (15 mins)"],
    "Tuesday": ["Review previous material (1 hr)", "Practice questions (45 mins)", "Formula review (15 mins)"],
    "Wednesday": ["Study new material (1.5 hrs)", "Scenario practice (30 mins)", "Weak areas focus (15 mins)"],
    "Thursday": ["Weekly review (1 hr)", "Mock exam practice (1 hr)", "Flashcard review (15 mins)"],
    "Friday": ["Light review (30 mins)", "Rest day - optional practice", "Prepare for next week"]
}

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'exam_date' not in st.session_state:
    st.session_state.exam_date = datetime.now() + timedelta(days=42)

if 'study_start_date' not in st.session_state:
    st.session_state.study_start_date = datetime.now()

if 'daily_goal_hours' not in st.session_state:
    st.session_state.daily_goal_hours = 2

if 'completed_days' not in st.session_state:
    st.session_state.completed_days = []

if 'study_log' not in st.session_state:
    st.session_state.study_log = []

if 'current_week' not in st.session_state:
    st.session_state.current_week = 1

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="plan-header">
    <h1>📅 Smart Study Plan</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Your personalized 6-week journey to IWCF success
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Stay organized, track progress, and achieve your goals
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ⏰ EXAM COUNTDOWN
# ═══════════════════════════════════════════════════════

col1, col2 = st.columns([2, 1])

with col1:
    # Calculate days remaining
    days_remaining = (st.session_state.exam_date - datetime.now()).days
    
    if days_remaining > 0:
        urgency_color = "#10B981" if days_remaining > 30 else "#F59E0B" if days_remaining > 14 else "#EF4444"
        
        st.markdown(f"""
        <div class="countdown-card" style="background: linear-gradient(135deg, {urgency_color} 0%, {urgency_color}90 100%);">
            <h2 style="margin: 0;">⏰ Exam Countdown</h2>
            <div style="font-size: 4rem; font-weight: bold; margin: 1rem 0;">{days_remaining}</div>
            <p style="font-size: 1.2rem; margin: 0;">Days Remaining</p>
            <p style="opacity: 0.9; margin-top: 0.5rem;">
                📅 {st.session_state.exam_date.strftime('%B %d, %Y')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="countdown-card">
            <h2>🎯 Exam Day!</h2>
            <p style="font-size: 1.5rem;">Good luck! You've got this! 💪</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### ⚙️ Settings")
    
    new_exam_date = st.date_input(
        "📅 Exam Date:",
        value=st.session_state.exam_date,
        min_value=datetime.now()
    )
    
    if new_exam_date != st.session_state.exam_date.date():
        st.session_state.exam_date = datetime.combine(new_exam_date, datetime.min.time())
        st.rerun()
    
    st.session_state.daily_goal_hours = st.slider(
        "🎯 Daily Study Goal (hours):",
        min_value=1,
        max_value=6,
        value=st.session_state.daily_goal_hours
    )

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📊 PROGRESS OVERVIEW
# ═══════════════════════════════════════════════════════

st.markdown("## 📊 Your Progress")

col1, col2, col3, col4 = st.columns(4)

# Calculate progress
total_study_days = 42  # 6 weeks
completed_days_count = len(st.session_state.completed_days)
progress_pct = (completed_days_count / total_study_days) * 100

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">📆</div>
        <h3 style="color: #10B981; margin: 0.5rem 0;">Week {st.session_state.current_week}/6</h3>
        <p style="color: #6B7280;">Current Week</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">✅</div>
        <h3 style="color: #3B82F6; margin: 0.5rem 0;">{completed_days_count}/{total_study_days}</h3>
        <p style="color: #6B7280;">Days Completed</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_hours = len(st.session_state.study_log) * st.session_state.daily_goal_hours
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">⏱️</div>
        <h3 style="color: #F59E0B; margin: 0.5rem 0;">{total_hours} hrs</h3>
        <p style="color: #6B7280;">Total Study Time</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">📈</div>
        <h3 style="color: #7C3AED; margin: 0.5rem 0;">{progress_pct:.0f}%</h3>
        <p style="color: #6B7280;">Plan Completion</p>
    </div>
    """, unsafe_allow_html=True)

# Progress bar
st.markdown(f"""
<div style="background: #E5E7EB; height: 15px; border-radius: 10px; margin: 1rem 0;">
    <div style="background: linear-gradient(90deg, #10B981 0%, #34D399 100%); 
                height: 100%; width: {progress_pct}%; border-radius: 10px;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📅 WEEKLY SCHEDULE
# ═══════════════════════════════════════════════════════

st.markdown("## 📅 6-Week Study Schedule")

# Week selector
selected_week = st.selectbox(
    "Select Week:",
    options=range(1, 7),
    format_func=lambda x: f"Week {x}: {MODULES_SCHEDULE[x-1]['title']}",
    index=st.session_state.current_week - 1
)

week_data = MODULES_SCHEDULE[selected_week - 1]

st.markdown(f"""
<div class="week-card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="margin: 0; color: #1E40AF;">Week {week_data['week']}: {week_data['title']}</h3>
            <p style="color: #6B7280; margin: 0.5rem 0;">
                📚 <strong>Modules:</strong> {', '.join(week_data['modules'])}
            </p>
            <p style="color: #6B7280; margin: 0;">
                🎯 <strong>Focus:</strong> {week_data['focus']}
            </p>
        </div>
        <div style="text-align: center; padding: 1rem; background: #EFF6FF; border-radius: 10px;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #1E40AF;">{week_data['daily_hours']}</div>
            <div style="color: #6B7280; font-size: 0.85rem;">hrs/day</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Daily breakdown
st.markdown("### 📋 Daily Tasks")

today = datetime.now().strftime("%A")

cols = st.columns(2)
days = list(DAILY_TASKS.keys())

for idx, day in enumerate(days):
    with cols[idx % 2]:
        is_today = day == today
        day_key = f"week{selected_week}_{day}"
        is_completed = day_key in st.session_state.completed_days
        
        status_class = "today" if is_today else "completed" if is_completed else ""
        
        st.markdown(f"""
        <div class="day-item {status_class}">
            <strong>{'📍 ' if is_today else ''}{day}</strong>
            {'<span style="color: #10B981; float: right;">✓ Done</span>' if is_completed else ''}
        </div>
        """, unsafe_allow_html=True)
        
        for task in DAILY_TASKS[day]:
            st.write(f"  • {task}")
        
        if not is_completed:
            if st.button(f"✅ Mark {day} Complete", key=f"complete_{day}_{selected_week}", use_container_width=True):
                st.session_state.completed_days.append(day_key)
                st.session_state.study_log.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "day": day,
                    "week": selected_week
                })
                st.success(f"✅ {day} marked as complete!")
                st.rerun()

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎯 TODAY'S GOALS
# ═══════════════════════════════════════════════════════

st.markdown("## 🎯 Today's Goals")

today_name = datetime.now().strftime("%A")
today_tasks = DAILY_TASKS.get(today_name, [])

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div class="goal-card">
        <h3 style="margin: 0;">📍 {today_name}'s Study Plan</h3>
        <p style="opacity: 0.9; margin-top: 0.5rem;">Target: {st.session_state.daily_goal_hours} hours of study</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for idx, task in enumerate(today_tasks, 1):
        st.checkbox(task, key=f"today_task_{idx}")

with col2:
    st.markdown(f"""
    <div class="tip-box">
        <strong>💡 Tip of the Day:</strong>
        <p style="margin: 0.5rem 0 0 0;">
            Focus on understanding concepts, not memorizing. 
            Use the AI Tutor to clarify any doubts!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Today's Study", use_container_width=True, type="primary"):
        st.switch_page("pages/01_📚_Learn.py")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📈 STUDY LOG
# ═══════════════════════════════════════════════════════

st.markdown("## 📈 Recent Study Log")

if st.session_state.study_log:
    for entry in reversed(st.session_state.study_log[-7:]):  # Last 7 entries
        st.markdown(f"""
        <div style="background: white; padding: 0.8rem 1rem; border-radius: 8px; 
                    margin: 0.3rem 0; display: flex; justify-content: space-between;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <span>📅 {entry['date']} - {entry['day']}</span>
            <span style="color: #10B981;">✅ Week {entry['week']}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📝 No study sessions logged yet. Start studying to track your progress!")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🔗 QUICK ACTIONS
# ═══════════════════════════════════════════════════════

st.markdown("## 🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Start Learning", use_container_width=True):
        st.switch_page("pages/01_📚_Learn.py")

with col2:
    if st.button("❓ Practice Quiz", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")

with col3:
    if st.button("🎴 Flashcards", use_container_width=True):
        st.switch_page("pages/08_🎴_Flashcards.py")

with col4:
    if st.button("📝 Mock Exam", use_container_width=True):
        st.switch_page("pages/03_📝_Mock_Exam.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        📅 <strong>Elshamy IWCF Mastery Method™ - Study Plan</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "A goal without a plan is just a wish" 🎯
    </p>
</div>
""", unsafe_allow_html=True)