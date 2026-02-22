"""
📊 ELSHAMY IWCF - Progress Dashboard
Comprehensive progress tracking and analytics
With Data Manager Integration
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import calendar

# ═══════════════════════════════════════════════════════
# 🔧 PATH & DATA MANAGER SETUP
# ═══════════════════════════════════════════════════════

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.data_manager import (
        load_progress,
        get_overall_stats,
        get_quiz_stats
    )
    DATA_MANAGER_AVAILABLE = True
except ImportError as e:
    DATA_MANAGER_AVAILABLE = False
    print(f"⚠️ Data Manager not available: {e}")

# ═══════════════════════════════════════════════════════
# 📱 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Progress - Elshamy IWCF",
    page_icon="📊",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .progress-header {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        animation: fadeIn 0.6s ease;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        transition: transform 0.3s ease;
    }
    
    .achievement-badge:hover {
        transform: scale(1.05);
    }
    
    .locked-badge {
        background: #E5E7EB;
        color: #9CA3AF;
        box-shadow: none;
    }
    
    .streak-card {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
    }
    
    .level-card {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    
    .milestone-item {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #10B981;
    }
    
    .milestone-pending {
        border-left-color: #9CA3AF;
        opacity: 0.7;
    }
    
    .calendar-day {
        width: 40px;
        height: 40px;
        display: inline-block;
        margin: 2px;
        border-radius: 8px;
        text-align: center;
        line-height: 40px;
        font-size: 0.9rem;
    }
    
    .day-studied {
        background: #10B981;
        color: white;
        font-weight: bold;
    }
    
    .day-today {
        border: 3px solid #3B82F6;
        font-weight: bold;
    }
    
    .day-normal {
        background: #F3F4F6;
        color: #6B7280;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 💾 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def calculate_study_days(data):
    """Calculate total study days from dates"""
    study_dates = set()
    
    if 'by_date' in data.get('study_time', {}):
        study_dates.update(data['study_time']['by_date'].keys())
    
    return max(len(study_dates), 1)


def get_user_level_name(xp):
    """Convert XP to level name"""
    if xp < 1000:
        return "Beginner"
    elif xp < 3000:
        return "Intermediate"
    elif xp < 6000:
        return "Advanced"
    else:
        return "Expert"


def generate_study_dates(data):
    """Generate study dates for calendar from data"""
    dates = []
    
    streak = data['achievements'].get('study_streak', 0)
    today = datetime.now()
    
    for i in range(min(streak, 30)):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        dates.append(date)
    
    if 'by_date' in data.get('study_time', {}):
        dates.extend(list(data['study_time']['by_date'].keys())[-30:])
    
    return list(set(dates))


def generate_daily_activity(data):
    """Generate daily activity from study time data"""
    activity = []
    
    if 'by_date' in data.get('study_time', {}):
        for date, minutes in sorted(data['study_time']['by_date'].items())[-30:]:
            hours = minutes / 60
            questions = int(hours * 12)
            activity.append({
                'date': date,
                'hours': round(hours, 1),
                'questions': questions,
                'topics_completed': 0
            })
    
    # Fill with demo data if insufficient
    if len(activity) < 30:
        today = datetime.now()
        for i in range(30 - len(activity)):
            date = (today - timedelta(days=30-i)).strftime('%Y-%m-%d')
            if i % 3 != 0:
                activity.append({
                    'date': date,
                    'hours': round(1.5 + (i % 4) * 0.5, 1),
                    'questions': int((1.5 + (i % 4) * 0.5) * 12),
                    'topics_completed': i % 2
                })
    
    return sorted(activity, key=lambda x: x['date'])[-30:]


def convert_badges_to_achievements(badges_list):
    """Convert Data Manager badges to achievement format"""
    
    achievements_db = {
        'first_steps': {
            'name': 'First Steps',
            'desc': 'Complete first topic',
            'icon': '🎯',
            'xp': 100,
            'unlocked': 'first_steps' in badges_list
        },
        'knowledge_seeker': {
            'name': 'Knowledge Seeker',
            'desc': 'Complete 10 topics',
            'icon': '📚',
            'xp': 200,
            'unlocked': 'knowledge_seeker' in badges_list
        },
        'scholar': {
            'name': 'Scholar',
            'desc': 'Complete all topics',
            'icon': '🎓',
            'xp': 500,
            'unlocked': 'scholar' in badges_list
        },
        'quiz_master': {
            'name': 'Quiz Master',
            'desc': 'Solve 100 questions',
            'icon': '⚡',
            'xp': 200,
            'unlocked': 'quiz_master' in badges_list
        },
        'quiz_legend': {
            'name': 'Quiz Legend',
            'desc': 'Solve 500 questions',
            'icon': '🌟',
            'xp': 400,
            'unlocked': 'quiz_legend' in badges_list
        },
        'accuracy_expert': {
            'name': 'Accuracy Expert',
            'desc': '90%+ accuracy on 50+ questions',
            'icon': '🎯',
            'xp': 300,
            'unlocked': 'accuracy_expert' in badges_list
        },
        'exam_taker': {
            'name': 'Exam Taker',
            'desc': 'Take first exam',
            'icon': '📝',
            'xp': 100,
            'unlocked': 'exam_taker' in badges_list
        },
        'exam_ready': {
            'name': 'Exam Ready',
            'desc': 'Pass 3 mock exams',
            'icon': '✅',
            'xp': 300,
            'unlocked': 'exam_ready' in badges_list
        },
        'exam_master': {
            'name': 'Exam Master',
            'desc': 'Pass 5 exams with 80%+',
            'icon': '🏆',
            'xp': 500,
            'unlocked': 'exam_master' in badges_list
        },
        'perfect_score': {
            'name': 'Perfect Score',
            'desc': 'Score 100% on exam',
            'icon': '💎',
            'xp': 500,
            'unlocked': 'perfect_score' in badges_list
        },
        'consistent': {
            'name': 'Consistent',
            'desc': '7-day study streak',
            'icon': '🔥',
            'xp': 250,
            'unlocked': 'consistent' in badges_list
        },
        'dedicated': {
            'name': 'Dedicated',
            'desc': '30-day study streak',
            'icon': '💪',
            'xp': 1000,
            'unlocked': 'dedicated' in badges_list
        },
    }
    
    # Add some locked achievements not in data manager
    achievements_db.update({
        'speed_demon': {
            'name': 'Speed Demon',
            'desc': 'Solve 50 questions in one day',
            'icon': '⚡',
            'xp': 150,
            'unlocked': False
        },
        'night_owl': {
            'name': 'Night Owl',
            'desc': 'Study session after 10 PM',
            'icon': '🦉',
            'xp': 100,
            'unlocked': False
        },
        'early_bird': {
            'name': 'Early Bird',
            'desc': 'Study session before 6 AM',
            'icon': '🐦',
            'xp': 100,
            'unlocked': False
        },
        'master': {
            'name': 'IWCF Master',
            'desc': 'Complete entire course with 90%+',
            'icon': '👑',
            'xp': 2000,
            'unlocked': False
        },
    })
    
    return achievements_db

# ═══════════════════════════════════════════════════════
# 💾 DATA INITIALIZATION
# ═══════════════════════════════════════════════════════

def init_progress_data():
    """Initialize progress data from Data Manager or demo"""
    
    if DATA_MANAGER_AVAILABLE:
        try:
            # Load from Data Manager
            data = load_progress()
            stats = get_overall_stats()
            quiz_stats = get_quiz_stats()
            
            st.session_state.user_progress = {
                'total_modules': data['modules']['total'],
                'completed_modules': stats['modules_completed'],
                'total_topics': 36,
                'completed_topics': stats['topics_completed'],
                'total_questions': 750,
                'solved_questions': quiz_stats['total'],
                'correct_answers': quiz_stats['correct'],
                'mock_exams_taken': stats['mock_exams_taken'],
                'mock_exams_passed': stats['mock_exams_passed'],
                'study_days': calculate_study_days(data),
                'streak_days': data['achievements']['study_streak'],
                'total_study_hours': data['study_time']['total_minutes'] / 60,
                'level': get_user_level_name(data['achievements']['xp_total']),
                'xp_points': data['achievements']['xp_total'],
                'start_date': data['user_info']['created_date'],
                'target_exam_date': '2024-02-15'
            }
            
            st.session_state.study_streak_dates = generate_study_dates(data)
            st.session_state.daily_activity = generate_daily_activity(data)
            st.session_state.achievements = convert_badges_to_achievements(data['achievements']['badges'])
            
        except Exception as e:
            print(f"Error loading from Data Manager: {e}")
            init_demo_data()
    else:
        init_demo_data()


def init_demo_data():
    """Initialize with demo data"""
    
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'total_modules': 8,
            'completed_modules': 5,
            'total_topics': 36,
            'completed_topics': 18,
            'total_questions': 750,
            'solved_questions': 487,
            'correct_answers': 410,
            'mock_exams_taken': 3,
            'mock_exams_passed': 2,
            'study_days': 23,
            'streak_days': 7,
            'total_study_hours': 34.5,
            'level': 'Intermediate',
            'xp_points': 3450,
            'start_date': '2024-01-01',
            'target_exam_date': '2024-02-15'
        }
    
    if 'daily_activity' not in st.session_state:
        today = datetime.now()
        st.session_state.daily_activity = []
        for i in range(30, 0, -1):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if i % 3 != 0:
                hours = round(1.5 + (i % 4) * 0.5, 1)
                questions = int(hours * 12)
                st.session_state.daily_activity.append({
                    'date': date,
                    'hours': hours,
                    'questions': questions,
                    'topics_completed': i % 2
                })
    
    if 'achievements' not in st.session_state:
        st.session_state.achievements = {
            'first_steps': {'name': 'First Steps', 'desc': 'Complete first module', 'unlocked': True, 'icon': '🎯', 'xp': 100},
            'quiz_master': {'name': 'Quiz Master', 'desc': 'Solve 100 questions', 'unlocked': True, 'icon': '📝', 'xp': 200},
            'exam_ready': {'name': 'Exam Ready', 'desc': 'Pass 3 mock exams', 'unlocked': True, 'icon': '✅', 'xp': 300},
            'consistent': {'name': 'Consistent', 'desc': '7-day streak', 'unlocked': True, 'icon': '🔥', 'xp': 250},
            'half_way': {'name': 'Half Way There', 'desc': 'Complete 50% of course', 'unlocked': True, 'icon': '🎊', 'xp': 400},
            'speed_demon': {'name': 'Speed Demon', 'desc': 'Solve 50 in one day', 'unlocked': False, 'icon': '⚡', 'xp': 150},
            'perfect_score': {'name': 'Perfect Score', 'desc': '100% on exam', 'unlocked': False, 'icon': '🏆', 'xp': 500},
            'night_owl': {'name': 'Night Owl', 'desc': 'Study after 10 PM', 'unlocked': False, 'icon': '🦉', 'xp': 100},
            'early_bird': {'name': 'Early Bird', 'desc': 'Study before 6 AM', 'unlocked': False, 'icon': '🐦', 'xp': 100},
            'dedicated': {'name': 'Dedicated', 'desc': '30-day streak', 'unlocked': False, 'icon': '💪', 'xp': 1000},
            'master': {'name': 'IWCF Master', 'desc': 'Complete all 90%+', 'unlocked': False, 'icon': '👑', 'xp': 2000},
        }
    
    if 'study_streak_dates' not in st.session_state:
        today = datetime.now()
        st.session_state.study_streak_dates = [
            (today - timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(7)
        ]

# Initialize
init_progress_data()
progress = st.session_state.user_progress

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="progress-header">
    <h1>📊 Your Learning Progress Dashboard</h1>
    <p>Track your journey to IWCF certification success</p>
</div>
""", unsafe_allow_html=True)

# Data source indicator
if DATA_MANAGER_AVAILABLE:
    st.success("✅ **Live Data:** Progress synced with database")
else:
    st.warning("⚠️ **Demo Mode:** Progress data is for demonstration only")

# ═══════════════════════════════════════════════════════
# 📊 TOP STATS ROW
# ═══════════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
overall_progress = (
    (progress['completed_modules'] / progress['total_modules'] * 0.3) + 
    (progress['completed_topics'] / progress['total_topics'] * 0.3) + 
    (progress['solved_questions'] / progress['total_questions'] * 0.4)
) * 100

accuracy = (progress['correct_answers'] / progress['solved_questions'] * 100) if progress['solved_questions'] > 0 else 0

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div style="color: #6B7280; font-size: 0.9rem;">Overall Progress</div>
        <div class="stat-number" style="color: #3B82F6;">{overall_progress:.0f}%</div>
        <div style="background: #E5E7EB; border-radius: 10px; height: 10px; margin-top: 1rem;">
            <div style="background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%); 
                 width: {overall_progress}%; height: 100%; border-radius: 10px; transition: width 1s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div style="color: #6B7280; font-size: 0.9rem;">Accuracy Rate</div>
        <div class="stat-number" style="color: #10B981;">{accuracy:.1f}%</div>
        <p style="margin-top: 0.5rem; color: #6B7280; font-size: 0.85rem;">
            {progress['correct_answers']}/{progress['solved_questions']} correct
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="streak-card">
        <div style="color: white; opacity: 0.9; font-size: 0.9rem;">Study Streak</div>
        <div class="stat-number">🔥 {progress['streak_days']}</div>
        <p style="margin-top: 0.5rem; opacity: 0.9; font-size: 0.85rem;">days in a row</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    xp = progress['xp_points']
    
    if xp < 1000:
        level = "Beginner"
        color = "#10B981"
    elif xp < 3000:
        level = "Intermediate"
        color = "#F59E0B"
    elif xp < 6000:
        level = "Advanced"
        color = "#8B5CF6"
    else:
        level = "Expert"
        color = "#EF4444"
    
    next_level_xp = ((xp // 1000) + 1) * 1000
    progress_to_next = ((xp % 1000) / 1000) * 100
    
    st.markdown(f"""
    <div class="level-card" style="background: linear-gradient(135deg, {color} 0%, {color}CC 100%);">
        <div style="color: white; opacity: 0.9; font-size: 0.9rem;">Current Level</div>
        <div class="stat-number">{level}</div>
        <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 8px; margin-top: 1rem;">
            <div style="background: white; width: {progress_to_next}%; height: 100%; border-radius: 10px;"></div>
        </div>
        <p style="margin-top: 0.5rem; opacity: 0.9; font-size: 0.8rem;">{xp} / {next_level_xp} XP</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📈 DETAILED PROGRESS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📈 Detailed Progress Breakdown")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📚 Modules")
    module_progress = (progress['completed_modules'] / progress['total_modules']) * 100
    
    st.markdown(f"""
    <div class="stat-card">
        <h2 style="color: #3B82F6; margin: 0;">{progress['completed_modules']}/{progress['total_modules']}</h2>
        <p style="color: #6B7280; margin-top: 0.5rem;">Modules Completed</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(module_progress / 100)
    st.caption(f"{module_progress:.0f}% Complete • {progress['total_modules'] - progress['completed_modules']} remaining")

with col2:
    st.markdown("### 📖 Topics")
    topic_progress = (progress['completed_topics'] / progress['total_topics']) * 100
    
    st.markdown(f"""
    <div class="stat-card">
        <h2 style="color: #10B981; margin: 0;">{progress['completed_topics']}/{progress['total_topics']}</h2>
        <p style="color: #6B7280; margin-top: 0.5rem;">Topics Mastered</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(topic_progress / 100)
    st.caption(f"{topic_progress:.0f}% Complete • {progress['total_topics'] - progress['completed_topics']} remaining")

with col3:
    st.markdown("### ❓ Questions")
    question_progress = (progress['solved_questions'] / progress['total_questions']) * 100
    
    st.markdown(f"""
    <div class="stat-card">
        <h2 style="color: #F59E0B; margin: 0;">{progress['solved_questions']}/{progress['total_questions']}</h2>
        <p style="color: #6B7280; margin-top: 0.5rem;">Questions Solved</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(question_progress / 100)
    st.caption(f"{question_progress:.0f}% Complete • {progress['total_questions'] - progress['solved_questions']} remaining")

# ═══════════════════════════════════════════════════════
# 📅 STUDY CALENDAR
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📅 Study Calendar")

today = datetime.now()
year = today.year
month = today.month

cal = calendar.monthcalendar(year, month)
month_name = calendar.month_name[month]

st.markdown(f"### {month_name} {year}")

study_dates_set = set(st.session_state.study_streak_dates)

calendar_html = '<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; max-width: 600px;">'

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
for day in days:
    calendar_html += f'<div style="text-align: center; font-weight: bold; color: #6B7280; padding: 10px;">{day}</div>'

for week in cal:
    for day in week:
        if day == 0:
            calendar_html += '<div></div>'
        else:
            date_str = f"{year}-{month:02d}-{day:02d}"
            is_studied = date_str in study_dates_set
            is_today = day == today.day
            
            day_class = "day-normal"
            if is_studied:
                day_class = "day-studied"
            if is_today:
                day_class += " day-today"
            
            calendar_html += f'<div class="calendar-day {day_class}">{day}</div>'

calendar_html += '</div>'

st.markdown(calendar_html, unsafe_allow_html=True)
st.caption("🟢 Studied | 🔵 Today | ⚪ Not studied")

# ═══════════════════════════════════════════════════════
# 📊 STUDY ACTIVITY CHARTS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📊 Study Activity Analytics")

tab1, tab2, tab3 = st.tabs(["📈 Daily Activity", "📊 Weekly Summary", "🎯 Performance"])

with tab1:
    df_activity = pd.DataFrame(st.session_state.daily_activity)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hours = go.Figure()
        fig_hours.add_trace(go.Bar(
            x=df_activity['date'],
            y=df_activity['hours'],
            marker_color='#3B82F6',
            name='Study Hours',
            text=df_activity['hours'],
            textposition='outside'
        ))
        
        fig_hours.update_layout(
            title="Daily Study Hours",
            xaxis_title="Date",
            yaxis_title="Hours",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_hours, use_container_width=True)
        
        total_hours = df_activity['hours'].sum()
        avg_hours = df_activity['hours'].mean()
        st.success(f"📊 **Total:** {total_hours:.1f} hours | **Average:** {avg_hours:.1f} hours/day")
    
    with col2:
        fig_questions = go.Figure()
        fig_questions.add_trace(go.Bar(
            x=df_activity['date'],
            y=df_activity['questions'],
            marker_color='#10B981',
            name='Questions',
            text=df_activity['questions'],
            textposition='outside'
        ))
        
        fig_questions.update_layout(
            title="Daily Questions Solved",
            xaxis_title="Date",
            yaxis_title="Questions",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_questions, use_container_width=True)
        
        total_q = df_activity['questions'].sum()
        avg_q = df_activity['questions'].mean()
        st.success(f"📊 **Total:** {total_q} questions | **Average:** {avg_q:.0f} questions/day")

with tab2:
    df_activity['week'] = pd.to_datetime(df_activity['date']).dt.isocalendar().week
    weekly_stats = df_activity.groupby('week').agg({
        'hours': 'sum',
        'questions': 'sum',
        'topics_completed': 'sum'
    }).reset_index()
    
    fig_weekly = go.Figure()
    
    fig_weekly.add_trace(go.Bar(
        x=weekly_stats['week'],
        y=weekly_stats['hours'],
        name='Hours',
        marker_color='#3B82F6',
        yaxis='y'
    ))
    
    fig_weekly.add_trace(go.Scatter(
        x=weekly_stats['week'],
        y=weekly_stats['questions'],
        name='Questions',
        marker_color='#10B981',
        yaxis='y2',
        mode='lines+markers'
    ))
    
    fig_weekly.update_layout(
        title="Weekly Progress",
        xaxis_title="Week Number",
        yaxis=dict(title="Study Hours", side='left'),
        yaxis2=dict(title="Questions Solved", side='right', overlaying='y'),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_weekly, use_container_width=True)

with tab3:
    # Get exam data
    if DATA_MANAGER_AVAILABLE:
        try:
            data = load_progress()
            if data['exams']['exam_history']:
                exam_data = {
                    'Exam': [f"Exam {i+1}" for i in range(len(data['exams']['exam_history']))],
                    'Score': [e['score'] for e in data['exams']['exam_history']],
                    'Date': [e['date'] for e in data['exams']['exam_history']]
                }
            else:
                exam_data = {'Exam': ['Mock 1', 'Mock 2', 'Mock 3'], 'Score': [72, 78, 85], 'Date': ['2024-01-10', '2024-01-15', '2024-01-20']}
        except:
            exam_data = {'Exam': ['Mock 1', 'Mock 2', 'Mock 3'], 'Score': [72, 78, 85], 'Date': ['2024-01-10', '2024-01-15', '2024-01-20']}
    else:
        exam_data = {'Exam': ['Mock 1', 'Mock 2', 'Mock 3'], 'Score': [72, 78, 85], 'Date': ['2024-01-10', '2024-01-15', '2024-01-20']}
    
    df_exams = pd.DataFrame(exam_data)
    
    fig_performance = go.Figure()
    
    fig_performance.add_trace(go.Scatter(
        x=df_exams['Exam'],
        y=df_exams['Score'],
        mode='lines+markers',
        name='Your Score',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=12, symbol='circle')
    ))
    
    fig_performance.add_hline(y=70, line_dash="dash", line_color="green",
                              annotation_text="Pass Mark (70%)", annotation_position="right")
    
    fig_performance.add_hline(y=90, line_dash="dot", line_color="gold",
                              annotation_text="Target (90%)", annotation_position="right")
    
    fig_performance.update_layout(
        title="Mock Exam Performance Trend",
        xaxis_title="Exam",
        yaxis_title="Score (%)",
        height=400,
        yaxis=dict(range=[0, 100]),
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_performance, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_score = sum(df_exams['Score']) / len(df_exams['Score'])
        delta = f"{df_exams['Score'].iloc[-1] - df_exams['Score'].iloc[0]:+.0f}%" if len(df_exams) > 1 else None
        st.metric("Average Score", f"{avg_score:.1f}%", delta=delta)
    
    with col2:
        best_score = max(df_exams['Score'])
        st.metric("Best Score", f"{best_score:.0f}%")
    
    with col3:
        latest_score = df_exams['Score'].iloc[-1]
        improvement = "Improving! 📈" if latest_score > avg_score else "Keep practicing 💪"
        st.metric("Latest Score", f"{latest_score:.0f}%", delta=improvement, delta_color="off")

# ═══════════════════════════════════════════════════════
# 🏆 ACHIEVEMENTS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🏆 Achievements & Badges")

achievements = st.session_state.achievements
unlocked_count = sum(1 for a in achievements.values() if a['unlocked'])
total_count = len(achievements)
total_xp_earned = sum(a['xp'] for a in achievements.values() if a['unlocked'])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unlocked", f"{unlocked_count}/{total_count}")

with col2:
    st.metric("XP Earned", f"{total_xp_earned}")

with col3:
    completion = (unlocked_count / total_count) * 100
    st.metric("Completion", f"{completion:.0f}%")

st.progress(unlocked_count / total_count)

st.markdown("### 🎖️ Your Badges")

cols = st.columns(4)
for idx, (key, achievement) in enumerate(achievements.items()):
    with cols[idx % 4]:
        badge_class = "achievement-badge" if achievement['unlocked'] else "achievement-badge locked-badge"
        lock_icon = "" if achievement['unlocked'] else "🔒 "
        
        st.markdown(f"""
        <div class="{badge_class}">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{achievement['icon']}</div>
            <div style="font-weight: bold; font-size: 1rem;">{lock_icon}{achievement['name']}</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9;">{achievement['desc']}</div>
            <div style="font-size: 0.75rem; margin-top: 0.5rem; opacity: 0.8;">+{achievement['xp']} XP</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎯 MILESTONES
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 🎯 Milestones & Goals")

milestones = [
    {'name': 'Complete all modules', 'progress': progress['completed_modules'], 'target': progress['total_modules'], 
     'done': progress['completed_modules'] >= progress['total_modules'], 'icon': '📚'},
    {'name': 'Solve 500 questions', 'progress': progress['solved_questions'], 'target': 500, 
     'done': progress['solved_questions'] >= 500, 'icon': '❓'},
    {'name': 'Pass 5 mock exams', 'progress': progress['mock_exams_passed'], 'target': 5, 
     'done': progress['mock_exams_passed'] >= 5, 'icon': '📝'},
    {'name': 'Achieve 85% accuracy', 'progress': accuracy, 'target': 85, 
     'done': accuracy >= 85, 'icon': '🎯'},
    {'name': '30-day study streak', 'progress': progress['streak_days'], 'target': 30, 
     'done': progress['streak_days'] >= 30, 'icon': '🔥'},
    {'name': 'Study 50 hours total', 'progress': progress['total_study_hours'], 'target': 50, 
     'done': progress['total_study_hours'] >= 50, 'icon': '⏰'}
]

col1, col2 = st.columns(2)

for idx, milestone in enumerate(milestones):
    with col1 if idx % 2 == 0 else col2:
        milestone_class = "milestone-item" if milestone['done'] else "milestone-item milestone-pending"
        status_icon = "✅" if milestone['done'] else "⏳"
        progress_pct = min((milestone['progress'] / milestone['target']) * 100, 100)
        
        st.markdown(f"""
        <div class="{milestone_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>{status_icon} {milestone['icon']} {milestone['name']}</strong>
                <span style="font-weight: bold; color: {'#10B981' if milestone['done'] else '#6B7280'};">
                    {milestone['progress']:.0f}/{milestone['target']:.0f}
                </span>
            </div>
            <div style="background: #E5E7EB; border-radius: 10px; height: 8px; margin-top: 0.8rem;">
                <div style="background: {'#10B981' if milestone['done'] else '#3B82F6'}; 
                     width: {progress_pct}%; height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ⏰ EXAM COUNTDOWN
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## ⏰ Exam Countdown")

target_date = datetime.strptime(progress['target_exam_date'], '%Y-%m-%d')
today_dt = datetime.now()
days_remaining = (target_date - today_dt).days

readiness_score = (overall_progress * 0.4) + (accuracy * 0.3) + (min(progress['mock_exams_passed'] / 5 * 100, 100) * 0.3)

col1, col2, col3, col4 = st.columns(4)

with col1:
    color = "#EF4444" if days_remaining < 7 else "#F59E0B" if days_remaining < 14 else "#10B981"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number" style="color: {color};">{days_remaining}</div>
        <div style="color: #6B7280; font-size: 0.9rem;">Days Remaining</div>
        <div style="margin-top: 0.5rem; color: #6B7280; font-size: 0.8rem;">
            Target: {target_date.strftime('%B %d, %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number" style="color: #10B981;">{progress['study_days']}</div>
        <div style="color: #6B7280; font-size: 0.9rem;">Days Studied</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number" style="color: #3B82F6;">{progress['total_study_hours']:.1f}</div>
        <div style="color: #6B7280; font-size: 0.9rem;">Total Hours</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    readiness_color = "#10B981" if readiness_score >= 80 else "#F59E0B" if readiness_score >= 60 else "#EF4444"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number" style="color: {readiness_color};">{readiness_score:.0f}%</div>
        <div style="color: #6B7280; font-size: 0.9rem;">Readiness Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 📋 Exam Readiness Assessment")

if readiness_score >= 85 and days_remaining >= 3:
    st.success("🎉 **EXCELLENT!** You're very well prepared for the exam!")
    st.info("**Recommendation:** Take 1-2 more mock exams, review formulas, and stay confident!")
elif readiness_score >= 70:
    st.info("📚 **GOOD PROGRESS!** You're on track but keep pushing.")
    st.warning("**Focus on:** Weak topics, more practice questions, and maintain study rhythm.")
else:
    st.warning("⚠️ **MORE PREPARATION NEEDED** - Don't worry, you have time!")
    if days_remaining < 7:
        st.error("🚨 **URGENT:** Exam is very soon! Intensive study required.")
    st.info("**Priority actions:** Complete remaining modules, solve more questions, take mock exams daily.")

# ═══════════════════════════════════════════════════════
# 💡 RECOMMENDATIONS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 💡 Personalized Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 What to Focus On")
    
    recommendations = []
    
    if progress['completed_topics'] < progress['total_topics'] * 0.5:
        recommendations.append(("📖", "Complete more learning modules", "High Priority"))
    
    if accuracy < 75:
        recommendations.append(("⚠️", "Improve accuracy - review wrong answers carefully", "High Priority"))
    
    if progress['mock_exams_taken'] < 5:
        recommendations.append(("📝", "Take more mock exams for exam readiness", "Medium Priority"))
    
    if progress['streak_days'] < 7:
        recommendations.append(("🔥", "Build a consistent 7-day study streak", "Medium Priority"))
    
    if progress['solved_questions'] < 300:
        recommendations.append(("❓", "Solve more practice questions", "High Priority"))
    
    if not recommendations:
        st.success("✅ **Great job!** You're on track with everything!")
    else:
        for icon, text, priority in recommendations:
            priority_color = "#EF4444" if "High" in priority else "#F59E0B"
            st.markdown(f"""
            <div style="background: #F3F4F6; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                 border-left: 4px solid {priority_color};">
                <strong>{icon} {text}</strong><br>
                <span style="color: {priority_color}; font-size: 0.85rem; font-weight: 600;">{priority}</span>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📅 Suggested Study Plan")
    
    if days_remaining > 21:
        st.success("✅ **Comfortable Timeline** - Steady pace recommended")
        plan = ["Study 2-3 hours daily", "Complete 2-3 topics per day", "One mock exam per week", 
                "Review on weekends", "Maintain balance"]
    elif days_remaining > 14:
        st.info("📚 **Standard Preparation** - Consistent effort needed")
        plan = ["Study 3-4 hours daily", "Complete 3-4 topics per day", "Mock exam every 3-4 days", 
                "Daily practice (50+ questions)", "Focus on weak areas"]
    elif days_remaining > 7:
        st.warning("⚠️ **Intensive Study Required** - Step up the pace")
        plan = ["Study 4-6 hours daily", "Complete 4-5 topics per day", "Mock exam every 2 days", 
                "Daily quiz (100+ questions)", "Formula revision daily"]
    else:
        st.error("🚨 **FINAL SPRINT MODE** - Maximum focus!")
        plan = ["Study 6-8 hours daily", "Complete all remaining topics ASAP", "Daily mock exams", 
                "Review formulas 2× daily", "Focus ONLY on exam prep"]
    
    for item in plan:
        st.markdown(f"- {item}")

# ═══════════════════════════════════════════════════════
# 💾 EXPORT PROGRESS
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 💾 Export Your Progress")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Download Progress Report", use_container_width=True):
        report_data = {
            'Metric': ['Overall Progress', 'Modules Completed', 'Topics Completed', 'Questions Solved', 
                      'Accuracy', 'Mock Exams Passed', 'Study Streak', 'Total Study Hours', 'Readiness Score'],
            'Value': [f"{overall_progress:.0f}%", f"{progress['completed_modules']}/{progress['total_modules']}",
                     f"{progress['completed_topics']}/{progress['total_topics']}", 
                     f"{progress['solved_questions']}/{progress['total_questions']}",
                     f"{accuracy:.1f}%", f"{progress['mock_exams_passed']}/{progress['mock_exams_taken']}",
                     f"{progress['streak_days']} days", f"{progress['total_study_hours']:.1f} hours",
                     f"{readiness_score:.0f}%"]
        }
        
        df_report = pd.DataFrame(report_data)
        csv = df_report.to_csv(index=False)
        
        st.download_button("⬇️ Download CSV", data=csv, 
                          file_name=f"iwcf_progress_{today_dt.strftime('%Y%m%d')}.csv", mime="text/csv")

with col2:
    if DATA_MANAGER_AVAILABLE and st.button("🔄 Refresh Data", use_container_width=True):
        for key in ['user_progress', 'daily_activity', 'achievements', 'study_streak_dates']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ Data refreshed!")
        st.rerun()

with col3:
    if st.button("🎯 Set New Goal", use_container_width=True):
        with st.form("goal_form"):
            new_target_date = st.date_input("Target Exam Date:", value=target_date)
            
            if st.form_submit_button("Save Goal"):
                st.session_state.user_progress['target_exam_date'] = new_target_date.strftime('%Y-%m-%d')
                st.success("✅ Goal updated!")
                st.rerun()

# ═══════════════════════════════════════════════════════
# 📌 SIDEBAR
# ═══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("---")
    st.markdown("### 💾 Data Source")
    
    if DATA_MANAGER_AVAILABLE:
        st.success("✅ Real Progress Data")
        st.caption("Data synced with database")
    else:
        st.warning("⚠️ Demo Data Mode")
        st.caption("Progress not saved")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    st.metric("Total XP", progress['xp_points'])
    st.metric("Study Days", progress['study_days'])
    st.metric("Current Streak", f"{progress['streak_days']} 🔥")
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    
    if st.button("📚 Continue Learning", use_container_width=True):
        st.switch_page("pages/01_📚_Learn.py")
    
    if st.button("❓ Practice Quiz", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")
    
    if st.button("📝 Mock Exam", use_container_width=True):
        st.switch_page("pages/03_📝_Mock_Exam.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p style="margin: 0; font-size: 1.1rem;">
        🎓 <strong>Elshamy IWCF Mastery Method™</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0;">
        Progress Tracking Dashboard
    </p>
    <p style="margin: 1rem 0 0 0; font-size: 0.9rem; font-style: italic;">
        "Success is the sum of small efforts repeated day in and day out" 💪
    </p>
</div>
""", unsafe_allow_html=True)