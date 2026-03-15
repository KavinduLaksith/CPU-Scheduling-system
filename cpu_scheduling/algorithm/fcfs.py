def run_fcfs(processes):

    # sort processes by arrival time
    processes.sort(key=lambda x: x["arrival"])

    time = 0
    results = []

    print("\nFCFS Scheduling\n")

    for p in processes:

        if time < p["arrival"]:
            time = p["arrival"]

        completion_time = time + p["burst"]
        turnaround_time = completion_time - p["arrival"]
        waiting_time = turnaround_time - p["burst"]

        results.append({
            "pid": p["pid"],
            "completion": completion_time,
            "tat": turnaround_time,
            "wt": waiting_time
        })

        time = completion_time

    return results