def check(exp, got):
    # Trả về "" nếu đạt, hoặc lý do sai
    if len(exp["decisions"]) != len(got["decisions"]):
        return f"decisions: đáp án {len(exp['decisions'])}, model {len(got['decisions'])}"
    if len(exp["actions"]) != len(got["actions"]):
        return f"actions: đáp án {len(exp['actions'])}, model {len(got['actions'])}"
    left = [(a["owner"], a["due_date"]) for a in got["actions"]]
    for a in exp["actions"]:
        key = (a["owner"], a["due_date"])
        if key not in left:
            return f"thiếu action (owner={a['owner']}, due_date={a['due_date']})"
        left.remove(key)
    return ""
