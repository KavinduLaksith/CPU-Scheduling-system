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


# ---------------- Gantt Chart ----------------

def draw_gantt(results, title):

    fig, ax = plt.subplots()

    start = 0

    for r in results:

        duration = r["tat"] - r["wt"]

        ax.broken_barh([(start, duration)], (10, 5))
        ax.text(start + duration/2, 12.5, r["pid"], ha='center', color="white")

        start += duration

    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_title(title + " Gantt Chart")

    plt.show()


# ---------------- Show Results ----------------

def show_table(results):

    result_table.delete(*result_table.get_children())

    for r in results:
        result_table.insert("", "end",
                            values=(r["pid"], r["completion"], r["tat"], r["wt"]))


def calculate_avg(results):

    total_wt = sum(r["wt"] for r in results)
    total_tat = sum(r["tat"] for r in results)

    avg_wt = total_wt / len(results)
    avg_tat = total_tat / len(results)

    return avg_wt, avg_tat


# ---------------- RUN ----------------

def run_algorithms():

    processes = get_processes()

    if len(processes) == 0:
        messagebox.showerror("Error", "Add processes first")
        return

    quantum = quantum_entry.get()

    if quantum == "":
        quantum = 2
    else:
        quantum = int(quantum)

    lower_priority = priority_rule.get() == 1

    comparison = []

    result_text.delete("1.0", tk.END)

    # FCFS
    if fcfs_var.get():

        results = run_fcfs(processes)

        show_table(results)

        avg_wt, avg_tat = calculate_avg(results)

        result_text.insert(tk.END, f"\nFCFS\nAverage WT: {avg_wt:.2f}\nAverage TAT: {avg_tat:.2f}\n")

        draw_gantt(results, "FCFS")

        comparison.append(("FCFS", avg_wt))


    # Round Robin
    if rr_var.get():

        results = run_round_robin(processes, quantum)

        show_table(results)

        avg_wt, avg_tat = calculate_avg(results)

        result_text.insert(tk.END, f"\nRound Robin\nAverage WT: {avg_wt:.2f}\nAverage TAT: {avg_tat:.2f}\n")

        draw_gantt(results, "Round Robin")

        comparison.append(("Round Robin", avg_wt))


    # SJF
    if sjf_var.get():

        results = run_sjf(processes)

        show_table(results)

        avg_wt, avg_tat = calculate_avg(results)

        result_text.insert(tk.END, f"\nSJF\nAverage WT: {avg_wt:.2f}\nAverage TAT: {avg_tat:.2f}\n")

        draw_gantt(results, "SJF")

        comparison.append(("SJF", avg_wt))


    # SRTN
    if srtn_var.get():

        results = run_srtn(processes)

        show_table(results)

        avg_wt, avg_tat = calculate_avg(results)

        result_text.insert(tk.END, f"\nSRTN\nAverage WT: {avg_wt:.2f}\nAverage TAT: {avg_tat:.2f}\n")

        draw_gantt(results, "SRTN")

        comparison.append(("SRTN", avg_wt))


    # Priority
    if priority_var.get():

        results = run_priority(processes, lower_priority)

        show_table(results)

        avg_wt, avg_tat = calculate_avg(results)

        result_text.insert(tk.END, f"\nPriority\nAverage WT: {avg_wt:.2f}\nAverage TAT: {avg_tat:.2f}\n")

        draw_gantt(results, "Priority")

        comparison.append(("Priority", avg_wt))


    # Comparison

    if comparison:

        result_text.insert(tk.END, "\nAlgorithm Comparison\n")

        for name, wt in comparison:
            result_text.insert(tk.END, f"{name} : {wt:.2f}\n")

        best = min(comparison, key=lambda x: x[1])

        result_text.insert(tk.END, f"\nBest Algorithm : {best[0]}\n")


# ---------------- GUI ----------------

root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1000x750")


title = tk.Label(root, text="CPU Scheduling Simulator", font=("Arial", 18))
title.pack(pady=10)


# ---------------- Input ----------------

input_frame = tk.Frame(root)
input_frame.pack()

tk.Label(input_frame, text="PID").grid(row=0, column=0)
tk.Label(input_frame, text="Arrival").grid(row=0, column=1)
tk.Label(input_frame, text="Burst").grid(row=0, column=2)
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


# ---------------- Process Table ----------------

columns = ("PID", "Arrival", "Burst", "Priority")

process_table = ttk.Treeview(root, columns=columns, show="headings", height=6)

for col in columns:
    process_table.heading(col, text=col)

process_table.pack(pady=10)


# ---------------- Algorithm Selection ----------------

alg_frame = tk.Frame(root)
alg_frame.pack()

fcfs_var = tk.BooleanVar()
rr_var = tk.BooleanVar()
sjf_var = tk.BooleanVar()
srtn_var = tk.BooleanVar()
priority_var = tk.BooleanVar()

tk.Checkbutton(alg_frame, text="FCFS", variable=fcfs_var).grid(row=0, column=0)
tk.Checkbutton(alg_frame, text="Round Robin", variable=rr_var).grid(row=0, column=1)
tk.Checkbutton(alg_frame, text="SJF", variable=sjf_var).grid(row=0, column=2)
tk.Checkbutton(alg_frame, text="SRTN", variable=srtn_var).grid(row=0, column=3)
tk.Checkbutton(alg_frame, text="Priority", variable=priority_var).grid(row=0, column=4)


# Quantum

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


# ---------------- Results Table ----------------

result_columns = ("PID", "Completion", "TAT", "WT")

result_table = ttk.Treeview(root, columns=result_columns, show="headings", height=6)

for col in result_columns:
    result_table.heading(col, text=col)

result_table.pack(pady=10)


# Result Text

result_text = tk.Text(root, height=10, width=100)
result_text.pack()


root.mainloop()