from copy import deepcopy

# ============================================================
# 기본 설정
# ============================================================

WORK_START = 9
WORK_END = 18

FIXED_BREAKS = {
    "lunch": (12, 13)
}

REST_POOL = ["☕ 커피타임", "🚶 산책", "🧘 스트레칭", "🍪 간식"]

# ============================================================
# Priority
# ============================================================

def calculate_priority(task):

    return (
        (8 - task["deadline"]) * 15 +
        task["importance"] * 12 +
        task["difficulty"] * 8 +
        task["duration"] * 5
    )

# ============================================================
# 스트레스 추정
# ============================================================

def estimate_stress(load, continuous_work, importance):

    stress = 20

    stress += load * 0.8
    stress += continuous_work * 5
    stress += importance * 6

    if stress > 100:
        stress = 100

    return stress

# ============================================================
# 빈 슬롯 찾기 (업그레이드)
# ============================================================

def find_slot(day_schedule, duration):

    day_schedule = sorted(day_schedule, key=lambda x: x["start"])

    current = WORK_START

    for item in day_schedule:

        if item["start"] - current >= duration:
            return current

        current = max(current, item["end"])

    if WORK_END - current >= duration:
        return current

    return None

# ============================================================
# 휴식 자동 삽입
# ============================================================

def insert_rest_blocks(day_schedule, stress):

    if stress < 60:
        return

    rest_time = 1 if stress < 80 else 2

    slot = find_slot(day_schedule, rest_time)

    if slot is None:
        return

    day_schedule.append({
        "time": f"{slot:02d}:00",
        "start": slot,
        "end": slot + rest_time,
        "task": "REST",
        "type": "AUTO"
    })

# ============================================================
# 일정 배치 (핵심)
# ============================================================

def place_task(day_schedule, task):

    priority = calculate_priority(task)

    slot = find_slot(day_schedule, task["duration"])

    if slot is None:
        return None

    stress = estimate_stress(
        priority,
        task["duration"],
        task["importance"]
    )

    day_schedule.append({
        "time": f"{slot:02d}:00",
        "start": slot,
        "end": slot + task["duration"],
        "task": task["name"],
        "type": "AI"
    })

    return {
        "slot": slot,
        "stress": stress
    }

# ============================================================
# 전체 스케줄러 (v2 핵심)
# ============================================================

def optimize_schedule(tasks, base_week):

    week = deepcopy(base_week)

    logs = []

    tasks = sorted(tasks, key=calculate_priority, reverse=True)

    for task in tasks:

        best_day = None
        best_result = None

        for day in week.keys():

            temp = deepcopy(week[day])

            result = place_task(temp, task)

            if result is None:
                continue

            if best_result is None or result["stress"] < best_result["stress"]:
                best_day = day
                best_result = result

        if best_day is None:
            continue

        week[best_day].append({
            "time": f"{best_result['slot']:02d}:00",
            "start": best_result["slot"],
            "end": best_result["slot"] + task["duration"],
            "task": task["name"],
            "type": "AI"
        })

        insert_rest_blocks(week[best_day], best_result["stress"])

        logs.append({
            "task": task["name"],
            "day": best_day,
            "time": f"{best_result['slot']:02d}:00",
            "priority": calculate_priority(task),
            "stress": best_result["stress"]
        })

    return week, logs

# ============================================================
# 비교 함수
# ============================================================

def compare_schedule(before, after):

    result = []

    for day in before.keys():

        b = sorted(before[day], key=lambda x: x["start"])
        a = sorted(after[day], key=lambda x: x["start"])

        result.append({
            "day": day,
            "before": [x["task"] for x in b],
            "after": [x["task"] for x in a]
        })

    return result