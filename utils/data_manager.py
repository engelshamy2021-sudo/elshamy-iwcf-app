"""
🎯 ELSHAMY IWCF - Data Manager (Fixed Version)
Comprehensive data persistence with backwards compatibility
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# ═══════════════════════════════════════════════════════
# 📂 PATHS SETUP
# ═══════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
USER_DATA_DIR = PROJECT_ROOT / "user_data"

PROGRESS_FILE = DATA_DIR / "user_progress.json"
LEGACY_PROGRESS = USER_DATA_DIR / "progress.json"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
USER_DATA_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════
# 🏗️ DEFAULT DATA STRUCTURE
# ═══════════════════════════════════════════════════════

DEFAULT_PROGRESS = {
    "user_info": {
        "name": "Engineer",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": "Beginner",
        "joined_date": datetime.now().strftime("%Y-%m-%d")
    },
    
    "modules": {
        "total": 8,
        "completed": [],
        "completed_topics": [],
        "in_progress": [],
        "bookmarked_topics": [],
        "module_progress": {
            "1": 0, "2": 0, "3": 0, "4": 0,
            "5": 0, "6": 0, "7": 0, "8": 0
        },
        "topics_completed": []
    },
    
    "quiz": {
        "questions_solved": 0,
        "total_attempted": 0,
        "questions_correct": 0,
        "total_correct": 0,
        "questions_wrong": 0,
        "by_module": {
            "1": {"total": 0, "correct": 0},
            "2": {"total": 0, "correct": 0},
            "3": {"total": 0, "correct": 0},
            "4": {"total": 0, "correct": 0},
            "5": {"total": 0, "correct": 0},
            "6": {"total": 0, "correct": 0},
            "7": {"total": 0, "correct": 0},
            "8": {"total": 0, "correct": 0}
        },
        "by_category": {},
        "by_topic": {},
        "completed": 0,
        "scores": []
    },
    
    "exams": {
        "total": 10,
        "mock_exams_taken": 0,
        "mock_exams_passed": 0,
        "attempted": [],
        "passed": [],
        "best_score": 0,
        "average_score": 0,
        "exam_history": [],
        "scores": {}
    },
    
    "achievements": {
        "xp_total": 0,
        "level": 1,
        "badges": [],
        "unlocked": [],
        "study_streak": 0,
        "last_study_date": datetime.now().strftime("%Y-%m-%d")
    },
    
    "flashcards": {
        "reviewed": 0,
        "mastered": []
    },
    
    "scenarios": {
        "completed": [],
        "scores": {}
    },
    
    "daily_challenge": {
        "date": None,
        "progress": 0,
        "completed": False
    },
    
    "study_time": {
        "total_minutes": 0,
        "by_date": {},
        "weekly": [0, 0, 0, 0, 0, 0, 0]
    },
    
    "settings": {
        "difficulty": "medium",
        "show_hints": True,
        "dark_mode": False
    }
}

# ═══════════════════════════════════════════════════════
# 💾 FILE OPERATIONS
# ═══════════════════════════════════════════════════════

def save_json(filepath, data):
    """Save data to JSON file"""
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Save Error: {e}")
        return False


def load_json(filepath, default=None):
    """Load data from JSON file"""
    filepath = Path(filepath)
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Load Error: {e}")
            return default if default else {}
    return default if default else {}

# ═══════════════════════════════════════════════════════
# 🔧 ENSURE ALL KEYS (CRITICAL FIX)
# ═══════════════════════════════════════════════════════

def ensure_all_keys(data):
    """Ensure all required keys exist - with deep merge"""
    
    if data is None:
        return DEFAULT_PROGRESS.copy()
    
    # ═══ MAIN SECTIONS ═══
    
    # user_info
    if 'user_info' not in data:
        data['user_info'] = DEFAULT_PROGRESS['user_info'].copy()
    else:
        for key in DEFAULT_PROGRESS['user_info']:
            if key not in data['user_info']:
                data['user_info'][key] = DEFAULT_PROGRESS['user_info'][key]
    
    # modules
    if 'modules' not in data:
        data['modules'] = DEFAULT_PROGRESS['modules'].copy()
    else:
        for key in DEFAULT_PROGRESS['modules']:
            if key not in data['modules']:
                data['modules'][key] = DEFAULT_PROGRESS['modules'][key]
        # Ensure completed_topics is a list
        if not isinstance(data['modules'].get('completed_topics'), list):
            data['modules']['completed_topics'] = []
        if not isinstance(data['modules'].get('bookmarked_topics'), list):
            data['modules']['bookmarked_topics'] = []
        if not isinstance(data['modules'].get('topics_completed'), list):
            data['modules']['topics_completed'] = []
    
    # quiz
    if 'quiz' not in data:
        data['quiz'] = DEFAULT_PROGRESS['quiz'].copy()
    else:
        for key in DEFAULT_PROGRESS['quiz']:
            if key not in data['quiz']:
                data['quiz'][key] = DEFAULT_PROGRESS['quiz'][key]
        # Sync old/new field names
        if 'total_attempted' in data['quiz']:
            data['quiz']['questions_solved'] = data['quiz']['total_attempted']
        if 'total_correct' in data['quiz']:
            data['quiz']['questions_correct'] = data['quiz']['total_correct']
    
    # exams
    if 'exams' not in data:
        data['exams'] = DEFAULT_PROGRESS['exams'].copy()
    else:
        for key in DEFAULT_PROGRESS['exams']:
            if key not in data['exams']:
                data['exams'][key] = DEFAULT_PROGRESS['exams'][key]
        # Ensure exam_history is a list
        if not isinstance(data['exams'].get('exam_history'), list):
            data['exams']['exam_history'] = []
    
    # achievements
    if 'achievements' not in data:
        data['achievements'] = DEFAULT_PROGRESS['achievements'].copy()
    else:
        for key in DEFAULT_PROGRESS['achievements']:
            if key not in data['achievements']:
                data['achievements'][key] = DEFAULT_PROGRESS['achievements'][key]
    
    # flashcards
    if 'flashcards' not in data:
        data['flashcards'] = DEFAULT_PROGRESS['flashcards'].copy()
    
    # scenarios
    if 'scenarios' not in data:
        data['scenarios'] = DEFAULT_PROGRESS['scenarios'].copy()
    
    # daily_challenge
    if 'daily_challenge' not in data:
        data['daily_challenge'] = DEFAULT_PROGRESS['daily_challenge'].copy()
    
    # study_time
    if 'study_time' not in data:
        data['study_time'] = DEFAULT_PROGRESS['study_time'].copy()
    else:
        for key in DEFAULT_PROGRESS['study_time']:
            if key not in data['study_time']:
                data['study_time'][key] = DEFAULT_PROGRESS['study_time'][key]
    
    # settings
    if 'settings' not in data:
        data['settings'] = DEFAULT_PROGRESS['settings'].copy()
    
    return data

# ═══════════════════════════════════════════════════════
# 📖 LOAD PROGRESS
# ═══════════════════════════════════════════════════════

def load_progress():
    """Load user progress from file"""
    try:
        data = None
        
        # Try main file first
        if PROGRESS_FILE.exists():
            data = load_json(PROGRESS_FILE)
        # Fallback to legacy
        elif LEGACY_PROGRESS.exists():
            data = load_json(LEGACY_PROGRESS)
        
        # Use default if nothing loaded
        if data is None or not data:
            data = DEFAULT_PROGRESS.copy()
        
        # CRITICAL: Ensure all keys exist
        data = ensure_all_keys(data)
        
        # Update last login
        data['user_info']['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update study streak
        data = update_streak(data)
        
        # Save updated data
        save_progress(data)
        
        return data
    
    except Exception as e:
        print(f"Load Progress Error: {e}")
        return DEFAULT_PROGRESS.copy()

# ═══════════════════════════════════════════════════════
# 💾 SAVE PROGRESS
# ═══════════════════════════════════════════════════════

def save_progress(data):
    """Save user progress to file"""
    try:
        # Ensure all keys before saving
        data = ensure_all_keys(data)
        
        save_json(PROGRESS_FILE, data)
        save_json(LEGACY_PROGRESS, data)  # Backup
        return True
    except Exception as e:
        print(f"Save Progress Error: {e}")
        return False

# ═══════════════════════════════════════════════════════
# 🔥 STREAK MANAGEMENT
# ═══════════════════════════════════════════════════════

def update_streak(data):
    """Update study streak"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        last_study = data.get('achievements', {}).get('last_study_date', '')
        
        if last_study == today:
            pass  # Already studied today
        elif last_study == yesterday:
            data['achievements']['study_streak'] = data['achievements'].get('study_streak', 0) + 1
            data['achievements']['last_study_date'] = today
        else:
            data['achievements']['study_streak'] = 1
            data['achievements']['last_study_date'] = today
    except:
        data['achievements']['study_streak'] = 1
        data['achievements']['last_study_date'] = datetime.now().strftime("%Y-%m-%d")
    
    return data

# ═══════════════════════════════════════════════════════
# 📚 MODULE / TOPIC COMPLETION
# ═══════════════════════════════════════════════════════

def record_topic_complete(topic_name, module_id):
    """Record topic completion"""
    data = load_progress()
    
    if topic_name not in data['modules']['completed_topics']:
        data['modules']['completed_topics'].append(topic_name)
        data['modules']['topics_completed'].append(topic_name)
        
        data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 25
        data['achievements']['level'] = get_level_from_xp(data['achievements']['xp_total'])
        
        save_progress(data)
        return True
    return False


def record_module_complete(module_name):
    """Record module completion"""
    data = load_progress()
    
    if module_name not in data['modules']['completed']:
        data['modules']['completed'].append(module_name)
        data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 100
        
        if module_name in data['modules'].get('in_progress', []):
            data['modules']['in_progress'].remove(module_name)
        
        save_progress(data)
        return True
    return False


def get_module_progress(module_id, total_topics):
    """Calculate module progress percentage"""
    data = load_progress()
    completed = len(data['modules'].get('completed_topics', []))
    return (completed / total_topics * 100) if total_topics > 0 else 0

# ═══════════════════════════════════════════════════════
# ❓ QUIZ TRACKING
# ═══════════════════════════════════════════════════════

def record_quiz_answer(module_id, is_correct, topic=None, category=None):
    """Record quiz answer"""
    data = load_progress()
    
    # Update totals
    data['quiz']['questions_solved'] = data['quiz'].get('questions_solved', 0) + 1
    data['quiz']['total_attempted'] = data['quiz'].get('total_attempted', 0) + 1
    
    if is_correct:
        data['quiz']['questions_correct'] = data['quiz'].get('questions_correct', 0) + 1
        data['quiz']['total_correct'] = data['quiz'].get('total_correct', 0) + 1
        data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 10
    else:
        data['quiz']['questions_wrong'] = data['quiz'].get('questions_wrong', 0) + 1
        data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 1
    
    # By module
    mod_str = str(module_id)
    if mod_str not in data['quiz']['by_module']:
        data['quiz']['by_module'][mod_str] = {'total': 0, 'correct': 0}
    data['quiz']['by_module'][mod_str]['total'] += 1
    if is_correct:
        data['quiz']['by_module'][mod_str]['correct'] += 1
    
    # By topic
    if topic:
        if topic not in data['quiz']['by_topic']:
            data['quiz']['by_topic'][topic] = {'total': 0, 'correct': 0}
        data['quiz']['by_topic'][topic]['total'] += 1
        if is_correct:
            data['quiz']['by_topic'][topic]['correct'] += 1
    
    # By category
    if category:
        if category not in data['quiz']['by_category']:
            data['quiz']['by_category'][category] = {'attempted': 0, 'correct': 0}
        data['quiz']['by_category'][category]['attempted'] += 1
        if is_correct:
            data['quiz']['by_category'][category]['correct'] += 1
    
    # Update level
    data['achievements']['level'] = get_level_from_xp(data['achievements']['xp_total'])
    
    # Update streak
    data = update_streak(data)
    
    # Update daily challenge
    data = update_daily_challenge(data)
    
    save_progress(data)


def get_quiz_stats():
    """Get quiz statistics"""
    data = load_progress()
    
    total = data['quiz'].get('questions_solved', 0)
    correct = data['quiz'].get('questions_correct', 0)
    accuracy = (correct / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'correct': correct,
        'wrong': data['quiz'].get('questions_wrong', 0),
        'accuracy': round(accuracy, 1)
    }

# ═══════════════════════════════════════════════════════
# 📝 EXAM TRACKING
# ═══════════════════════════════════════════════════════

def record_exam_result(score, passed):
    """Record exam result"""
    data = load_progress()
    
    data['exams']['mock_exams_taken'] = data['exams'].get('mock_exams_taken', 0) + 1
    
    if passed:
        data['exams']['mock_exams_passed'] = data['exams'].get('mock_exams_passed', 0) + 1
        data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 200
    else:
        data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 50
    
    # Update best score
    if score > data['exams'].get('best_score', 0):
        data['exams']['best_score'] = score
    
    # Add to history
    exam_entry = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'score': score,
        'passed': passed
    }
    
    if 'exam_history' not in data['exams']:
        data['exams']['exam_history'] = []
    data['exams']['exam_history'].append(exam_entry)
    
    # Calculate average
    if data['exams']['exam_history']:
        scores = [e['score'] for e in data['exams']['exam_history']]
        data['exams']['average_score'] = round(sum(scores) / len(scores), 1)
    
    # Update level
    data['achievements']['level'] = get_level_from_xp(data['achievements']['xp_total'])
    
    save_progress(data)
    return True

# ═══════════════════════════════════════════════════════
# 🎯 DAILY CHALLENGE
# ═══════════════════════════════════════════════════════

def update_daily_challenge(data):
    """Update daily challenge progress"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if data['daily_challenge'].get('date') != today:
        data['daily_challenge'] = {
            'date': today,
            'progress': 0,
            'completed': False
        }
    
    if not data['daily_challenge'].get('completed', False):
        data['daily_challenge']['progress'] = data['daily_challenge'].get('progress', 0) + 1
        
        if data['daily_challenge']['progress'] >= 10:
            data['daily_challenge']['completed'] = True
            data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + 50
    
    return data

# ═══════════════════════════════════════════════════════
# 🏆 ACHIEVEMENTS & BADGES
# ═══════════════════════════════════════════════════════

def check_and_award_badges():
    """Check and award new badges"""
    data = load_progress()
    
    if 'badges' not in data['achievements']:
        data['achievements']['badges'] = []
    
    badges = data['achievements']['badges']
    new_badges = []
    
    # First Steps
    topics = data['modules'].get('completed_topics', [])
    if len(topics) >= 1 and "first_steps" not in badges:
        badges.append("first_steps")
        new_badges.append("🎯 First Steps")
    
    # Knowledge Seeker
    if len(topics) >= 10 and "knowledge_seeker" not in badges:
        badges.append("knowledge_seeker")
        new_badges.append("📚 Knowledge Seeker")
    
    # Quiz Master
    questions = data['quiz'].get('questions_solved', 0)
    if questions >= 100 and "quiz_master" not in badges:
        badges.append("quiz_master")
        new_badges.append("⚡ Quiz Master")
    
    # Exam Ready
    exams_passed = data['exams'].get('mock_exams_passed', 0)
    if exams_passed >= 3 and "exam_ready" not in badges:
        badges.append("exam_ready")
        new_badges.append("📝 Exam Ready")
    
    # Consistent
    streak = data['achievements'].get('study_streak', 0)
    if streak >= 7 and "consistent" not in badges:
        badges.append("consistent")
        new_badges.append("🔥 Consistent")
    
    data['achievements']['badges'] = badges
    save_progress(data)
    return new_badges


def add_xp(amount):
    """Add XP to user"""
    data = load_progress()
    data['achievements']['xp_total'] = data['achievements'].get('xp_total', 0) + amount
    data['achievements']['level'] = get_level_from_xp(data['achievements']['xp_total'])
    save_progress(data)
    return data['achievements']['xp_total']

# ═══════════════════════════════════════════════════════
# 🔖 BOOKMARKS
# ═══════════════════════════════════════════════════════

def toggle_bookmark(topic_name):
    """Toggle bookmark"""
    data = load_progress()
    
    bookmarks = data['modules'].get('bookmarked_topics', [])
    
    if topic_name in bookmarks:
        bookmarks.remove(topic_name)
        data['modules']['bookmarked_topics'] = bookmarks
        save_progress(data)
        return False
    else:
        bookmarks.append(topic_name)
        data['modules']['bookmarked_topics'] = bookmarks
        save_progress(data)
        return True


def get_bookmarks():
    """Get all bookmarks"""
    data = load_progress()
    return data['modules'].get('bookmarked_topics', [])

# ═══════════════════════════════════════════════════════
# 📊 STATISTICS & CALCULATIONS
# ═══════════════════════════════════════════════════════

def get_level_from_xp(xp):
    """Calculate level from XP"""
    return (xp // 500) + 1


def get_user_level(xp):
    """Get user level name"""
    levels = [
        (0, "Beginner"),
        (100, "Learner"),
        (300, "Student"),
        (600, "Practitioner"),
        (1000, "Skilled"),
        (1500, "Advanced"),
        (2200, "Expert"),
        (3000, "Master"),
        (4000, "Elite"),
        (5500, "Legend"),
        (7500, "IWCF Champion")
    ]
    
    for min_xp, level_name in reversed(levels):
        if xp >= min_xp:
            return level_name
    return "Beginner"


def calculate_overall_progress(data):
    """Calculate overall progress percentage"""
    try:
        modules_total = data['modules'].get('total', 8)
        modules_completed = len(data['modules'].get('completed', []))
        modules_pct = (modules_completed / modules_total) * 40 if modules_total > 0 else 0
        
        questions = data['quiz'].get('questions_solved', 0)
        questions_pct = min((questions / 500) * 30, 30)
        
        exams_total = data['exams'].get('total', 10)
        exams_passed = len(data['exams'].get('passed', []))
        exams_pct = (exams_passed / exams_total) * 20 if exams_total > 0 else 0
        
        flashcards = len(data['flashcards'].get('mastered', []))
        flashcards_pct = min((flashcards / 100) * 10, 10)
        
        return round(modules_pct + questions_pct + exams_pct + flashcards_pct, 1)
    except:
        return 0


def calculate_predicted_score(data):
    """Calculate predicted exam score"""
    try:
        questions = data['quiz'].get('questions_solved', 0)
        correct = data['quiz'].get('questions_correct', 0)
        
        if questions == 0:
            return 0
        
        accuracy = (correct / questions) * 100
        
        exam_history = data['exams'].get('exam_history', [])
        if exam_history:
            scores = [e['score'] for e in exam_history]
            exam_avg = sum(scores) / len(scores)
            predicted = (accuracy * 0.6) + (exam_avg * 0.4)
        else:
            predicted = accuracy * 0.8
        
        return round(min(predicted, 100), 1)
    except:
        return 0


def get_overall_stats():
    """Get comprehensive statistics"""
    data = load_progress()
    
    try:
        topics = data['modules'].get('completed_topics', [])
        quiz_stats = get_quiz_stats()
        
        return {
            'overall_progress': calculate_overall_progress(data),
            'modules_completed': len(data['modules'].get('completed', [])),
            'topics_completed': len(topics),
            'questions_solved': quiz_stats['total'],
            'quiz_accuracy': quiz_stats['accuracy'],
            'mock_exams_taken': data['exams'].get('mock_exams_taken', 0),
            'mock_exams_passed': data['exams'].get('mock_exams_passed', 0),
            'best_exam_score': data['exams'].get('best_score', 0),
            'average_exam_score': data['exams'].get('average_score', 0),
            'predicted_score': calculate_predicted_score(data),
            'xp_total': data['achievements'].get('xp_total', 0),
            'level': get_level_from_xp(data['achievements'].get('xp_total', 0)),
            'study_streak': data['achievements'].get('study_streak', 0),
            'badges': data['achievements'].get('badges', []),
            'badges_count': len(data['achievements'].get('badges', []))
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        return {
            'overall_progress': 0, 'modules_completed': 0, 'topics_completed': 0,
            'questions_solved': 0, 'quiz_accuracy': 0, 'mock_exams_taken': 0,
            'mock_exams_passed': 0, 'best_exam_score': 0, 'average_exam_score': 0,
            'predicted_score': 0, 'xp_total': 0, 'level': 1, 'study_streak': 0,
            'badges': [], 'badges_count': 0
        }

# ═══════════════════════════════════════════════════════
# 🔄 SESSION STATE SYNC (SAFE VERSION)
# ═══════════════════════════════════════════════════════

def sync_to_session_state():
    """Sync data to Streamlit session state - SAFE VERSION"""
    import streamlit as st
    
    try:
        data = load_progress()
        stats = get_overall_stats()
        
        # User info
        st.session_state.user_name = data.get('user_info', {}).get('name', 'Engineer')
        st.session_state.user_level = get_user_level(data.get('achievements', {}).get('xp_total', 0))
        st.session_state.study_streak = data.get('achievements', {}).get('study_streak', 0)
        st.session_state.total_xp = data.get('achievements', {}).get('xp_total', 0)
        
        # Progress
        st.session_state.total_progress = stats['overall_progress']
        st.session_state.modules_completed = stats['modules_completed']
        st.session_state.modules_total = data.get('modules', {}).get('total', 8)
        st.session_state.questions_solved = stats['questions_solved']
        st.session_state.questions_correct = data.get('quiz', {}).get('questions_correct', 0)
        st.session_state.exams_passed = stats['mock_exams_passed']
        st.session_state.exams_total = data.get('exams', {}).get('total', 10)
        st.session_state.predicted_score = stats['predicted_score']
        
        # Daily challenge
        today = datetime.now().strftime("%Y-%m-%d")
        daily = data.get('daily_challenge', {})
        if daily.get('date') == today:
            st.session_state.daily_challenge_progress = daily.get('progress', 0)
        else:
            st.session_state.daily_challenge_progress = 0
        
        # Study time
        st.session_state.weekly_hours = data.get('study_time', {}).get('weekly', [0,0,0,0,0,0,0])
        
        # Last study
        last_date = data.get('achievements', {}).get('last_study_date', '')
        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        if last_date == today_str:
            st.session_state.last_study_time = "Today"
        elif last_date == yesterday_str:
            st.session_state.last_study_time = "Yesterday"
        elif last_date:
            st.session_state.last_study_time = last_date
        else:
            st.session_state.last_study_time = "Never"
        
        return data
        
    except Exception as e:
        print(f"Sync Error: {e}")
        raise e

# ═══════════════════════════════════════════════════════
# 🔄 RESET FUNCTIONS
# ═══════════════════════════════════════════════════════

def reset_all_progress():
    """Reset all progress"""
    save_progress(DEFAULT_PROGRESS.copy())
    return True


def reset_quiz_progress():
    """Reset quiz progress only"""
    data = load_progress()
    data['quiz'] = DEFAULT_PROGRESS['quiz'].copy()
    save_progress(data)
    return True


def reset_exam_progress():
    """Reset exam progress only"""
    data = load_progress()
    data['exams'] = DEFAULT_PROGRESS['exams'].copy()
    save_progress(data)
    return True