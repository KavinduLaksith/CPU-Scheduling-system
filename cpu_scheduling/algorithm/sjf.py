def run_sjf(processes):

    processes = sorted(processes, key=lambda x: (x["arrival"], x["burst"]))

    current_time = 0
    results = []
    gantt = []

    for p in processes:

        pid = p["pid"]
        arrival = p["arrival"]
        burst = p["burst"]

        if current_time < arrival:
            current_time = arrival

        start = current_time
        end = current_time + burst

        gantt.append((pid, start, end))

        completion = end
        tat = completion - arrival
        wt = tat - burst

        results.append({
            "pid": pid,
            "completion": completion,
            "tat": tat,
            "wt": wt
        })

        current_time = end

    return results, gantt