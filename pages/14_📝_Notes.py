import streamlit as st
from datetime import datetime
import json

# ═══════════════════════════════════════════════════════
# 🎨 PAGE CONFIG
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Personal Notes - IWCF Mastery",
    page_icon="📝",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
# 🎨 CUSTOM CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .notes-header {
        background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    .note-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #3B82F6;
        transition: all 0.3s ease;
    }
    
    .note-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .note-card.important {
        border-left-color: #EF4444;
        background: linear-gradient(to right, #FEE2E2 0%, white 100%);
    }
    
    .note-card.tip {
        border-left-color: #F59E0B;
        background: linear-gradient(to right, #FEF3C7 0%, white 100%);
    }
    
    .note-card.reminder {
        border-left-color: #7C3AED;
        background: linear-gradient(to right, #EDE9FE 0%, white 100%);
    }
    
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .category-formulas {
        background: #DBEAFE;
        color: #1E40AF;
    }
    
    .category-concepts {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .category-tricks {
        background: #FEF3C7;
        color: #92400E;
    }
    
    .category-questions {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid #3B82F6;
    }
    
    .search-box {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    .folder-card {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid #E5E7EB;
    }
    
    .folder-card:hover {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left-color: #3B82F6;
        transform: translateX(5px);
    }
    
    .note-meta {
        color: #6B7280;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📝 SAMPLE NOTES DATA
# ═══════════════════════════════════════════════════════

SAMPLE_NOTES = [
    {
        "id": 1,
        "title": "Hydrostatic Pressure - Quick Tip",
        "content": "Remember: HP = 0.052 × MW × TVD\n\nQuick mental calculation:\n• For 10 ppg mud: multiply depth by 0.52\n• For 12 ppg mud: multiply depth by 0.624\n\nExample: 10,000 ft with 10 ppg = 10,000 × 0.52 = 5,200 psi",
        "category": "Formulas",
        "type": "tip",
        "created": "2024-01-15",
        "module": "Pressure Fundamentals",
        "tags": ["pressure", "calculations", "formula"]
    },
    {
        "id": 2,
        "title": "Kill Methods - Key Differences",
        "content": "Driller's Method vs Wait & Weight:\n\nDriller's:\n✅ Start immediately (no wait)\n✅ Simpler for beginners\n❌ Takes longer (2 circulations)\n\nWait & Weight:\n✅ Faster (1 circulation)\n✅ Less formation exposure\n❌ Need to wait for KMW preparation\n\nChoose based on: crew experience, KMW availability, formation strength",
        "category": "Concepts",
        "type": "important",
        "created": "2024-01-14",
        "module": "Kill Methods",
        "tags": ["kill methods", "comparison", "procedures"]
    },
    {
        "id": 3,
        "title": "Kick Detection - Don't Forget!",
        "content": "PRIMARY signs (act immediately!):\n1. Pit gain\n2. Flow rate increase\n3. Flow with pumps off\n4. Drilling break\n\nSECONDARY signs:\n• Pump pressure decrease\n• Cut mud\n• Chloride increase\n\nAction: Stop → Pick up → Check flow → Shut in (30 seconds max!)",
        "category": "Concepts",
        "type": "important",
        "created": "2024-01-13",
        "module": "Kick Detection",
        "tags": ["kick", "detection", "safety"]
    },
    {
        "id": 4,
        "title": "Common Exam Mistakes",
        "content": "⚠️ Watch out for:\n\n1. MD vs TVD - Always use TVD!\n2. Forgetting to add OMW in KMW formula\n3. Not adding CLF in subsea calculations\n4. Wrong units (psi vs bar)\n5. Reading 'EXCEPT' or 'NOT' in questions\n\nDouble-check these in every calculation!",
        "category": "Tricks",
        "type": "reminder",
        "created": "2024-01-12",
        "module": "General",
        "tags": ["exam", "mistakes", "tips"]
    },
    {
        "id": 5,
        "title": "Subsea - CLF & Riser Margin",
        "content": "Critical for subsea!\n\nCLF (Choke Line Friction):\n• True SICP = Surface SICP + CLF\n• Always ADD, never subtract\n\nRiser Margin:\n• RM = (MW - 8.6) × 0.052 × WD\n• Minimum: 200 psi\n• Recommended: 400-600 psi\n• Needed for emergency disconnect\n\nThese are heavily tested!",
        "category": "Formulas",
        "type": "important",
        "created": "2024-01-11",
        "module": "Subsea Operations",
        "tags": ["subsea", "CLF", "riser margin"]
    }
]

# ═══════════════════════════════════════════════════════
# 💾 SESSION STATE
# ═══════════════════════════════════════════════════════

if 'notes' not in st.session_state:
    st.session_state.notes = SAMPLE_NOTES.copy()

if 'note_filter' not in st.session_state:
    st.session_state.note_filter = "All"

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

if 'selected_module' not in st.session_state:
    st.session_state.selected_module = "All Modules"

# ═══════════════════════════════════════════════════════
# 🎨 HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="notes-header">
    <h1>📝 Personal Notes</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Your personal study companion - Write, organize, and review
    </p>
    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
        Keep all your IWCF insights in one place
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 📊 STATS
# ═══════════════════════════════════════════════════════

st.markdown("## 📊 Your Notes Overview")

col1, col2, col3, col4 = st.columns(4)

total_notes = len(st.session_state.notes)
formulas_count = sum(1 for n in st.session_state.notes if n['category'] == 'Formulas')
concepts_count = sum(1 for n in st.session_state.notes if n['category'] == 'Concepts')
tricks_count = sum(1 for n in st.session_state.notes if n['category'] == 'Tricks')

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">📝</div>
        <h3 style="color: #3B82F6; margin: 0.5rem 0;">{total_notes}</h3>
        <p style="color: #6B7280;">Total Notes</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">🧮</div>
        <h3 style="color: #1E40AF; margin: 0.5rem 0;">{formulas_count}</h3>
        <p style="color: #6B7280;">Formulas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">💡</div>
        <h3 style="color: #10B981; margin: 0.5rem 0;">{concepts_count}</h3>
        <p style="color: #6B7280;">Concepts</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 2rem;">✨</div>
        <h3 style="color: #F59E0B; margin: 0.5rem 0;">{tricks_count}</h3>
        <p style="color: #6B7280;">Tips & Tricks</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# ➕ CREATE NEW NOTE
# ═══════════════════════════════════════════════════════

st.markdown("## ➕ Create New Note")

with st.expander("✍️ Write a new note", expanded=False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        note_title = st.text_input("📌 Title:", placeholder="e.g., BOP Components - Important Points")
    
    with col2:
        note_category = st.selectbox(
            "📂 Category:",
            ["Formulas", "Concepts", "Tricks", "Questions", "General"]
        )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        note_module = st.selectbox(
            "📚 Module:",
            ["General", "Introduction", "Pressure Fundamentals", "Kick Detection", 
             "Shut-in Procedures", "Kill Methods", "BOP Equipment", 
             "Subsea Operations", "Advanced Topics"]
        )
    
    with col2:
        note_type = st.selectbox(
            "🏷️ Type:",
            ["normal", "important", "tip", "reminder"]
        )
    
    note_content = st.text_area(
        "✍️ Content:",
        placeholder="Write your note here...\n\nYou can use:\n• Bullet points\n• Numbers\n• Line breaks",
        height=200
    )
    
    note_tags = st.text_input(
        "🏷️ Tags (comma separated):",
        placeholder="e.g., pressure, calculations, important"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 Save Note", use_container_width=True, type="primary"):
            if note_title and note_content:
                new_note = {
                    "id": max([n['id'] for n in st.session_state.notes], default=0) + 1,
                    "title": note_title,
                    "content": note_content,
                    "category": note_category,
                    "type": note_type,
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "module": note_module,
                    "tags": [tag.strip() for tag in note_tags.split(",")] if note_tags else []
                }
                st.session_state.notes.insert(0, new_note)
                st.success("✅ Note saved successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Please fill in both title and content!")
    
    with col2:
        if st.button("🗑️ Clear Form", use_container_width=True):
            st.rerun()

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🔍 SEARCH & FILTER
# ═══════════════════════════════════════════════════════

st.markdown("## 🔍 Search & Filter Notes")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_query = st.text_input(
        "🔍 Search:",
        placeholder="Search by title, content, or tags...",
        value=st.session_state.search_query
    )
    st.session_state.search_query = search_query

with col2:
    filter_category = st.selectbox(
        "📂 Category:",
        ["All", "Formulas", "Concepts", "Tricks", "Questions", "General"]
    )

with col3:
    filter_module = st.selectbox(
        "📚 Module:",
        ["All Modules", "General", "Introduction", "Pressure Fundamentals", "Kick Detection", 
         "Shut-in Procedures", "Kill Methods", "BOP Equipment", 
         "Subsea Operations", "Advanced Topics"]
    )

# Sort options
col1, col2 = st.columns([3, 1])

with col1:
    sort_by = st.radio(
        "Sort by:",
        ["Newest First", "Oldest First", "Title A-Z", "Title Z-A"],
        horizontal=True
    )

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📄 DISPLAY NOTES
# ═══════════════════════════════════════════════════════

st.markdown("## 📄 Your Notes")

# Filter notes
filtered_notes = st.session_state.notes.copy()

# Apply search
if search_query:
    filtered_notes = [
        n for n in filtered_notes
        if search_query.lower() in n['title'].lower() 
        or search_query.lower() in n['content'].lower()
        or any(search_query.lower() in tag.lower() for tag in n.get('tags', []))
    ]

# Apply category filter
if filter_category != "All":
    filtered_notes = [n for n in filtered_notes if n['category'] == filter_category]

# Apply module filter
if filter_module != "All Modules":
    filtered_notes = [n for n in filtered_notes if n['module'] == filter_module]

# Apply sorting
if sort_by == "Newest First":
    filtered_notes.sort(key=lambda x: x['created'], reverse=True)
elif sort_by == "Oldest First":
    filtered_notes.sort(key=lambda x: x['created'])
elif sort_by == "Title A-Z":
    filtered_notes.sort(key=lambda x: x['title'])
elif sort_by == "Title Z-A":
    filtered_notes.sort(key=lambda x: x['title'], reverse=True)

# Display count
st.markdown(f"**Showing {len(filtered_notes)} of {total_notes} notes**")

if filtered_notes:
    for note in filtered_notes:
        # Type icons
        type_icon = {
            "important": "🔴",
            "tip": "💡",
            "reminder": "📌",
            "normal": "📝"
        }.get(note['type'], "📝")
        
        note_class = note['type'] if note['type'] != 'normal' else ''
        
        st.markdown(f"""
        <div class="note-card {note_class}">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: #1F2937;">{type_icon} {note['title']}</h3>
                    <div style="margin-top: 0.5rem;">
                        <span class="category-badge category-{note['category'].lower()}">{note['category']}</span>
                        <span style="color: #6B7280; font-size: 0.85rem; margin-left: 0.5rem;">
                            📚 {note['module']}
                        </span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="color: #6B7280; font-size: 0.85rem;">📅 {note['created']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Content
        st.markdown(f"**Content:**")
        st.text(note['content'])
        
        # Tags
        if note.get('tags'):
            tags_html = " ".join([f"<span style='background: #F3F4F6; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.8rem; margin-right: 0.3rem;'>🏷️ {tag}</span>" for tag in note['tags']])
            st.markdown(tags_html, unsafe_allow_html=True)
        
        # Actions
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("📝 Edit", key=f"edit_{note['id']}", use_container_width=True):
                st.info("Edit functionality coming soon!")
        
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{note['id']}", use_container_width=True):
                st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note['id']]
                st.success("Note deleted!")
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("📭 No notes found. Try adjusting your filters or create a new note!")

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 📂 ORGANIZE BY MODULE
# ═══════════════════════════════════════════════════════

st.markdown("## 📂 Browse by Module")

modules = {}
for note in st.session_state.notes:
    module = note['module']
    if module not in modules:
        modules[module] = []
    modules[module].append(note)

cols = st.columns(3)

for idx, (module, notes) in enumerate(sorted(modules.items())):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="folder-card">
            <div style="font-size: 1.5rem;">📁</div>
            <h4 style="margin: 0.5rem 0 0 0; color: #1F2937;">{module}</h4>
            <p style="color: #6B7280; margin: 0.3rem 0 0 0; font-size: 0.9rem;">
                {len(notes)} note{'s' if len(notes) != 1 else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View {module} notes", key=f"module_{idx}", use_container_width=True):
            st.session_state.selected_module = module
            st.rerun()

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 💡 TIPS
# ═══════════════════════════════════════════════════════

st.markdown("## 💡 Note-Taking Tips")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **✍️ Effective Note-Taking:**
    
    ✅ Use clear, descriptive titles
    ✅ Break down complex topics
    ✅ Add examples to formulas
    ✅ Use bullet points for clarity
    ✅ Tag for easy searching
    ✅ Mark important points
    
    **📝 What to Note:**
    - Formulas with examples
    - Common mistakes
    - Exam tips
    - Tricky concepts
    - Personal insights
    """)

with col2:
    st.markdown("""
    **🎯 Organization Tips:**
    
    ✅ One topic per note
    ✅ Use categories consistently
    ✅ Review notes weekly
    ✅ Update as you learn
    ✅ Link related notes
    
    **⚡ Quick Access:**
    - Use search for instant find
    - Filter by module/category
    - Sort by date or title
    - Export important notes
    """)

st.markdown("---")

# ═══════════════════════════════════════════════════════
# 🚀 QUICK ACTIONS
# ═══════════════════════════════════════════════════════

st.markdown("## 🚀 Continue Learning")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Study Modules", use_container_width=True):
        st.switch_page("pages/01_📚_Learn.py")

with col2:
    if st.button("🎴 Flashcards", use_container_width=True):
        st.switch_page("pages/08_🎴_Flashcards.py")

with col3:
    if st.button("📄 Cheat Sheets", use_container_width=True):
        st.switch_page("pages/12_📄_Cheat_Sheets.py")

with col4:
    if st.button("🤖 AI Tutor", use_container_width=True):
        st.switch_page("pages/07_🎯_AI_Tutor.py")

# ═══════════════════════════════════════════════════════
# 📌 FOOTER
# ═══════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1.5rem;">
    <p style="margin: 0;">
        📝 <strong>Elshamy IWCF Mastery Method™ - Personal Notes</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        "The palest ink is better than the best memory" - Write it down! ✍️
    </p>
</div>
""", unsafe_allow_html=True)