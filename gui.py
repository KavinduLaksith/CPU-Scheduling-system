import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from algorithm.fcfs import run_fcfs
from algorithm.round_robin import run_round_robin
from algorithm.sjf import run_sjf
from algorithm.srtn import run_srtn
from algorithm.priority import run_priority


# ---------------- Add Process ----------------

def add_process():

    pid = pid_entry.get()
    arrival = arrival_entry.get()
    burst = burst_entry.get()
    priority = priority_entry.get()

    if pid == "" or arrival == "" or burst == "":
        messagebox.showerror("Error", "Fill PID, Arrival, Burst")
        return

    if priority == "":
        priority = 0

    process_table.insert("", "end", values=(pid, arrival, burst, priority))

    pid_entry.delete(0, tk.END)
    arrival_entry.delete(0, tk.END)
    burst_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)


# ---------------- Get Processes ----------------

def get_processes():

    processes = []

    for row in process_table.get_children():

        values = process_table.item(row)["values"]

        processes.append({
            "pid": values[0],
            "arrival": int(values[1]),
            "burst": int(values[2]),
            "priority": int(values[3])
        })

    return processes
# ---------------- Enter Key Navigation ----------------

def go_to_arrival(event):
    arrival_entry.focus_set()

def go_to_burst(event):
    burst_entry.focus_set()

def go_to_priority(event):
    priority_entry.focus_set()

def add_with_enter(event):
    add_process()
    pid_entry.focus_set()


# ---------------- Gantt Chart ----------------

def draw_gantt(results, algorithm_name):

    fig, ax = plt.subplots()

    start = 0
    y = 50

    colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336",'#F44325',
    '']

    for i, r in enumerate(results):

        finish = r["completion"]
        duration = finish - start

        ax.broken_barh(
            [(start, duration)],
            (y, 5),
            facecolors=colors[i % len(colors)],
            edgecolors="black"
        )

        ax.text(
            start + duration / 2,
            y + 2.5,
            "P" + str(r["pid"]),
            ha="center",
            va="center",
            color="white",
            fontsize=11
        )

        ax.text(start, y - 1, str(start))

        start = finish

    ax.text(start, y - 1, str(start))

    ax.set_ylim(5, 20)
    ax.set_xlim(0, start + 1)

    ax.set_xlabel("Time")
    ax.set_title(f"{algorithm_name} Gantt Chart")

    ax.set_yticks([])

    plt.show()

def draw_rr_gantt(timeline):

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    y = 10

    colors = ["#4CAF50","#2196F3","#FF9800","#9C27B0","#F44336"]

    for i,(pid,start,end) in enumerate(timeline):

        duration = end - start

        ax.broken_barh(
            [(start,duration)],
            (y,5),
            facecolors=colors[i%len(colors)],
            edgecolors="black"
        )

        ax.text(
            start + duration/2,
            y + 2.5,
            "P"+str(pid),
            ha="center",
            va="center",
            color="white"
        )

        ax.text(start,y-1,str(start))

    ax.text(end,y-1,str(end))

    ax.set_xlabel("Time")
    ax.set_title("Round Robin Gantt Chart")

    ax.set_yticks([])

    plt.show()


# ---------------- Calculate Average ----------------

def calculate_avg(results):

    total_wt = sum(r["wt"] for r in results)
    total_tat = sum(r["tat"] for r in results)

    avg_wt = total_wt / len(results)
    avg_tat = total_tat / len(results)

    return avg_wt, avg_tat


# ---------------- Show Results ----------------

def show_results(results, name):

    result_text.insert(tk.END, "\n================================\n")
    result_text.insert(tk.END, name + "\n")
    result_text.insert(tk.END, "================================\n")

    result_text.insert(tk.END, "PID    Completion    TAT    WT\n")

    for r in results:

        result_text.insert(
            tk.END,
            f"{r['pid']}       {r['completion']}       {r['tat']}       {r['wt']}\n"
        )


# ---------------- RUN ----------------

def run_algorithms():

    processes = get_processes()

    if len(processes) == 0:
        messagebox.showerror("Error", "Add processes first")
        return

    result_text.delete("1.0", tk.END)

    quantum = quantum_entry.get()

    if quantum == "":
        quantum = 2
    else:
        quantum = int(quantum)

    lower_priority = priority_rule.get() == 1

    comparison = []


    # FCFS
    if fcfs_var.get():

        fcfs_results = run_fcfs(processes)

        show_results(fcfs_results, "FCFS")

        avg_wt, avg_tat = calculate_avg(fcfs_results)

        result_text.insert(tk.END, f"\nAverage WT : {avg_wt:.2f}\n")
        result_text.insert(tk.END, f"Average TAT : {avg_tat:.2f}\n")

        draw_gantt(fcfs_results, "FCFS")

        comparison.append(("FCFS", avg_wt))


    # Round Robin
    if rr_var.get():

        rr_results = run_round_robin(processes, quantum)

        show_results(rr_results, "Round Robin")

        avg_wt, avg_tat = calculate_avg(rr_results)

        result_text.insert(tk.END, f"\nAverage WT : {avg_wt:.2f}\n")
        result_text.insert(tk.END, f"Average TAT : {avg_tat:.2f}\n")

        draw_gantt(rr_results, "Round Robin")

        comparison.append(("Round Robin", avg_wt))


    # SJF
    if sjf_var.get():

        sjf_results = run_sjf(processes)

        show_results(sjf_results, "SJF")

        avg_wt, avg_tat = calculate_avg(sjf_results)

        result_text.insert(tk.END, f"\nAverage WT : {avg_wt:.2f}\n")
        result_text.insert(tk.END, f"Average TAT : {avg_tat:.2f}\n")

        draw_gantt(sjf_results, "SJF")

        comparison.append(("SJF", avg_wt))


    # SRTN
    if srtn_var.get():

        srtn_results = run_srtn(processes)

        show_results(srtn_results, "SRTN")

        avg_wt, avg_tat = calculate_avg(srtn_results)

        result_text.insert(tk.END, f"\nAverage WT : {avg_wt:.2f}\n")
        result_text.insert(tk.END, f"Average TAT : {avg_tat:.2f}\n")

        draw_gantt(srtn_results, "SRTN")

        comparison.append(("SRTN", avg_wt))


    # Priority
    if priority_var.get():

        priority_results = run_priority(processes, lower_priority)

        show_results(priority_results, "Priority")

        avg_wt, avg_tat = calculate_avg(priority_results)

        result_text.insert(tk.END, f"\nAverage WT : {avg_wt:.2f}\n")
        result_text.insert(tk.END, f"Average TAT : {avg_tat:.2f}\n")

        draw_gantt(priority_results, "Priority")

        comparison.append(("Priority", avg_wt))


    # Algorithm Comparison

    result_text.insert(tk.END, "\n================================\n")
    result_text.insert(tk.END, "Algorithm Comparison\n")
    result_text.insert(tk.END, "================================\n")

    for name, wt in comparison:
        result_text.insert(tk.END, f"{name} : {wt:.2f}\n")

    best = min(comparison, key=lambda x: x[1])

    result_text.insert(tk.END, f"\nBest Algorithm : {best[0]}\n")
    result_text.insert(tk.END, "Reason : Minimum Average Waiting Time\n")


# ---------------- GUI ----------------

root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1000x750")


title = tk.Label(root, text="CPU Scheduling Simulator", font=("Arial", 18))
title.pack(pady=10)


# Input Section

input_frame = tk.Frame(root)
input_frame.pack()

tk.Label(input_frame, text="PID").grid(row=0, column=0)
tk.Label(input_frame, text="Arrival").grid(row=0, column=1)
tk.Label(input_frame, text="Burst(Service Time)").grid(row=0, column=2)
tk.Label(input_frame, text="Priority").grid(row=0, column=3)

pid_entry = tk.Entry(input_frame)
arrival_entry = tk.Entry(input_frame)
burst_entry = tk.Entry(input_frame)
priority_entry = tk.Entry(input_frame)

pid_entry.grid(row=1, column=0)
arrival_entry.grid(row=1, column=1)
burst_entry.grid(row=1, column=2)
priority_entry.grid(row=1, column=3)

tk.Button(input_frame, text="Add Process", command=add_process).grid(row=1, column=4)


# Process Table

columns = ("PID", "Arrival", "Burst", "Priority")

process_table = ttk.Treeview(root, columns=columns, show="headings", height=6)

for col in columns:
    process_table.heading(col, text=col)

process_table.pack(pady=10)


# Algorithm Selection

alg_frame = tk.Frame(root)
alg_frame.pack()

fcfs_var = tk.BooleanVar()
rr_var = tk.BooleanVar()
sjf_var = tk.BooleanVar()
srtn_var = tk.BooleanVar()
priority_var = tk.BooleanVar()

tk.Checkbutton(alg_frame, text="FCFS(First Come First Serve)", variable=fcfs_var).grid(row=0, column=0)
tk.Checkbutton(alg_frame, text="Round Robin", variable=rr_var).grid(row=0, column=1)
tk.Checkbutton(alg_frame, text="SJF(Shortest Job First)", variable=sjf_var).grid(row=0, column=2)
tk.Checkbutton(alg_frame, text="SRTN(Shortest Remaining Time Next)", variable=srtn_var).grid(row=0, column=3)
tk.Checkbutton(alg_frame, text="Priority", variable=priority_var).grid(row=0, column=4)


# Quantum Input

quantum_frame = tk.Frame(root)
quantum_frame.pack()

tk.Label(quantum_frame, text="Time Quantum").pack(side="left")
quantum_entry = tk.Entry(quantum_frame, width=5)
quantum_entry.pack(side="left")


# Priority Rule

priority_frame = tk.Frame(root)
priority_frame.pack()

priority_rule = tk.IntVar(value=1)

tk.Radiobutton(priority_frame, text="Lower number = higher priority", variable=priority_rule, value=1).pack()
tk.Radiobutton(priority_frame, text="Higher number = higher priority", variable=priority_rule, value=2).pack()


tk.Button(root, text="RUN", command=run_algorithms).pack(pady=10)


# Results Panel

result_text = tk.Text(root, height=20, width=110)
result_text.pack()

root.mainloop()