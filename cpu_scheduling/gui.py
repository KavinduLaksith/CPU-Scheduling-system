import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# import your algorithm functions
from algorithm.fcfs import run_fcfs
from algorithm.sjf import run_sjf
from algorithm.srtn import run_srtn
from algorithm.priority import run_priority
from algorithm.round_robin import run_round_robin


root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("900x600")

# =============================
# PAGE CONTROL
# =============================

container = tk.Frame(root)
container.pack(fill="both", expand=True)

page1 = tk.Frame(container)
page2 = tk.Frame(container)
page3 = tk.Frame(container)

for page in (page1, page2, page3):
    page.grid(row=0, column=0, sticky="nsew")

def show_page(page):
    page.tkraise()

# =============================
# PAGE 1 - PROCESS INPUT
# =============================

title = tk.Label(page1, text="CPU Scheduling Simulator", font=("Arial",18))
title.pack(pady=10)

input_frame = tk.Frame(page1)
input_frame.pack(pady=10)

tk.Label(input_frame, text="PID").grid(row=0,column=0)
tk.Label(input_frame, text="Arrival").grid(row=0,column=1)
tk.Label(input_frame, text="Burst").grid(row=0,column=2)
tk.Label(input_frame, text="Priority").grid(row=0,column=3)

pid_entry = tk.Entry(input_frame,width=8)
arrival_entry = tk.Entry(input_frame,width=8)
burst_entry = tk.Entry(input_frame,width=8)
priority_entry = tk.Entry(input_frame,width=8)

pid_entry.grid(row=1,column=0)
arrival_entry.grid(row=1,column=1)
burst_entry.grid(row=1,column=2)
priority_entry.grid(row=1,column=3)


pid_entry.bind("<Return>", lambda e: arrival_entry.focus())
arrival_entry.bind("<Return>", lambda e: burst_entry.focus())
burst_entry.bind("<Return>", lambda e: priority_entry.focus())
priority_entry.bind("<Return>", lambda e: add_process())




# process table
columns=("PID","Arrival","Burst","Priority")
process_table = ttk.Treeview(page1,columns=columns,show="headings",height=6)

for col in columns:
    process_table.heading(col,text=col)
    process_table.column(col,width=120,anchor="center")

process_table.pack(pady=10)

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

    # Add to table
    process_table.insert("", "end", values=(pid, arrival, burst, priority))

    # CLEAR INPUT FIELDS
    pid_entry.delete(0, tk.END)
    arrival_entry.delete(0, tk.END)
    burst_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)

    # Move cursor back to PID for next process
    pid_entry.focus()
    
def clear_processes():

    for item in process_table.get_children():
        process_table.delete(item)

    pid_entry.delete(0,tk.END)
    arrival_entry.delete(0,tk.END)
    burst_entry.delete(0,tk.END)
    priority_entry.delete(0,tk.END)

    pid_entry.focus()

def delete_process():

    selected = process_table.selection()

    if not selected:
        messagebox.showwarning("Warning","Select a process to delete")
        return

    for item in selected:
        process_table.delete(item)

tk.Button(input_frame,text="Add Process",command=add_process).grid(row=1,column=4,padx=5)
tk.Button(page1, text="Clear All Processes", command=clear_processes).pack(pady=5)
tk.Button(page1, text="Delete Selected", command=delete_process).pack(pady=5)
tk.Button(page1,text="Next → Choose Algorithm",
          command=lambda: show_page(page2),
          width=25).pack(pady=20)

# =============================
# PAGE 2 - ALGORITHM SELECTION
# =============================

tk.Label(page2,text="Choose Algorithm",font=("Arial",16)).pack(pady=10)

algo_container = tk.Frame(page2)
algo_container.pack(pady=20)

fcfs_var = tk.BooleanVar()
sjf_var = tk.BooleanVar()
srtn_var = tk.BooleanVar()
priority_var = tk.BooleanVar()
rr_var = tk.BooleanVar()

algo_frame = tk.LabelFrame(algo_container, text="Algorithms", padx=20, pady=10)
algo_frame.grid(row=0, column=0, padx=20)

tk.Checkbutton(algo_frame, text="FCFS", variable=fcfs_var).pack(anchor="w")
tk.Checkbutton(algo_frame, text="SJF", variable=sjf_var).pack(anchor="w")
tk.Checkbutton(algo_frame, text="SRTN", variable=srtn_var).pack(anchor="w")
tk.Checkbutton(algo_frame, text="Priority", variable=priority_var).pack(anchor="w")
tk.Checkbutton(algo_frame, text="Round Robin", variable=rr_var).pack(anchor="w")
# Round Robin options
rr_type_var = tk.StringVar(value="fcfs")

rr_frame = tk.LabelFrame(algo_container, text="Round Robin Settings", padx=20, pady=10)
rr_frame.grid(row=0, column=1, padx=20)

tk.Radiobutton(rr_frame, text="FCFS Round Robin", variable=rr_type_var, value="fcfs").pack(anchor="w")
tk.Radiobutton(rr_frame, text="SJF Round Robin", variable=rr_type_var, value="sjf").pack(anchor="w")
tk.Radiobutton(rr_frame, text="SRTN Round Robin", variable=rr_type_var, value="srtn").pack(anchor="w")
tk.Radiobutton(rr_frame, text="Priority Round Robin", variable=rr_type_var, value="priority").pack(anchor="w")

tk.Label(rr_frame, text="Time Quantum").pack(pady=(10,0))
quantum_entry = tk.Entry(rr_frame, width=8)
quantum_entry.pack()

# priority rule
priority_rule_var = tk.StringVar(value="lower")

rule_frame = tk.LabelFrame(algo_container, text="Priority Rule", padx=20, pady=10)
rule_frame.grid(row=1, column=0, columnspan=2, pady=20)

tk.Label(rule_frame,text="Priority Rule").pack()

tk.Radiobutton(rule_frame,
               text="Lower number higher priority",
               variable=priority_rule_var,
               value="lower").pack(anchor="w")

tk.Radiobutton(rule_frame,
               text="Higher number higher priority",
               variable=priority_rule_var,
               value="higher").pack(anchor="w")

button_frame = tk.Frame(page2)
button_frame.pack(pady=20)


tk.Button(button_frame,text="← Previous",width=15,
          command=lambda: show_page(page1)).grid(row=0,column=1,padx=10)

# =============================
# PAGE 3 - RESULTS
# =============================

# Results title
tk.Label(page3, text="Results", font=("Arial",18)).pack(pady=10)

# scrollable canvas
canvas = tk.Canvas(page3)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(page3, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# frame inside canvas
result_frame = tk.Frame(canvas)

canvas_window = canvas.create_window((0,0), window=result_frame, anchor="nw")

def resize_canvas(event):
    canvas.itemconfig(canvas_window, width=event.width)
    result_frame.config(width= event.width)
    result_frame.columnconfigure(0, weight=1)

canvas.bind("<Configure>", resize_canvas)

def configure_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

result_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

tk.Button(page3, text="← Back to Algorithms", command=lambda: show_page(page2)).pack(pady=10)



# =============================
# HELPER FUNCTIONS
# =============================

def get_processes():

    processes=[]

    for row in process_table.get_children():

        vals = process_table.item(row)["values"]

        processes.append({
            "pid": vals[0],
            "arrival": int(vals[1]),
            "burst": int(vals[2]),
            "priority": int(vals[3])
        })

    return processes
def show_result_table(frame, processes, results):

    import tkinter.ttk as ttk

    columns = ("PID","Arrival","Burst","Priority","WT","TAT")

    table = ttk.Treeview(frame, columns=columns, show="headings", height=6)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=140, anchor="center")
        table.column("PID", width=80, anchor="center")
        table.column("Arrival", width=100, anchor="center")
        table.column("Burst", width=100, anchor="center")
        table.column("Priority", width=100, anchor="center")
        table.column("WT", width=100, anchor="center")
        table.column("TAT", width=100, anchor="center")

    table.pack(pady=10)

    for r in results:

        pid = r["pid"]

        process = next(p for p in processes if p["pid"] == pid)

        table.insert("", "end", values=(
            pid,
            process["arrival"],
            process["burst"],
            process["priority"],
            r["wt"],
            r["tat"]
        ))




def calculate_avg(results):

    total_wt = sum(r["wt"] for r in results)
    total_tat = sum(r["tat"] for r in results)

    avg_wt = total_wt / len(results)
    avg_tat = total_tat / len(results)

    return avg_wt, avg_tat   


# =============================
# DRAW GANT chart
# =============================

def draw_gantt(gantt, algorithm_name, frame):

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    fig, ax = plt.subplots(figsize=(20,3))

    y = 10

    colors = ["#4CAF50","#2196F3","#FF9800","#9C27B0","#F44336"]

    for i,(pid,start,end) in enumerate(gantt):

        duration = end - start

        ax.broken_barh([(start,duration)],(y,5),
                       facecolors=colors[i % len(colors)],
                       edgecolors="black")

        ax.text(start + duration/2,
                y + 2.5,
                f"{pid}",
                ha="center",
                va="center",
                color="white",
                fontsize=9)

        ax.text(start,y-1,str(start))

    ax.text(gantt[-1][2],y-1,str(gantt[-1][2]))

    ax.set_ylim(5,20)
    ax.set_xlim(0,gantt[-1][2]+1)

    ax.set_yticks([])
    ax.set_title(f"{algorithm_name} Gantt Chart")
    ax.set_xlabel("Time")

    canvas = FigureCanvasTkAgg(fig,master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# =============================
# RUN ALGORITHMS
# =============================


def run_algorithms():

    processes = get_processes()

    if not processes:
        messagebox.showerror("Error","No processes added")
        return
    for widget in result_frame.winfo_children():
        widget.destroy()

    if rr_var.get() and quantum_entry.get() == "":
        messagebox.showerror("Error", "Enter Time Quantum")
        return
    comparison=[]

    # FCFS
    
    if fcfs_var.get():

        results = run_fcfs(processes)
        
            
        avg_wt, avg_tat = calculate_avg(results)

        section = tk.Frame(result_frame)
        section.pack(fill="both",expand=True,pady=15)
        

        tk.Label(section,text="FCFS",font=("Arial",14)).pack()
        show_result_table(section,processes,results)
        tk.Label(section,text=f"Average WT: {avg_wt:.2f}",font=("Arial",12)).pack()
        tk.Label(section,text=f"Average TAT: {avg_tat:.2f}",font=("Arial",12)).pack()
 
        
        # create gantt
        gantt=[]
        current=0
        for r in results:
            pid=r["pid"]
            burst=next(p["burst"] for p in processes if p["pid"]==pid)
            start=current
            end=current+burst
            gantt.append((pid,start,end))
            current=end

        

        draw_gantt(gantt,"FCFS",section)
        comparison.append(("FCFS", avg_wt))

    # SJF
    if sjf_var.get():

        results,gantt = run_sjf(processes)
        

        avg_wt, avg_tat = calculate_avg(results)

        section = tk.Frame(result_frame)
        section.pack(fill="both",expand=True,pady=15)
        

        tk.Label(section, text="SJF", font=("Arial",14)).pack()
        show_result_table(section,processes,results)
        tk.Label(section,
                text=f"Average WT: {avg_wt:.2f}",
                font=("Arial", 12)).pack()

        tk.Label(section,
                text=f"Average TAT: {avg_tat:.2f}",
                font=("Arial", 12)).pack()
        
        

        draw_gantt(gantt,  "SJF", section)

        comparison.append(("SJF", avg_wt))

    # SRTN
    if srtn_var.get():

        results,gantt = run_srtn(processes)
        

        avg_wt, avg_tat = calculate_avg(results)

        section = tk.Frame(result_frame)
        section.pack(fill='both',expand=True,pady=15)
        

        tk.Label(section, text="SRTN", font=("Arial",14)).pack()
        
        show_result_table(section,processes,results)
        tk.Label(section,
                text=f"Average WT: {avg_wt:.2f}",
                font=("Arial", 12)).pack()

        tk.Label(section,
                text=f"Average TAT: {avg_tat:.2f}",
                font=("Arial", 12)).pack()
        
        

        draw_gantt(gantt,  "SRTN", section)

        comparison.append(("SRTN", avg_wt))

    # Priority
    if priority_var.get():

        lower_priority = priority_rule_var.get() == "lower"

        results,gantt = run_priority(processes, lower_priority)
        
        avg_wt, avg_tat = calculate_avg(results)

        section = tk.Frame(result_frame)
        section.pack(fill="both",expand=True,pady=15)
        

        tk.Label(section, text="Priority", font=("Arial",14)).pack()

        show_result_table(section,processes,results)
        tk.Label(section,
                text=f"Average WT: {avg_wt:.2f}",
                font=("Arial", 12)).pack()

        tk.Label(section,
                text=f"Average TAT: {avg_tat:.2f}",
                font=("Arial", 12)).pack()
        

        draw_gantt(gantt,  "Priority", section)

        comparison.append(("Priority", avg_wt))

    # Round Robin
    if rr_var.get():

        if quantum_entry.get() == "":
            messagebox.showerror("Error","Enter Time Quantum")
            return

        quantum = int(quantum_entry.get())

        rr_type = rr_type_var.get()

        lower_priority = (priority_rule_var.get() == "lower")

        results, gantt = run_round_robin(
            processes,
            quantum,
            rr_type,
            lower_priority
        )
        
        avg_wt, avg_tat = calculate_avg(results)

        section = tk.Frame(result_frame)
        section.pack(fill="both",expand=True,pady=15)

        

        tk.Label(section,
                text=f"{rr_type} Round Robin",
                font=("Arial",14,"bold")).pack()
        
        show_result_table(section,processes,results)

        tk.Label(section,
                text=f"Average WT: {avg_wt:.2f}",
                font=("Arial",12)).pack()

        tk.Label(section,
                text=f"Average TAT: {avg_tat:.2f}",
                font=("Arial",12)).pack()
        

        draw_gantt(gantt, 
                f"{rr_type} Round Robin",
                section)
        
        comparison.append((f"{rr_type} Round Robin", avg_wt))
    # comparison
    comparison_section = tk.Frame(result_frame)
    comparison_section.pack(fill="x",pady=30)

    tk.Label(comparison_section,
            text="Algorithm Comparison",
            font=("Arial",14,"bold")).pack()

    for name, wt in comparison:
        tk.Label(comparison_section,
                text=f"{name} : {wt:.2f}").pack()
        
    if not comparison:
        messagebox.showerror("Error","Select at least one algorithm")
        return

    best = min(comparison, key=lambda x: x[1])

    tk.Label(comparison_section,
         text=f"Best Algorithm : {best[0]}",
         font=("Arial",12,"bold")).pack()
    
    comparison_section.pack(fill="both",expand=True,pady=20)

    show_page(page3)

tk.Button(button_frame,text="RUN",width=15,
          command=run_algorithms).grid(row=0,column=0,padx=10)



show_page(page1)

root.mainloop()