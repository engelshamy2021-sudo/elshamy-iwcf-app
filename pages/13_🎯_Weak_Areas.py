import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Weak Areas Analysis - IWCF Mastery",
    page_icon="🎯",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .weak-header {
        background: linear-gradient(135deg, #DC2626 0%, #F87171 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
    }
    
    .analysis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .weak-topic {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #EF4444;
        margin: 1rem 0;
    }
    
    .average-topic {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .strong-topic {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .progress-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .progress-bar-mini {
        flex: 1;
        background: #E5E7EB;
        height: 10px;
        border-radius: 5px;
        overflow: hidden;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 PERFORMANCE DATA (Demo)
# ═══════════════════════════════════════════════════════

TOPICS_PERFORMANCE = {
    "Hydrostatic Pressure": {
        "questions_attempted": 25,
        "correct": 22,
        "accuracy": 88,
        "time_spent": 45,
        "difficulty": "Easy",
        "last_attempt": "2 days ago"
    },
    "Kill Mud Weight Calculation": {
        "questions_attempted": 30,
        "correct": 18,
        "accuracy": 60,
        "time_spent": 75,
        "difficulty": "Medium",
        "last_attempt": "1 day ago"
    },
    "Kick Detection Signs": {
        "questions_attempted": 20,
        "correct": 19,
        "accuracy": 95,
        "time_spent": 30,
        "difficulty": "Easy",
        "last_attempt": "3 days ago"
    },
    "Driller's Method": {
        "questions_attempted": 15,
        "correct": 9,
        "accuracy": 60,
        "time_spent": 50,
        "difficulty": "Hard",
        "last_attempt": "Today"
    },
    "Wait & Weight Method": {
        "questions_attempted": 12,
        "correct": 6,
        "accuracy": 50,
        "time_spent": 45,
        "difficulty": "Hard",
        "last_attempt": "1 day ago"
    },
    "BOP Components": {
        "questions_attempted": 18,
        "correct": 15,
        "accuracy": 83,
        "time_spent": 35,
        "difficulty": "Medium",
        "last_attempt": "2 days ago"
    },
    "Shut-in Procedures": {
        "questions_attempted": 22,
        "correct": 20,
        "accuracy": 91,
        "time_spent": 40,
        "difficulty": "Easy",
        "last_attempt": "1 day ago"
    },
    "ICP & FCP Calculations": {
        "questions_attempted": 28,
        "correct": 17,
        "accuracy": 61,
        "time_spent": 70,
        "difficulty": "Medium",
        "last_attempt": "Today"
    },
    "Subsea Operations": {
        "questions_attempted": 10,
        "correct": 4,
        "accuracy": 40,
        "time_spent": 35,
        "difficulty": "Hard",
        "last_attempt": "3 days ago"
    },
    "Riser Margin": {
        "questions_attempted": 8,
        "correct": 3,
        "accuracy": 38,
        "time_spent": 25,
        "difficulty": "Hard",
        "last_attempt": "4 days ago"
    },
    "MAASP": {
        "questions_attempted": 14,
        "correct": 7,
        "accuracy": 50,
        "time_spent": 45,
        "difficulty": "Hard",
        "last_attempt": "2 days ago"
    },
    "Formation Pressure": {
        "questions_attempted": 16,
        "correct": 14,
        "accuracy": 88,
        "time_spent": 30,
        "difficulty": "Easy",
        "last_attempt": "1 day ago"
    }
}

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'performance_data' not in st.session_state:
    st.session_state.performance_data = TOPICS_PERFORMANCE

# ═══════════════════════════════════════════════════════
# 🔧 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def categorize_performance(accuracy):
    """Categorize topic based on accuracy"""
    if accuracy >= 80:
        return "Strong", "🟢"
    elif accuracy >= 60:
        return "Average", "🟡"
    else:
        return "Weak", "🔴"

def get_recommendations(topic, data):
    """Generate personalized recommendations"""
    accuracy = data['accuracy']
    
    if accuracy < 60:
        return [
            f"📚 Review {topic} in Learn module",
            f"🎴 Practice {topic} flashcards daily",
            f"🧮 Use calculator for {topic} problems",
            f"🤖 Ask AI Tutor to explain {topic}",
            f"❓ Solve 10 more questions on {topic}"
        ]
    elif accuracy < 80:
        return [
            f"✅ Good progress on {topic}!",
            f"🎯 Practice 5 more questions to solidify",
            f"📝 Try {topic} in mock exams",
            f"🎴 Quick flashcard review recommended"
        ]
    else:
        return [
            f"🌟 Excellent mastery of {topic}!",
            f"✅ Maintain with weekly review",
            f"🎓 You're ready for exam questions on this topic"
        ]

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="weak-header">
    <h1>🎯 Weak Areas Analysis</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        AI-powered performance analysis & personalized recommendations
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Identify gaps, focus your study, maximize your score
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 OVERALL PERFORMANCE
# ═══════════════════════════════════════════════════════

st.markdown("## 📊 Overall Performance Summary")

# Calculate totals
total_questions = sum(d['questions_attempted'] for d in TOPICS_PERFORMANCE.values())
total_correct = sum(d['correct'] for d in TOPICS_PERFORMANCE.values())
overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

weak_count = sum(1 for d in TOPICS_PERFORMANCE.values() if d['accuracy'] < 60)
average_count = sum(1 for d in TOPICS_PERFORMANCE.values() if 60 <= d['accuracy'] < 80)
strong_count = sum(1 for d in TOPICS_PERFORMANCE.values() if d['accuracy'] >= 80)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #3B82F6;">
        <div style="font-size: 2rem;">📝</div>
        <h3 style="color: #3B82F6; margin: 0.5rem 0;">{total_questions}</h3>
        <p style="color: #6B7280;">Total Questions</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #10B981;">
        <div style="font-size: 2rem;">🎯</div>
        <h3 style="color: #10B981; margin: 0.5rem 0;">{overall_accuracy:.0f}%</h3>
        <p style="color: #6B7280;">Overall Accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #EF4444;">
        <div style="font-size: 2rem;">🔴</div>
        <h3 style="color: #EF4444; margin: 0.5rem 0;">{weak_count}</h3>
        <p style="color: #6B7280;">Weak Topics</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card" style="border-top: 4px solid #10B981;">
        <div style="font-size: 2rem;">🟢</div>
        <h3 style="color: #10B981; margin: 0.5rem 0;">{strong_count}</h3>
        <p style="color: #6B7280;">Strong Topics</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📈 PERFORMANCE CHART
# ═══════════════════════════════════════════════════════

st.markdown("## 📈 Performance by Topic")

# Create dataframe for chart
df = pd.DataFrame([
    {
        'Topic': topic,
        'Accuracy': data['accuracy'],
        'Questions': data['questions_attempted'],
        'Category': categorize_performance(data['accuracy'])[0]
    }
    for topic, data in TOPICS_PERFORMANCE.items()
])

# Sort by accuracy
df = df.sort_values('Accuracy')

# Color mapping
color_map = {
    'Weak': '#EF4444',
    'Average': '#F59E0B',
    'Strong': '#10B981'
}

# Create bar chart
fig = px.bar(
    df,
    x='Accuracy',
    y='Topic',
    orientation='h',
    color='Category',
    color_discrete_map=color_map,
    text='Accuracy',
    title='Accuracy by Topic'
)

fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
fig.update_layout(
    xaxis_title="Accuracy (%)",
    yaxis_title="",
    height=600,
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

fig.add_vline(x=60, line_dash="dash", line_color="red", annotation_text="Minimum Pass")
fig.add_vline(x=80, line_dash="dash", line_color="green", annotation_text="Target")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🔴 WEAK AREAS (Priority)
# ═══════════════════════════════════════════════════════

st.markdown("## 🔴 Priority Areas (Need Immediate Attention)")

weak_topics = {k: v for k, v in TOPICS_PERFORMANCE.items() if v['accuracy'] < 60}

if weak_topics:
    for topic, data in sorted(weak_topics.items(), key=lambda x: x[1]['accuracy']):
        st.markdown(f"""
        <div class="weak-topic">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: #991B1B;">🔴 {topic}</h3>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                        <span>Accuracy: <strong>{data['accuracy']}%</strong></span>
                        <span>•</span>
                        <span>Questions: {data['correct']}/{data['questions_attempted']}</span>
                        <span>•</span>
                        <span>Difficulty: {data['difficulty']}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2rem; color: #EF4444;">{data['accuracy']}%</div>
                    <div style="font-size: 0.8rem; color: #6B7280;">Last: {data['last_attempt']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show progress bar
        st.markdown(f"""
        <div style="background: #FEE2E2; height: 8px; border-radius: 4px; margin: 0.5rem 0;">
            <div style="background: #EF4444; height: 100%; width: {data['accuracy']}%; border-radius: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown(f"""
        <div class="recommendation-box">
            <strong>📋 Action Plan for {topic}:</strong>
        </div>
        """, unsafe_allow_html=True)
        
        recommendations = get_recommendations(topic, data)
        for rec in recommendations:
            st.write(f"  {rec}")
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📚 Learn {topic[:15]}...", key=f"learn_{topic}", use_container_width=True):
                st.switch_page("pages/01_📚_Learn.py")
        with col2:
            if st.button(f"❓ Practice Quiz", key=f"quiz_{topic}", use_container_width=True):
                st.switch_page("pages/02_❓_Quiz.py")
        with col3:
            if st.button(f"🤖 Ask AI", key=f"ai_{topic}", use_container_width=True):
                st.switch_page("pages/07_🎯_AI_Tutor.py")
        
        st.markdown("<br>", unsafe_allow_html=True)
else:
    st.success("🎉 No weak areas! Great job!")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🟡 AVERAGE AREAS (Needs Improvement)
# ═══════════════════════════════════════════════════════

st.markdown("## 🟡 Areas for Improvement")

average_topics = {k: v for k, v in TOPICS_PERFORMANCE.items() if 60 <= v['accuracy'] < 80}

if average_topics:
    for topic, data in sorted(average_topics.items(), key=lambda x: x[1]['accuracy']):
        st.markdown(f"""
        <div class="average-topic">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #92400E;">🟡 {topic}</h4>
                    <span style="color: #78350F;">
                        {data['accuracy']}% accuracy • {data['correct']}/{data['questions_attempted']} correct
                    </span>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5rem; color: #F59E0B;">{data['accuracy']}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.markdown(f"""
        <div style="background: #FEF3C7; height: 6px; border-radius: 3px; margin: 0.5rem 0;">
            <div style="background: #F59E0B; height: 100%; width: {data['accuracy']}%; border-radius: 3px;"></div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No topics in this category.")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🟢 STRONG AREAS (Keep Up!)
# ═══════════════════════════════════════════════════════

st.markdown("## 🟢 Your Strong Areas")

strong_topics = {k: v for k, v in TOPICS_PERFORMANCE.items() if v['accuracy'] >= 80}

if strong_topics:
    cols = st.columns(3)
    for idx, (topic, data) in enumerate(sorted(strong_topics.items(), key=lambda x: x[1]['accuracy'], reverse=True)):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="strong-topic">
                <h4 style="margin: 0; color: #065F46;">🟢 {topic}</h4>
                <div style="font-size: 1.8rem; font-weight: bold; color: #10B981; margin: 0.5rem 0;">
                    {data['accuracy']}%
                </div>
                <p style="color: #047857; margin: 0; font-size: 0.9rem;">
                    {data['correct']}/{data['questions_attempted']} correct
                </p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Keep studying to build your strong areas!")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 💡 AI INSIGHTS
# ═══════════════════════════════════════════════════════

st.markdown("## 💡 AI-Powered Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="insight-card">
        <h3 style="margin: 0;">🎯 Study Plan Recommendation</h3>
        <p style="margin: 1rem 0 0 0; opacity: 0.9;">
            Based on your performance, focus on:
        </p>
        <ul style="margin: 0.5rem 0;">
            <li>Subsea Operations (40% - Critical!)</li>
            <li>Riser Margin (38% - Critical!)</li>
            <li>Wait & Weight Method (50%)</li>
        </ul>
        <p style="margin: 1rem 0 0 0;">
            📅 Recommended: 2 hours/day on these topics
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-card">
        <h3 style="margin: 0;">📈 Progress Trend</h3>
        <p style="margin: 1rem 0 0 0; opacity: 0.9;">
            Your overall accuracy is improving!
        </p>
        <ul style="margin: 0.5rem 0;">
            <li>Last week: 62% average</li>
            <li>This week: 68% average</li>
            <li>Improvement: +6% 🎉</li>
        </ul>
        <p style="margin: 1rem 0 0 0;">
            🎓 At this rate, you'll be exam-ready in 2 weeks!
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🎓 EXAM READINESS
# ═══════════════════════════════════════════════════════

st.markdown("## 🎓 Exam Readiness Assessment")

# Calculate readiness score
readiness_score = overall_accuracy
readiness_color = "#10B981" if readiness_score >= 80 else "#F59E0B" if readiness_score >= 70 else "#EF4444"

st.markdown(f"""
<div style="background: linear-gradient(135deg, {readiness_color} 0%, {readiness_color}90 100%); 
            padding: 2rem; border-radius: 15px; color: white; text-align: center;">
    <h2 style="margin: 0;">Current Readiness Score</h2>
    <div style="font-size: 4rem; font-weight: bold; margin: 1rem 0;">{readiness_score:.0f}%</div>
    <p style="font-size: 1.2rem; margin: 0;">
        {'🎉 Excellent! You are ready!' if readiness_score >= 80 else '⚡ Good progress! Keep going!' if readiness_score >= 70 else '📚 More study needed'}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Readiness breakdown
col1, col2, col3 = st.columns(3)

with col1:
    topics_ready = sum(1 for d in TOPICS_PERFORMANCE.values() if d['accuracy'] >= 80)
    total_topics = len(TOPICS_PERFORMANCE)
    st.metric("Topics Mastered", f"{topics_ready}/{total_topics}", f"{(topics_ready/total_topics*100):.0f}%")

with col2:
    questions_ready = sum(1 for d in TOPICS_PERFORMANCE.values() if d['accuracy'] >= 70)
    st.metric("Topics Exam-Ready", f"{questions_ready}/{total_topics}", f"{(questions_ready/total_topics*100):.0f}%")

with col3:
    predicted_score = overall_accuracy
    st.metric("Predicted Exam Score", f"{predicted_score:.0f}%", 
              "Pass" if predicted_score >= 70 else "Need More Study")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🚀 QUICK ACTIONS
# ═══════════════════════════════════════════════════════

st.markdown("## 🚀 Take Action Now")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Study Weak Topics", use_container_width=True, type="primary"):
        st.switch_page("pages/01_📚_Learn.py")

with col2:
    if st.button("❓ Practice Quiz", use_container_width=True):
        st.switch_page("pages/02_❓_Quiz.py")

with col3:
    if st.button("📝 Mock Exam", use_container_width=True):
        st.switch_page("pages/03_📝_Mock_Exam.py")

with col4:
    if st.button("🤖 Ask AI Tutor", use_container_width=True):
        st.switch_page("pages/07_🎯_AI_Tutor.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        🎯 <strong>Elshamy IWCF Mastery Method™ - Weak Areas Analysis</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "Knowing yourself is the beginning of all wisdom" - Focus on growth! 📈
    </p>
</div>
""", unsafe_allow_html=True)