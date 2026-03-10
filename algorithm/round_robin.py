def run_round_robin(processes, quantum):

    time = 0
    queue = []
    results = []

    processes.sort(key=lambda x: x["arrival"])

    remaining = {p["pid"]: p["burst"] for p in processes}
    completion = {}

    arrived = []
    i = 0
    n = len(processes)

    while len(completion) < n:

        # add newly arrived processes
        while i < n and processes[i]["arrival"] <= time:
            queue.append(processes[i]["pid"])
            arrived.append(processes[i]["pid"])
            i += 1

        if not queue:
            time += 1
            continue

        pid = queue.pop(0)

        run_time = min(quantum, remaining[pid])

        time += run_time
        remaining[pid] -= run_time

        # check new arrivals during execution
        while i < n and processes[i]["arrival"] <= time:
            queue.append(processes[i]["pid"])
            arrived.append(processes[i]["pid"])
            i += 1

        if remaining[pid] > 0:
            queue.append(pid)
        else:
            completion[pid] = time

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