def run_priority(processes):

    time = 0
    completed = []
    results = []

    processes = processes.copy()
    n = len(processes)

    while len(completed) < n:

        ready = []

        for p in processes:
            if p["arrival"] <= time and p["pid"] not in completed:
                ready.append(p)

        if not ready:
            time += 1
            continue

        # choose process with highest priority (lowest number)
        ready.sort(key=lambda x: x["priority"])
        current = ready[0]

        completion_time = time + current["burst"]
        tat = completion_time - current["arrival"]
        wt = tat - current["burst"]

        results.append({
            "pid": current["pid"],
            "completion": completion_time,
            "tat": tat,
            "wt": wt
        })

        time = completion_time
        completed.append(current["pid"])

    return results