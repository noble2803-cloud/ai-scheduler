from stress import task_stress, analyze_schedule
from scheduler import calculate_priority

def autonomous_decision(task):

    if task["difficulty"] >= 4 and task["deadline"] > 3:
        return "DEFER"

    if task["importance"] >= 5:
        return "PRIORITY"

    return "NORMAL"

# ============================================================
# AI 종합 판단 엔진
# ============================================================

def decision_score(task):

    priority = calculate_priority(task)

    stress = task_stress(
        priority,
        task["duration"],
        task["importance"]
    )

    score = (
        priority * 0.6 +
        (100 - stress) * 0.4
    )

    return score


# ============================================================
# 작업 위험도 판단
# ============================================================

def risk_level(score):

    if score >= 120:
        return "🟢 최우선 (즉시 실행)"

    elif score >= 90:
        return "🟡 중요"

    elif score >= 60:
        return "🟠 보통"

    return "🔴 낮음"


# ============================================================
# AI 판단 이유 생성
# ============================================================

def explain_decision(task):

    reasons = []

    if task["deadline"] <= 2:
        reasons.append("마감이 매우 임박")

    if task["importance"] >= 4:
        reasons.append("중요도가 높음")

    if task["difficulty"] >= 4:
        reasons.append("난이도 높음")

    if task["duration"] >= 4:
        reasons.append("장시간 작업")

    if not reasons:
        reasons.append("일반 작업")

    return ", ".join(reasons)


# ============================================================
# 전체 task 분석
# ============================================================

def analyze_tasks(tasks):

    result = []

    for task in tasks:

        score = decision_score(task)

        result.append({

            "name": task["name"],

            "priority": calculate_priority(task),

            "decision_score": round(score, 2),

            "risk": risk_level(score),

            "reason": explain_decision(task),

            "duration": task["duration"]

        })

    return sorted(result, key=lambda x: x["decision_score"], reverse=True)


# ============================================================
# 스케줄 전체 평가
# ============================================================

def evaluate_week(week_schedule):

    from stress import analyze_schedule

    result = {}

    for day, schedule in week_schedule.items():

        result[day] = analyze_schedule(schedule)

    return result


# ============================================================
# AI 최종 결론
# ============================================================

def final_ai_summary(tasks, week_schedule):

    analyzed = analyze_tasks(tasks)

    stress_summary = evaluate_week(week_schedule)

    avg_stress = sum(
        v["score"] for v in stress_summary.values()
    ) / len(stress_summary)

    return {

        "task_analysis": analyzed,

        "weekly_stress": stress_summary,

        "average_stress": round(avg_stress, 2),

        "global_status":
            "🔥 과부하" if avg_stress > 75 else
            "⚠️ 주의" if avg_stress > 50 else
            "🟢 안정"
    }
