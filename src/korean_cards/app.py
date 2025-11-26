import streamlit as st
from crew import KoreanTutorCrew

st.set_page_config(page_title="Korean Dojo Agent", layout="wide")

# Initialize State
if 'tutor' not in st.session_state:
    st.session_state.tutor = KoreanTutorCrew()
if 'lesson_plan' not in st.session_state:
    st.session_state.lesson_plan = None
if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = {} # Store feedback per scenario ID

# --- Sidebar: Input ---
with st.sidebar:
    st.title("🇰🇷 AI Tutor")
    korean_input = st.text_area("Enter Korean Text", height=150)
    
    if st.button("Generate Lesson"):
        if korean_input:
            with st.spinner("Agents are analyzing & designing scenarios..."):
                # Unified Call
                result = st.session_state.tutor.run_tutor(korean_input)
                st.session_state.lesson_plan = result.pydantic
        else:
            st.warning("Please enter text first.")

# --- Main Page ---
if st.session_state.lesson_plan:
    lesson = st.session_state.lesson_plan
    
    # PART A: Reference Deck (Syllabus)
    st.subheader("📚 Vocabulary Breakdown")
    cols = st.columns(3)
    for idx, item in enumerate(lesson.syllabus.items):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"#### {item.korean_phrase}")
                st.caption(f"{', '.join(item.components)}")
                st.write(f"**Meaning:** {item.literal_meaning}")
                with st.expander("Context Note"):
                    st.info(item.contextual_note)

    st.divider()

    # PART B: The Dojo (Scenarios)
    st.subheader("⚔️ Practice Scenarios")
    
    scenarios = lesson.practice_scenarios.scenarios
    tabs = st.tabs([f"{s.id}: {s.title}" for s in scenarios])

    for i, tab in enumerate(tabs):
        with tab:
            scen = scenarios[i]
            # Scenario Card - NOW WITH FORCED DARK TEXT COLOR
            st.markdown(f"""
            <div style="background-color:#f0f2f6; color:#31333F; padding:20px; border-radius:10px; margin-bottom:20px; border-left: 5px solid #ff4b4b;">
                <p style="margin-bottom: 5px;"><strong>🎭 Role:</strong> {scen.user_role} &nbsp;|&nbsp; <strong>🗣️ Tone:</strong> {scen.required_tone}</p>
                <p style="font-size:18px; line-height: 1.5; font-weight: 500; margin: 15px 0;"><em>"{scen.scenario_description}"</em></p>
                <p style="font-size:14px; color:#555;"><strong>🎯 Targets:</strong> {', '.join(scen.target_items)}</p>
            </div>
            """, unsafe_allow_html=True)

            # Input & Feedback
            user_key = f"user_in_{scen.id}"
            user_ans = st.text_input("Your Answer:", key=user_key)
            
            if st.button("Submit & Evaluate", key=f"btn_{scen.id}"):
                with st.spinner("Evaluator is grading..."):
                    # Call Evaluation Crew
                    eval_res = st.session_state.tutor.run_evaluation(scen, user_ans)
                    st.session_state.feedback_history[scen.id] = eval_res.pydantic

            # Show Result if it exists for this scenario
            if scen.id in st.session_state.feedback_history:
                res = st.session_state.feedback_history[scen.id]
                
                if res.is_correct:
                    st.success(f"✅ PASSED! Score: {res.score}/10")
                else:
                    st.error(f"❌ REVISE. Score: {res.score}/10")
                
                st.write(f"**Coach:** {res.feedback_text}")
                st.info(f"**Native Speaker would say:** {res.better_alternative}")

else:
    st.info("👈 Paste a Korean paragraph in the sidebar to start your session.")