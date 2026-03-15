def run_srtn(processes):

    time = 0
    completed = 0
    n = len(processes)

    remaining = {p["pid"]: p["burst"] for p in processes}
    completion = {}

    processes = processes.copy()

    while completed < n:

        ready = []

        for p in processes:
            if p["arrival"] <= time and remaining[p["pid"]] > 0:
                ready.append(p)

        if not ready:
            time += 1
            continue

        # choose process with smallest remaining time
        ready.sort(key=lambda x: remaining[x["pid"]])
        current = ready[0]

        pid = current["pid"]

        remaining[pid] -= 1
        time += 1

        if remaining[pid] == 0:
            completion[pid] = time
            completed += 1

    results = []

    for p in processes:

        tat = completion[p["pid"]] - p["arrival"]
        wt = tat - p["burst"]

        results.append({
            "pid": p["pid"],
            "completion": completion[p["pid"]],
            "tat": tat,
            "wt": wt
        })

    return results