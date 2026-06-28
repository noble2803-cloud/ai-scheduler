import random

# ============================================================
# 기본 고정 일정 (데모용)
# ============================================================

FIXED_MORNING = [
    "메일 확인",
    "팀 스탠드업",
    "업무 계획",
    "커피 한잔"
]

FIXED_BREAK = [
    "커피타임",
    "스트레칭",
    "짧은 산책",
    "간식"
]

FIXED_WORK = [
    "보고서 작성",
    "Spotfire 분석",
    "데이터 검토",
    "회의",
    "코드 리뷰",
    "문서 작업",
    "프로젝트 진행"
]

FIXED_EVENING = [
    "운동",
    "독서",
    "영화",
    "휴식",
    "친구 만나기"
]

# ============================================================
# 하루 기본 구조 생성
# ============================================================

def generate_day_structure():

    schedule = []

    # 오전 시작
    schedule.append({
        "time": "09:00",
        "start": 9,
        "end": 10,
        "task": random.choice(FIXED_MORNING),
        "type": "BASE"
    })

    current = 10

    # 업무 블록 생성
    while current < 18:

        # 점심
        if current == 12:

            schedule.append({
                "time": "12:00",
                "start": 12,
                "end": 13,
                "task": "점심",
                "type": "FIXED"
            })

            current = 13
            continue

        # 랜덤 작업 또는 휴식
        if random.random() < 0.2:
            task = random.choice(FIXED_BREAK)
            duration = 1
        else:
            task = random.choice(FIXED_WORK)
            duration = random.choice([1, 2])

        schedule.append({
            "time": f"{current:02d}:00",
            "start": current,
            "end": current + duration,
            "task": task,
            "type": "BASE"
        })

        current += duration

    # 퇴근 후
    schedule.append({
        "time": "19:00",
        "start": 19,
        "end": 20,
        "task": random.choice(FIXED_EVENING),
        "type": "BASE"
    })

    return schedule


# ============================================================
# 주간 스케줄 생성
# ============================================================

def generate_week():

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    week = {}

    for d in days:

        week[d] = generate_day_structure()

    return week


# ============================================================
# 데모용 랜덤 이벤트 삽입
# ============================================================

def inject_random_events(schedule, intensity=0.3):

    events = [
        "긴급 회의",
        "추가 업무 요청",
        "자료 수정",
        "클라이언트 응답",
        "이슈 대응"
    ]

    if random.random() < intensity:

        schedule.append({
            "time": "14:00",
            "start": 14,
            "end": 15,
            "task": random.choice(events),
            "type": "EVENT"
        })

    return schedule


# ============================================================
# 발표용 강조 포인트
# ============================================================

def highlight_busy_days(week):

    result = {}

    for day, schedule in week.items():

        work_count = len([
            x for x in schedule
            if x["type"] in ["BASE", "EVENT"]
        ])

        result[day] = {
            "tasks": work_count,
            "status":
                "🔥 매우 바쁨" if work_count > 10 else
                "⚠️ 보통" if work_count > 7 else
                "🟢 여유"
        }

    return result