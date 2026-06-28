import streamlit as st

from random_schedule import generate_week, inject_random_events, highlight_busy_days
from scheduler import optimize_schedule
from stress import analyze_schedule
from decision_engine import final_ai_summary
from gemini_ai import explain_schedule, one_line_summary

# ============================================================
# UI 설정
# ============================================================

st.set_page_config(
    page_title="AI Scheduler",
    layout="wide"
)

st.title("🧠 AI Smart Scheduler (v2)")

# ============================================================
# Session State
# ============================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "result" not in st.session_state:
    st.session_state.result = None

# ============================================================
# 사이드바 - Task 입력
# ============================================================

st.sidebar.header("📌 Task 입력")

name = st.sidebar.text_input("Task 이름")

deadline = st.sidebar.slider("마감 (D-day)", 1, 7, 3)

duration = st.sidebar.slider("소요 시간", 1, 4, 2)

importance = st.sidebar.slider("중요도", 1, 5, 3)

difficulty = st.sidebar.slider("난이도", 1, 5, 3)

if st.sidebar.button("추가"):

    if name:

        st.session_state.tasks.append({

            "name": name,
            "deadline": deadline,
            "duration": duration,
            "importance": importance,
            "difficulty": difficulty

        })

# ============================================================
# Task 리스트
# ============================================================

st.subheader("📋 현재 Task")

for i, t in enumerate(st.session_state.tasks):

    col1, col2 = st.columns([4,1])

    with col1:
        st.write(t)

    with col2:

        if st.button("삭제", key=i):

            st.session_state.tasks.pop(i)

            st.rerun()

# ============================================================
# 실행 버튼
# ============================================================

if st.button("🚀 AI 스케줄 생성"):

    base_week = generate_week()

    for d in base_week:

        base_week[d] = inject_random_events(base_week[d])

    optimized_week, logs, thinking = optimize_schedule(
        st.session_state.tasks,
        base_week
    )

    analysis = final_ai_summary(
        st.session_state.tasks,
        optimized_week
    )

    stress_summary = {
        d: analyze_schedule(v)
        for d, v in optimized_week.items()
    }

    explanation = explain_schedule(
        st.session_state.tasks,
        logs
    )

    st.session_state.result = {

        "week": optimized_week,
        "logs": logs,
        "thinking": thinking,
        "analysis": analysis,
        "stress": stress_summary,
        "explanation": explanation

    }

# ============================================================
# 결과 출력
# ============================================================

if st.session_state.result:

    res = st.session_state.result

    st.divider()

    st.subheader("📊 AI 분석 결과")

    st.write(res["analysis"]["global_status"])

    st.write("평균 스트레스:", res["analysis"]["average_stress"])

    st.divider()

    st.subheader("🧠 AI 설명")

    st.write(res["explanation"])

    st.divider()

    st.subheader("📅 주간 스케줄")

    st.json(res["week"])

    st.divider()

    st.subheader("🔥 스트레스 분석")

    st.json(res["stress"])

    st.divider()

    st.subheader("📌 AI Thinking")

    st.json(res["thinking"])