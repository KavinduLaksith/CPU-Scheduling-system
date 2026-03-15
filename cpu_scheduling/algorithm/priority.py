def run_priority(processes, lower_priority=True):

    # sort by arrival time first
    processes = sorted(processes, key=lambda x: x["arrival"])

    time = 0
    completed = 0
    n = len(processes)

    ready_queue = []
    results = []
    gantt = []

    visited = [False] * n

    while completed < n:

        # add arrived processes to ready queue
        for i in range(n):
            if processes[i]["arrival"] <= time and not visited[i]:
                ready_queue.append(processes[i])
                visited[i] = True

        if not ready_queue:
            time += 1
            continue

        # choose process based on priority rule
        if lower_priority:
            ready_queue.sort(key=lambda x: x["priority"])
        else:
            ready_queue.sort(key=lambda x: -x["priority"])

        process = ready_queue.pop(0)

        pid = process["pid"]
        arrival = process["arrival"]
        burst = process["burst"]
        priority = process["priority"]

        start = time
        end = time + burst

        gantt.append((pid, start, end))

        time = end

        completion = end
        tat = completion - arrival
        wt = tat - burst

        results.append({
            "pid": pid,
            "completion": completion,
            "tat": tat,
            "wt": wt
        })

        completed += 1

    return results, gantt