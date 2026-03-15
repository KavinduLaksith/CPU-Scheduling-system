def run_round_robin(processes, quantum, rr_type="fcfs", lower_priority=True):

    processes = sorted(processes, key=lambda x: x["arrival"])

    time = 0
    ready_queue = []
    results = []
    gantt = []

    remaining = {p["pid"]: p["burst"] for p in processes}
    completion = {}

    i = 0
    n = len(processes)

    while len(completion) < n:

        # add arrived processes
        while i < n and processes[i]["arrival"] <= time:
            ready_queue.append(processes[i])
            i += 1

        if not ready_queue:
            time += 1
            continue

        # -------- SELECT PROCESS BASED ON TYPE --------

        if rr_type == "FCFS":
            process = ready_queue.pop(0)

        elif rr_type == "SJF":
            ready_queue.sort(key=lambda x: x["burst"])
            process = ready_queue.pop(0)

        elif rr_type == "SRTN":
            ready_queue.sort(key=lambda x: remaining[x["pid"]])
            process = ready_queue.pop(0)

        elif rr_type == "PRIORITY":
            if lower_priority:
                ready_queue.sort(key=lambda x: x["priority"])
            else:
                ready_queue.sort(key=lambda x: -x["priority"])
            process = ready_queue.pop(0)

        else:
            process = ready_queue.pop(0)

        pid = process["pid"]

        run_time = min(quantum, remaining[pid])

        start = time
        time += run_time
        end = time

        # correct gantt slice
        gantt.append((pid, start, end))

        remaining[pid] -= run_time

        # add new arrivals
        while i < n and processes[i]["arrival"] <= time:
            ready_queue.append(processes[i])
            i += 1

        # if not finished, return to queue
        if remaining[pid] > 0:
            ready_queue.append(process)
        else:
            completion[pid] = time

    # calculate results
    for p in processes:

        pid = p["pid"]

        tat = completion[pid] - p["arrival"]
        wt = tat - p["burst"]

        results.append({
            "pid": pid,
            "completion": completion[pid],
            "tat": tat,
            "wt": wt
        })

    return results, gantt