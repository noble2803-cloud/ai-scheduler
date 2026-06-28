import os
import google.generativeai as genai
import streamlit as st
# ============================================================
# Gemini 초기화
# ============================================================

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = os.getenv("GEMINI_API_KEY")

model = None

if API_KEY:

    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")


# ============================================================
# 단일 task 설명 생성
# ============================================================

def explain_task(task, schedule_result):

    if model is None:

        return fallback_explain(task)

    prompt = f"""
너는 일정 최적화 AI야.

아래 작업을 왜 이 시간에 배치했는지 설명해.

TASK:
{task}

SCHEDULE RESULT:
{schedule_result}

조건:
- 3~5줄 이내
- 너무 길게 설명하지 말 것
- 발표용으로 자연스럽게
- 스트레스/우선순위 고려 포함
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except:

        return fallback_explain(task)


# ============================================================
# 전체 스케줄 설명 생성
# ============================================================

def explain_schedule(tasks, logs):

    if model is None:

        return fallback_schedule_explain(tasks)

    prompt = f"""
너는 AI 스케줄러 발표용 설명을 만드는 AI야.

아래 데이터를 기반으로 발표 스크립트를 만들어.

TASKS:
{tasks}

LOGS:
{logs}

조건:
- 한국어
- 10줄 이내
- 발표용 자연스러운 말투
- "왜 이렇게 배치했는지"
- 스트레스 감소 전략 포함
- 우선순위 기반 설명
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except:

        return fallback_schedule_explain(tasks)


# ============================================================
# fallback (API 없을 때)
# ============================================================

def fallback_explain(task):

    return (
        f"{task['name']}은(는) "
        f"마감({task['deadline']}일), "
        f"중요도({task['importance']})를 고려하여 "
        f"우선 배치되었습니다."
    )


def fallback_schedule_explain(tasks):

    return "AI가 우선순위와 스트레스를 고려하여 최적의 일정으로 재배치했습니다."


# ============================================================
# 발표용 한줄 요약 생성
# ============================================================

def one_line_summary(stress_score, efficiency_gain):

    if stress_score > 80:

        return "현재 일정은 과부하 상태로 즉시 조정이 필요합니다."

    elif stress_score > 50:

        return "일정이 다소 빡빡하지만 관리 가능한 수준입니다."

    return "현재 일정은 안정적으로 최적화되어 있습니다."
