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


def compare_details(exp, got):
    # Bảng so sánh từng hạng mục với gold để hiện trên demo
    rows = []
    n_exp_d, n_got_d = len(exp["decisions"]), len(got["decisions"])
    rows.append({
        "item": "Số decisions",
        "gold": str(n_exp_d),
        "ai": str(n_got_d),
        "ok": n_exp_d == n_got_d,
    })
    n_exp_a, n_got_a = len(exp["actions"]), len(got["actions"])
    rows.append({
        "item": "Số actions",
        "gold": str(n_exp_a),
        "ai": str(n_got_a),
        "ok": n_exp_a == n_got_a,
    })

    left = [(a["owner"], a["due_date"]) for a in got["actions"]]
    for i, a in enumerate(exp["actions"], start=1):
        key = (a["owner"], a["due_date"])
        ok = key in left
        if ok:
            left.remove(key)
        rows.append({
            "item": f"Action {i} (owner + due_date)",
            "gold": f"{a['owner']} / {a['due_date']}",
            "ai": f"{a['owner']} / {a['due_date']}" if ok else "không khớp / thiếu",
            "ok": ok,
        })
    for j, key in enumerate(left, start=1):
        rows.append({
            "item": f"Action thừa {j}",
            "gold": "—",
            "ai": f"{key[0]} / {key[1]}",
            "ok": False,
        })
    return rows
