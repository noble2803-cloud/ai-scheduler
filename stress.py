# ============================================================
# 기본 스트레스 계산 모듈 (v2)
# scheduler.py v2 기준 연동
# ============================================================

# ============================================================
# 단일 작업 스트레스
# ============================================================

def task_stress(priority, duration, importance):

    stress = 15

    stress += priority * 0.2
    stress += duration * 6
    stress += importance * 8

    if stress > 100:
        stress = 100

    return stress


# ============================================================
# 하루 전체 스트레스
# ============================================================

def daily_stress(schedule):

    total = 0
    count = 0

    for item in schedule:

        if item["task"] in ["lunch", "REST"]:
            continue

        priority = 50  # fallback
        duration = item["end"] - item["start"]
        importance = 3

        stress = task_stress(priority, duration, importance)

        total += stress
        count += 1

    if count == 0:
        return 10

    avg = total / count

    return min(100, avg)


# ============================================================
# 스트레스 상태 분류
# ============================================================

def stress_level(score):

    if score >= 80:
        return "🔥 매우 높음"

    elif score >= 60:
        return "⚠️ 높음"

    elif score >= 40:
        return "🙂 보통"

    return "😌 낮음"


# ============================================================
# 스트레스 기반 행동 추천
# ============================================================

def stress_recommendation(score):

    if score >= 80:

        return [
            "5분 즉시 휴식",
            "산책 추천 🚶",
            "커피 타임 ☕",
            "업무 재조정 필요"
        ]

    elif score >= 60:

        return [
            "스트레칭 🧘",
            "짧은 휴식",
            "물 마시기",
            "업무 속도 조절"
        ]

    elif score >= 40:

        return [
            "가벼운 휴식",
            "리듬 유지",
            "무리 금지"
        ]

    return [
        "현재 매우 안정적",
        "여유롭게 진행 가능",
        "짧은 휴식 OK"
    ]


# ============================================================
# 스트레스 분석 요약
# ============================================================

def analyze_schedule(schedule):

    score = daily_stress(schedule)

    return {
        "score": round(score, 2),
        "level": stress_level(score),
        "recommendation": stress_recommendation(score)
    }