"""
🛢️ ELSHAMY IWCF MASTERY SYSTEM™
Main Dashboard - Interactive Learning Platform
Created by Eng. Ahmed Elshamy | 2026 Edition
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
import os
import sys
from pathlib import Path
import random
import json

# ═══════════════════════════════════════════════════════
# 🔧 PATH SETUP
# ═══════════════════════════════════════════════════════

# Get project root directory
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════
# 📱 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Elshamy IWCF Mastery System",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# 💾 IMPORT DATA MANAGER
# ═══════════════════════════════════════════════════════

try:
    from utils.data_manager import (
        load_progress, 
        save_progress, 
        sync_to_session_state,
        calculate_overall_progress,
        calculate_predicted_score,
        get_user_level,
        get_overall_stats,
        DEFAULT_PROGRESS
    )
    DATA_MANAGER_AVAILABLE = True
except ImportError as e:
    DATA_MANAGER_AVAILABLE = False
    print(f"⚠️ Data Manager Import Error: {e}")

# ═══════════════════════════════════════════════════════
# 💾 INITIALIZE SESSION STATE
# ═══════════════════════════════════════════════════════

def init_session_state():
    """Initialize all session state variables"""
    
    if DATA_MANAGER_AVAILABLE:
        try:
            # Load real data
            sync_to_session_state()
            return True
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            print(f"Sync Error: {e}")
    
    # Demo data (fallback)
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "Engineer"
    if 'user_level' not in st.session_state:
        st.session_state.user_level = "Beginner"
    if 'study_streak' not in st.session_state:
        st.session_state.study_streak = 0
    if 'total_progress' not in st.session_state:
        st.session_state.total_progress = 0
    if 'modules_completed' not in st.session_state:
        st.session_state.modules_completed = 0
    if 'modules_total' not in st.session_state:
        st.session_state.modules_total = 8
    if 'questions_solved' not in st.session_state:
        st.session_state.questions_solved = 0
    if 'questions_correct' not in st.session_state:
        st.session_state.questions_correct = 0
    if 'exams_passed' not in st.session_state:
        st.session_state.exams_passed = 0
    if 'exams_total' not in st.session_state:
        st.session_state.exams_total = 10
    if 'predicted_score' not in st.session_state:
        st.session_state.predicted_score = 0
    if 'daily_challenge_progress' not in st.session_state:
        st.session_state.daily_challenge_progress = 0
    if 'weekly_hours' not in st.session_state:
        st.session_state.weekly_hours = [0, 0, 0, 0, 0, 0, 0]
    if 'last_study_time' not in st.session_state:
        st.session_state.last_study_time = "Never"
    if 'total_xp' not in st.session_state:
        st.session_state.total_xp = 0
    
    return False

# Initialize
data_loaded = init_session_state()

# Initialize Goal & Settings modals
if 'show_goal_modal' not in st.session_state:
    st.session_state.show_goal_modal = False
if 'show_settings_modal' not in st.session_state:
    st.session_state.show_settings_modal = False
if 'user_goal' not in st.session_state:
    st.session_state.user_goal = {
        'exam_date': None,
        'target_score': 80,
        'daily_hours': 2,
        'weekly_quizzes': 5
    }
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {
        'theme': 'Light',
        'notifications': True,
        'sound_effects': True,
        'language': 'English',
        'experience_level': 'Intermediate'
    }

# Show warning only once
if not DATA_MANAGER_AVAILABLE and 'dm_warning_shown' not in st.session_state:
    st.warning("⚠️ Data Manager not available. Using demo data. Progress will not be saved.")
    st.session_state.dm_warning_shown = True

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main theme colors */
    :root {
        --primary: #1E40AF;
        --secondary: #F59E0B;
        --success: #10B981;
        --danger: #EF4444;
        --purple: #8B5CF6;
    }
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid var(--primary);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Progress bar */
    .progress-container {
        background: #E5E7EB;
        border-radius: 20px;
        height: 30px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
        height: 100%;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        transition: width 1s ease;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(30, 64, 175, 0.4);
    }
    
    /* Modal styles */
    .modal-header-goal {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .modal-header-settings {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Goal display card */
    .goal-display {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    /* New user banner */
    .new-user-banner {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Level badge */
    .level-badge {
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    /* Tip box */
    .tip-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-left: 5px solid #F59E0B;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Activity item */
    .activity-item {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #3B82F6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎨 MAIN HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="main-header">
    <h1>🛢️ ELSHAMY IWCF MASTERY SYSTEM™</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Interactive Learning Platform - 2026 Edition
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9;">
        Created by Eng. Ahmed Elshamy | Your Path to IWCF Success
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎉 NEW USER BANNER
# ═══════════════════════════════════════════════════════

if st.session_state.questions_solved == 0 and st.session_state.modules_completed == 0:
    st.markdown("""
    <div class="new-user-banner">
        <h3 style="margin: 0;">🎉 Welcome to Your IWCF Journey!</h3>
        <p style="margin: 0.5rem 0 0 0;">
            Start learning now and track your real progress towards certification!
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 👤 USER WELCOME
# ═══════════════════════════════════════════════════════

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Dynamic welcome message
    streak_emoji = "🔥" if st.session_state.study_streak > 0 else "⭐"
    streak_text = f"{st.session_state.study_streak} days" if st.session_state.study_streak > 0 else "Start today!"
    
    st.markdown(f"""
    <div class="fade-in" style="background: white; padding: 1.5rem; 
         border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="margin: 0;">👋 Welcome back, {st.session_state.user_name}!</h2>
        <p style="color: #6B7280; margin-top: 0.5rem;">
            {streak_emoji} Study Streak: <strong>{streak_text}</strong> | 
            🏆 Level: <strong>{st.session_state.user_level}</strong> | 
            ⏰ Last study: <strong>{st.session_state.last_study_time}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🎯 Set Goal", use_container_width=True):
        st.session_state.show_goal_modal = True
        st.session_state.show_settings_modal = False
        st.rerun()

with col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.show_settings_modal = True
        st.session_state.show_goal_modal = False
        st.rerun()

# ═══════════════════════════════════════════════════════
# 🎯 SET GOAL MODAL
# ═══════════════════════════════════════════════════════

if st.session_state.show_goal_modal:
    st.markdown("---")
    st.markdown("""
    <div class="modal-header-goal">
        <h2 style="margin: 0;">🎯 Set Your Study Goal</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Define your targets for IWCF success!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        exam_date = st.date_input(
            "📅 Target Exam Date",
            value=None,
            min_value=date.today(),
            help="When do you plan to take the IWCF exam?"
        )
        
        target_score = st.slider(
            "🎯 Target Score (%)",
            min_value=50,
            max_value=100,
            value=st.session_state.user_goal['target_score'],
            step=5,
            help="What score are you aiming for? (Pass = 70%)"
        )
        
        # Visual indicator for target score
        if target_score >= 90:
            st.success("🌟 Excellent target! Aim for the stars!")
        elif target_score >= 80:
            st.info("👍 Great target! Very achievable with dedication.")
        elif target_score >= 70:
            st.warning("✅ This is the passing score. Aim higher for safety margin!")
        else:
            st.error("⚠️ This is below passing score (70%). Set a higher target!")
    
    with col_g2:
        daily_hours = st.slider(
            "⏰ Daily Study Hours",
            min_value=0.5,
            max_value=8.0,
            value=float(st.session_state.user_goal['daily_hours']),
            step=0.5,
            help="How many hours can you study daily?"
        )
        
        weekly_quizzes = st.slider(
            "📝 Weekly Quiz Goal",
            min_value=1,
            max_value=20,
            value=st.session_state.user_goal['weekly_quizzes'],
            step=1,
            help="How many quizzes per week?"
        )
        
        # Recommendation based on hours
        if daily_hours >= 4:
            st.success("🔥 Intensive study mode! You'll be ready fast!")
        elif daily_hours >= 2:
            st.info("👍 Good study pace. Steady progress!")
        else:
            st.warning("⚡ Consider increasing study time for better results.")
    
    # Calculate study plan
    if exam_date:
        days_left = (exam_date - date.today()).days
        
        if days_left > 0:
            total_hours = days_left * daily_hours
            total_questions = int(total_hours * 15)
            mock_exams = max(3, days_left // 7)
            
            st.markdown("---")
            st.markdown("### 📊 Your Personalized Study Plan")
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("📆 Days Left", f"{days_left}")
            with col_b:
                st.metric("⏱️ Total Hours", f"{total_hours:.0f}")
            with col_c:
                st.metric("❓ Questions", f"{total_questions:,}")
            with col_d:
                st.metric("📝 Mock Exams", f"{mock_exams}")
            
            # Progress indicator
            if days_left < 7:
                st.error("⚠️ Less than a week! Intensive revision mode recommended!")
            elif days_left < 14:
                st.warning("⏰ Two weeks left. Focus on weak areas and mock exams!")
            elif days_left < 30:
                st.info("📚 One month left. Good time to cover all modules!")
            else:
                st.success("✅ Plenty of time! Build strong foundations.")
                
        elif days_left == 0:
            st.warning("⚡ Your exam is TODAY! Good luck! 🍀")
        else:
            st.error("❌ This date is in the past. Please select a future date.")
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("✅ Save Goal", type="primary", use_container_width=True, key="save_goal"):
            st.session_state.user_goal = {
                'exam_date': str(exam_date) if exam_date else None,
                'target_score': target_score,
                'daily_hours': daily_hours,
                'weekly_quizzes': weekly_quizzes
            }
            
            # Save to data manager if available
            if DATA_MANAGER_AVAILABLE:
                try:
                    data = load_progress()
                    data['user_goal'] = st.session_state.user_goal
                    save_progress(data)
                except Exception as e:
                    print(f"Save goal error: {e}")
            
            st.session_state.show_goal_modal = False
            st.balloons()
            st.success("🎯 Goal saved successfully!")
            st.rerun()
    
    with col_btn2:
        if st.button("❌ Cancel", use_container_width=True, key="cancel_goal"):
            st.session_state.show_goal_modal = False
            st.rerun()
    
    with col_btn3:
        if st.button("🔄 Reset Goal", use_container_width=True, key="reset_goal"):
            st.session_state.user_goal = {
                'exam_date': None,
                'target_score': 80,
                'daily_hours': 2,
                'weekly_quizzes': 5
            }
            st.info("Goal reset to defaults.")
            st.rerun()
    
    st.markdown("---")

# ═══════════════════════════════════════════════════════
# ⚙️ SETTINGS MODAL
# ═══════════════════════════════════════════════════════

if st.session_state.show_settings_modal:
    st.markdown("---")
    st.markdown("""
    <div class="modal-header-settings">
        <h2 style="margin: 0;">⚙️ Settings</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Customize your learning experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "🎨 Appearance", "🔔 Notifications", "📊 Data"])
    
    with tab1:
        st.markdown("### 👤 Profile Settings")
        
        new_name = st.text_input(
            "Your Name",
            value=st.session_state.user_name,
            help="This name will be displayed throughout the app"
        )
        
        experience_level = st.selectbox(
            "Experience Level",
            ["Beginner", "Intermediate", "Advanced", "Expert"],
            index=["Beginner", "Intermediate", "Advanced", "Expert"].index(
                st.session_state.user_settings.get('experience_level', 'Intermediate')
            ),
            help="This helps personalize your learning path"
        )
        
        st.markdown("---")
        st.markdown("### 📧 Contact (Optional)")
        email = st.text_input("Email", placeholder="your.email@example.com")
        
    with tab2:
        st.markdown("### 🎨 Appearance Settings")
        
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "Auto"],
            index=["Light", "Dark", "Auto"].index(
                st.session_state.user_settings.get('theme', 'Light')
            ),
            help="Choose your preferred color theme"
        )
        
        st.info("💡 Theme changes will apply on next reload.")
        
        st.markdown("### 🔤 Font Size")
        font_size = st.select_slider(
            "Font Size",
            options=["Small", "Medium", "Large", "Extra Large"],
            value="Medium"
        )
        
    with tab3:
        st.markdown("### 🔔 Notification Settings")
        
        notifications = st.toggle(
            "Enable Notifications",
            value=st.session_state.user_settings.get('notifications', True),
            help="Get reminders for daily study goals"
        )
        
        sound_effects = st.toggle(
            "Sound Effects",
            value=st.session_state.user_settings.get('sound_effects', True),
            help="Play sounds for correct/incorrect answers"
        )
        
        if notifications:
            st.markdown("### ⏰ Reminder Time")
            reminder_time = st.time_input("Daily Reminder", value=None)
            
            st.markdown("### 📱 Reminder Types")
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                st.checkbox("Daily study reminder", value=True)
                st.checkbox("Quiz completion reminder", value=True)
            with col_n2:
                st.checkbox("Streak protection alert", value=True)
                st.checkbox("Weekly progress report", value=False)
    
    with tab4:
        st.markdown("### 📊 Data Management")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("#### 📥 Export Data")
            if st.button("📄 Export Progress as JSON", use_container_width=True, key="export_json"):
                if DATA_MANAGER_AVAILABLE:
                    try:
                        data = load_progress()
                        export_data = {
                            'user_name': st.session_state.user_name,
                            'progress': data,
                            'goals': st.session_state.user_goal,
                            'settings': st.session_state.user_settings,
                            'export_date': str(datetime.now())
                        }
                        st.download_button(
                            label="⬇️ Download JSON File",
                            data=json.dumps(export_data, indent=2),
                            file_name=f"iwcf_progress_{date.today()}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Export failed: {e}")
                else:
                    # Demo mode export
                    demo_data = {
                        'user_name': st.session_state.user_name,
                        'total_progress': st.session_state.total_progress,
                        'questions_solved': st.session_state.questions_solved,
                        'modules_completed': st.session_state.modules_completed,
                        'goals': st.session_state.user_goal,
                        'export_date': str(datetime.now()),
                        'mode': 'demo'
                    }
                    st.download_button(
                        label="⬇️ Download JSON File",
                        data=json.dumps(demo_data, indent=2),
                        file_name=f"iwcf_progress_{date.today()}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            if st.button("📊 Export as CSV", use_container_width=True, key="export_csv"):
                csv_data = f"""Field,Value
Name,{st.session_state.user_name}
Progress,{st.session_state.total_progress}%
Questions Solved,{st.session_state.questions_solved}
Modules Completed,{st.session_state.modules_completed}
Study Streak,{st.session_state.study_streak} days
Predicted Score,{st.session_state.predicted_score}%
Export Date,{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
                st.download_button(
                    label="⬇️ Download CSV File",
                    data=csv_data,
                    file_name=f"iwcf_progress_{date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col_d2:
            st.markdown("#### 🗑️ Reset Data")
            
            st.warning("⚠️ These actions cannot be undone!")
            
            if st.button("🔄 Reset Progress Only", use_container_width=True, key="reset_progress"):
                st.session_state.total_progress = 0
                st.session_state.questions_solved = 0
                st.session_state.questions_correct = 0
                st.session_state.modules_completed = 0
                st.session_state.study_streak = 0
                st.session_state.exams_passed = 0
                st.session_state.predicted_score = 0
                st.session_state.total_xp = 0
                st.session_state.daily_challenge_progress = 0
                
                if DATA_MANAGER_AVAILABLE:
                    try:
                        save_progress(DEFAULT_PROGRESS)
                    except:
                        pass
                
                st.success("✅ Progress reset!")
                st.rerun()
            
            st.markdown("---")
            
            confirm_reset = st.checkbox("I understand this will delete ALL my data", key="confirm_full_reset")
            
            if st.button("🗑️ Reset Everything", use_container_width=True, disabled=not confirm_reset, key="reset_all"):
                if DATA_MANAGER_AVAILABLE:
                    try:
                        save_progress(DEFAULT_PROGRESS)
                    except:
                        pass
                
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                    
                st.success("✅ All data reset!")
                st.rerun()
    
    st.markdown("---")
    
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    
    with col_s1:
        if st.button("✅ Save Settings", type="primary", use_container_width=True, key="save_settings"):
            st.session_state.user_name = new_name
            st.session_state.user_settings = {
                'theme': theme,
                'notifications': notifications,
                'sound_effects': sound_effects,
                'language': 'English',
                'experience_level': experience_level
            }
            
            # Save to data manager if available
            if DATA_MANAGER_AVAILABLE:
                try:
                    data = load_progress()
                    data['user_name'] = new_name
                    if 'user_settings' not in data:
                        data['user_settings'] = {}
                    data['user_settings'] = st.session_state.user_settings
                    save_progress(data)
                except Exception as e:
                    print(f"Save settings error: {e}")
            
            st.session_state.show_settings_modal = False
            st.success("✅ Settings saved successfully!")
            st.rerun()
    
    with col_s2:
        if st.button("❌ Cancel", use_container_width=True, key="cancel_settings"):
            st.session_state.show_settings_modal = False
            st.rerun()
    
    with col_s3:
        if st.button("🔄 Reset to Default", use_container_width=True, key="reset_settings"):
            st.session_state.user_name = "Engineer"
            st.session_state.user_settings = {
                'theme': 'Light',
                'notifications': True,
                'sound_effects': True,
                'language': 'English',
                'experience_level': 'Intermediate'
            }
            st.info("Settings reset to defaults.")
            st.rerun()
    
    st.markdown("---")
    
    # App Info
    st.markdown("""
    <div style="text-align: center; color: #6B7280; padding: 1rem; 
                background: #F3F4F6; border-radius: 10px;">
        <p style="margin: 0;"><strong>🛢️ Elshamy IWCF Mastery System™</strong></p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">Version 1.0.0 | 2026 Edition</p>
        <p style="margin: 0; font-size: 0.85rem;">Created by Eng. Ahmed Elshamy</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.7;">© 2026 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎯 SHOW CURRENT GOAL (if set and modals closed)
# ═══════════════════════════════════════════════════════

if (st.session_state.user_goal.get('exam_date') and 
    not st.session_state.show_goal_modal and 
    not st.session_state.show_settings_modal):
    try:
        exam_date_str = st.session_state.user_goal['exam_date']
        exam_date_obj = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        days_left = (exam_date_obj - date.today()).days
        
        if days_left > 0:
            st.markdown(f"""
            <div class="goal-display">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        🎯 <strong>Your Goal:</strong> Score {st.session_state.user_goal['target_score']}% by {exam_date_obj.strftime('%B %d, %Y')}
                    </div>
                    <div style="margin-top: 0.5rem;">
                        📆 <strong>{days_left} days left</strong> | 
                        ⏰ {st.session_state.user_goal['daily_hours']}h/day | 
                        📝 {st.session_state.user_goal['weekly_quizzes']} quizzes/week
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        print(f"Goal display error: {e}")

# ═══════════════════════════════════════════════════════
# 🏆 LEVEL BADGE (if XP available)
# ═══════════════════════════════════════════════════════

if (not st.session_state.show_goal_modal and 
    not st.session_state.show_settings_modal and
    hasattr(st.session_state, 'total_xp') and 
    st.session_state.total_xp > 0):
    
    current_xp = st.session_state.total_xp
    current_level = (current_xp // 500) + 1
    xp_in_level = current_xp % 500
    level_progress = (xp_in_level / 500) * 100
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown(f"""
        <div class="level-badge">
            <h3 style="margin: 0;">🏆 Level {current_level}</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
                {xp_in_level} / 500 XP ({int(level_progress)}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(level_progress / 100)
        st.caption(f"🎯 {500 - xp_in_level} XP to Level {current_level + 1}")

# ═══════════════════════════════════════════════════════
# 📊 PROGRESS OVERVIEW (only if modals are closed)
# ═══════════════════════════════════════════════════════

if not st.session_state.show_goal_modal and not st.session_state.show_settings_modal:
    
    st.markdown("---")
    st.markdown("## 📊 Your Learning Progress")
    
    # Progress bar
    progress = st.session_state.total_progress
    progress_color = "#10B981" if progress >= 70 else "#F59E0B" if progress >= 40 else "#3B82F6"
    
    st.markdown(f"""
    <div class="progress-container fade-in">
        <div class="progress-bar" style="width: {max(progress, 5)}%; 
             background: linear-gradient(90deg, {progress_color} 0%, {progress_color}90 100%);">
            {progress:.1f}% Complete
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Motivational message based on progress
    if progress == 0:
        st.info("🚀 **Start your journey!** Every expert was once a beginner.")
    elif progress < 25:
        st.info("📚 **Great start!** Keep going, you're building a solid foundation.")
    elif progress < 50:
        st.success("💪 **Good progress!** You're almost halfway there!")
    elif progress < 75:
        st.success("🔥 **Excellent!** You're on track for success!")
    else:
        st.success("🏆 **Outstanding!** You're almost ready for the exam!")
    
    # ═══════════════════════════════════════════════════════
    # 📈 STATS CARDS
    # ═══════════════════════════════════════════════════════
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        modules_pct = (st.session_state.modules_completed / st.session_state.modules_total * 100) if st.session_state.modules_total > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #1E40AF; margin: 0;">📚 {st.session_state.modules_completed}/{st.session_state.modules_total}</h3>
            <p style="color: #6B7280; margin-top: 0.5rem;">Modules Completed</p>
            <p style="color: #10B981; font-size: 0.85rem; margin-top: 0.3rem;">{modules_pct:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        accuracy = 0
        if st.session_state.questions_solved > 0 and hasattr(st.session_state, 'questions_correct'):
            accuracy = (st.session_state.questions_correct / st.session_state.questions_solved * 100)
        st.markdown(f"""
        <div class="stat-card" style="animation-delay: 0.1s;">
            <h3 style="color: #10B981; margin: 0;">⚡ {st.session_state.questions_solved}</h3>
            <p style="color: #6B7280; margin-top: 0.5rem;">Questions Solved</p>
            <p style="color: #10B981; font-size: 0.85rem; margin-top: 0.3rem;">{accuracy:.0f}% accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="animation-delay: 0.2s;">
            <h3 style="color: #F59E0B; margin: 0;">✅ {st.session_state.exams_passed}/{st.session_state.exams_total}</h3>
            <p style="color: #6B7280; margin-top: 0.5rem;">Mock Exams Passed</p>
            <p style="color: #F59E0B; font-size: 0.85rem; margin-top: 0.3rem;">70% to pass</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        score_color = "#10B981" if st.session_state.predicted_score >= 70 else "#F59E0B" if st.session_state.predicted_score >= 50 else "#EF4444"
        st.markdown(f"""
        <div class="stat-card" style="animation-delay: 0.3s;">
            <h3 style="color: {score_color}; margin: 0;">🎯 {st.session_state.predicted_score}%</h3>
            <p style="color: #6B7280; margin-top: 0.5rem;">Predicted Score</p>
            <p style="color: {score_color}; font-size: 0.85rem; margin-top: 0.3rem;">
                {'Ready!' if st.session_state.predicted_score >= 70 else 'Keep studying!'}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # 🎓 QUICK ACCESS
    # ═══════════════════════════════════════════════════════
    
    st.markdown("---")
    st.markdown("## 🎓 Quick Access")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚\n\nLearn\n\nStart Module", key="btn_learn"):
            if os.path.exists("pages/01_📚_Learn.py"):
                st.switch_page("pages/01_📚_Learn.py")
            else:
                st.warning("📚 Learn page is under construction!")
    
    with col2:
        if st.button("❓\n\nQuiz\n\nPractice Questions", key="btn_quiz"):
            if os.path.exists("pages/02_❓_Quiz.py"):
                st.switch_page("pages/02_❓_Quiz.py")
            else:
                st.warning("❓ Quiz page is under construction!")
    
    with col3:
        if st.button("📝\n\nMock Exam\n\nTest Yourself", key="btn_exam"):
            if os.path.exists("pages/03_📝_Mock_Exam.py"):
                st.switch_page("pages/03_📝_Mock_Exam.py")
            else:
                st.warning("📝 Mock Exam page is under construction!")
    
    with col4:
        if st.button("🧮\n\nCalculator\n\nSolve Problems", key="btn_calc"):
            if os.path.exists("pages/04_🧮_Calculator.py"):
                st.switch_page("pages/04_🧮_Calculator.py")
            else:
                st.warning("🧮 Calculator page is under construction!")
    
    # ═══════════════════════════════════════════════════════
    # 🔥 DAILY CHALLENGE
    # ═══════════════════════════════════════════════════════
    
    st.markdown("---")
    st.markdown("## 🔥 Daily Challenge")
    
    daily_progress = st.session_state.daily_challenge_progress
    daily_total = 10
    daily_pct = (daily_progress / daily_total) * 100
    
    if daily_progress >= daily_total:
        st.markdown("""
        <div class="fade-in" style="background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); 
             padding: 2rem; border-radius: 15px; border-left: 5px solid #10B981;">
            <h3 style="margin: 0; color: #065F46;">🎉 Daily Challenge Complete!</h3>
            <p style="color: #047857; margin-top: 0.5rem;">
                Congratulations! You've earned +50 XP! Come back tomorrow for a new challenge! 🏅
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="fade-in" style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
             padding: 2rem; border-radius: 15px; border-left: 5px solid #F59E0B;">
            <h3 style="margin: 0; color: #92400E;">💎 Solve 10 questions to unlock today's reward!</h3>
            <p style="color: #78350F; margin-top: 0.5rem;">
                Complete the challenge and earn 50 XP + Special Badge 🏅
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="progress-container" style="margin-top: 1rem;">
        <div class="progress-bar" style="width: {max(daily_pct, 5)}%; 
             background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 100%);">
            {daily_progress}/{daily_total} Questions
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if daily_progress < daily_total:
        if st.button("🚀 Continue Challenge", use_container_width=True, key="btn_challenge"):
            if os.path.exists("pages/02_❓_Quiz.py"):
                st.switch_page("pages/02_❓_Quiz.py")
            else:
                st.success("Challenge mode activated!")
    
    # ═══════════════════════════════════════════════════════
    # 📈 STUDY ANALYTICS
    # ═══════════════════════════════════════════════════════
    
    st.markdown("---")
    st.markdown("## 📈 Study Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Weekly Activity")
        
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = st.session_state.weekly_hours
        
        fig = go.Figure(data=[
            go.Bar(
                x=days, 
                y=hours,
                marker_color=['#1E40AF' if h >= 2 else '#9CA3AF' for h in hours],
                text=[f'{h:.1f}h' for h in hours],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            yaxis_title="Hours Studied",
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        total_hours = sum(hours)
        st.metric("This Week", f"{total_hours:.1f} hours", f"Goal: 14 hours")
    
    with col2:
        st.markdown("### 🎯 Module Completion")
        
        completed = st.session_state.modules_completed
        in_progress = 1 if completed < st.session_state.modules_total else 0
        not_started = max(0, st.session_state.modules_total - completed - in_progress)
        
        labels = ['Completed', 'In Progress', 'Not Started']
        values = [completed, in_progress, not_started]
        colors = ['#10B981', '#F59E0B', '#E5E7EB']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=colors
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════
    # 💡 TIP OF THE DAY
    # ═══════════════════════════════════════════════════════
    
    st.markdown("---")
    
    tips = [
        "💡 **Pro Tip:** Focus on understanding concepts, not just memorizing formulas!",
        "💡 **Study Hack:** Practice calculations daily to build muscle memory!",
        "💡 **Exam Strategy:** Always read the question twice before answering!",
        "💡 **Time Management:** Spend max 1.5 minutes per question in the exam!",
        "💡 **Retention Boost:** Review topics within 24 hours for better retention!",
        "💡 **Confidence Builder:** Take practice quizzes before attempting mock exams!",
        "💡 **Common Mistake:** Don't confuse SIDPP and SICP - practice identifying them!",
        "💡 **Success Formula:** Consistency beats intensity. Study 2 hours daily!",
        "💡 **Mental Prep:** Visualize success before taking mock exams!",
        "💡 **Smart Review:** Focus 80% of study time on weak areas!",
    ]
    
    # Seed random with date so tip changes daily
    random.seed(datetime.now().strftime("%Y-%m-%d"))
    tip = random.choice(tips)
    
    st.markdown(f"""
    <div class="tip-box">
        {tip}
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # 🎯 RECOMMENDED NEXT STEPS
    # ═══════════════════════════════════════════════════════
    
    st.markdown("---")
    st.markdown("## 🎯 Recommended for You")
    
    col1, col2, col3 = st.columns(3)
    
    # Dynamic recommendations
    with col1:
        if st.session_state.modules_completed < st.session_state.modules_total:
            next_module = st.session_state.modules_completed + 1
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #1E40AF;">
                <h4>📚 Continue Learning</h4>
                <p style="color: #6B7280;">Module {next_module} awaits!</p>
                <p style="color: #10B981; font-weight: 600;">Start now</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #10B981;">
                <h4>📚 All Modules Complete!</h4>
                <p style="color: #6B7280;">Great job!</p>
                <p style="color: #10B981; font-weight: 600;">Review any module</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Continue →", key="resume_learn", use_container_width=True):
            if os.path.exists("pages/01_📚_Learn.py"):
                st.switch_page("pages/01_📚_Learn.py")
    
    with col2:
        if st.session_state.questions_solved > 0 and hasattr(st.session_state, 'questions_correct'):
            accuracy = (st.session_state.questions_correct / st.session_state.questions_solved * 100)
            if accuracy < 70:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #EF4444;">
                    <h4>💪 Practice More</h4>
                    <p style="color: #6B7280;">Current: {accuracy:.0f}%</p>
                    <p style="color: #EF4444; font-weight: 600;">Target: 70%+</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #10B981;">
                    <h4>💪 Great Accuracy!</h4>
                    <p style="color: #6B7280;">Current: {accuracy:.0f}%</p>
                    <p style="color: #10B981; font-weight: 600;">Keep it up!</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #F59E0B;">
                <h4>💪 Start Practicing</h4>
                <p style="color: #6B7280;">No questions yet</p>
                <p style="color: #F59E0B; font-weight: 600;">Begin now!</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Practice →", key="practice_weak", use_container_width=True):
            if os.path.exists("pages/02_❓_Quiz.py"):
                st.switch_page("pages/02_❓_Quiz.py")
    
    with col3:
        if st.session_state.predicted_score >= 70:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #10B981;">
                <h4>📝 Ready for Exam!</h4>
                <p style="color: #6B7280;">Predicted: {st.session_state.predicted_score}%</p>
                <p style="color: #10B981; font-weight: 600;">Take a mock exam</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; border-top: 4px solid #F59E0B;">
                <h4>📝 Mock Exam</h4>
                <p style="color: #6B7280;">Test your knowledge</p>
                <p style="color: #F59E0B; font-weight: 600;">When ready</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Start →", key="start_exam", use_container_width=True):
            if os.path.exists("pages/03_📝_Mock_Exam.py"):
                st.switch_page("pages/03_📝_Mock_Exam.py")
    
    # ═══════════════════════════════════════════════════════
    # 📜 RECENT ACTIVITY
    # ═══════════════════════════════════════════════════════
    
    if DATA_MANAGER_AVAILABLE:
        st.markdown("---")
        st.markdown("## 📜 Recent Activity")
        
        try:
            data = load_progress()
            
            # Collect recent activities
            activities = []
            
            # Recent topics completed
            if data.get('modules', {}).get('completed_topics'):
                recent_topics = data['modules']['completed_topics'][-3:]
                for topic in reversed(recent_topics):
                    activities.append({
                        'icon': '✅',
                        'text': f"Completed topic: **{topic}**",
                        'color': '#10B981'
                    })
            
            # Recent exams
            if data.get('exams', {}).get('exam_history'):
                recent_exams = data['exams']['exam_history'][-2:]
                for exam in reversed(recent_exams):
                    icon = "✅" if exam.get('passed') else "📝"
                    status = "PASSED" if exam.get('passed') else "ATTEMPTED"
                    color = "#10B981" if exam.get('passed') else "#F59E0B"
                    activities.append({
                        'icon': icon,
                        'text': f"Mock Exam {status}: **{exam.get('score', 0)}%** • {exam.get('date', 'N/A')}",
                        'color': color
                    })
            
            # Show activities
            if activities:
                for activity in activities[:5]:  # Show last 5
                    st.markdown(f"""
                    <div class="activity-item" style="border-left-color: {activity['color']};">
                        {activity['icon']} {activity['text']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📝 No recent activity. Start learning to see your progress here!")
        
        except Exception as e:
            print(f"Activity Error: {e}")

# ═══════════════════════════════════════════════════════
# 📌 SIDEBAR
# ═══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("---")
    
    # System Status
    st.markdown("### 💾 System Status")
    if DATA_MANAGER_AVAILABLE:
        st.success("✅ Data Manager: Active")
        st.caption("✓ Progress auto-saved")
    else:
        st.warning("⚠️ Demo Mode")
        st.caption("⚠ Progress not saved")
    
    st.markdown("---")
    
    # User Stats
    st.markdown("### 🌟 Your Stats")
    
    if hasattr(st.session_state, 'total_xp'):
        st.metric("Total XP", st.session_state.total_xp)
        
        # Next level calculation
        current_xp = st.session_state.total_xp
        next_level_xp = (((current_xp // 500) + 1) * 500)
        xp_needed = next_level_xp - current_xp
        st.caption(f"🎯 {xp_needed} XP to next level")
    
    st.metric("Current Level", st.session_state.user_level)
    st.metric("Study Streak", f"{st.session_state.study_streak} days")
    
    # Streak motivation
    if st.session_state.study_streak == 0:
        st.info("💡 Start your streak today!")
    elif st.session_state.study_streak < 7:
        days_to_badge = 7 - st.session_state.study_streak
        st.success(f"🔥 {days_to_badge} days to weekly badge!")
    elif st.session_state.study_streak >= 7:
        st.success("🏆 Weekly streak achieved!")
    
    st.markdown("---")
    
    # Quick links
    st.markdown("### 🔗 Quick Links")
    
    if st.button("📊 View Full Progress", use_container_width=True, key="sidebar_progress"):
        if os.path.exists("pages/05_📊_Progress.py"):
            st.switch_page("pages/05_📊_Progress.py")
        else:
            st.info("Progress page coming soon!")
    
    if st.button("📖 Formulas Reference", use_container_width=True, key="sidebar_formulas"):
        if os.path.exists("pages/06_📖_Formulas.py"):
            st.switch_page("pages/06_📖_Formulas.py")
        else:
            st.info("Formulas page coming soon!")
    
    if st.button("🤖 AI Tutor", use_container_width=True, key="sidebar_ai"):
        if os.path.exists("pages/07_🤖_AI_Tutor.py"):
            st.switch_page("pages/07_🤖_AI_Tutor.py")
        else:
            st.info("AI Tutor coming soon!")
    
    st.markdown("---")
    
    # Reset option (only in demo mode)
    if not DATA_MANAGER_AVAILABLE:
        st.markdown("### 🔄 Demo Controls")
        if st.button("Reset Demo Data", use_container_width=True, key="reset_demo"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")

# Show XP if available
if DATA_MANAGER_AVAILABLE and hasattr(st.session_state, 'total_xp') and st.session_state.total_xp > 0:
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%); 
         padding: 1rem; border-radius: 12px; margin-bottom: 1rem; color: white;">
        <span style="font-size: 1.2rem;">⭐ Total XP: <strong>{st.session_state.total_xp}</strong> 
        | 🏆 Level: <strong>{(st.session_state.total_xp // 500) + 1}</strong></span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p style="margin: 0;">
        🎓 <strong>Elshamy IWCF Mastery Method™ 2026</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0;">
        Created by Eng. Ahmed Elshamy | © 2026 All Rights Reserved
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Your Success is My Mission" 💪
    </p>
</div>
""", unsafe_allow_html=True)