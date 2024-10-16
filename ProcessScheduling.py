import tkinter as tk
from tkinter import ttk
from collections import deque

def findWaitingTimeFCFS(processes, n, wt):
    wt[0] = 0
    for i in range(1, n):
        wt[i] = processes[i - 1][1] + wt[i - 1]

def findTurnAroundTimeFCFS(processes, n, wt, tat):
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

def findavgTimeFCFS(processes, n):
    wt = [0] * n
    tat = [0] * n
    findWaitingTimeFCFS(processes, n, wt)
    findTurnAroundTimeFCFS(processes, n, wt, tat)
    return wt, tat

def findWaitingTimeSJF(processes, n, wt):
    service_time = [0] * n
    service_time[0] = 0
    wt[0] = 0

    for i in range(1, n):
        service_time[i] = service_time[i - 1] + processes[i - 1][1]
        wt[i] = max(0, service_time[i] - processes[i][2])

def findTurnAroundTimeSJF(processes, n, wt, tat):
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

def findavgTimeSJF(processes, n):
    wt = [0] * n
    tat = [0] * n
    findWaitingTimeSJF(processes, n, wt)
    findTurnAroundTimeSJF(processes, n, wt, tat)
    return wt, tat

def findWaitingTimePriority(processes, n, wt):
    wt[0] = 0

    for i in range(1, n):
        wt[i] = 0
        for j in range(i):
            wt[i] += processes[j][1]

def findTurnAroundTimePriority(processes, n, wt, tat):
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

def findavgTimePriority(processes, n):
    wt = [0] * n
    tat = [0] * n
    findWaitingTimePriority(processes, n, wt)
    findTurnAroundTimePriority(processes, n, wt, tat)
    return wt, tat

def findWaitingTimeSRT(processes, n, wt):
    rt = [0] * n
    for i in range(n):
        rt[i] = processes[i][1]
    complete = 0
    t = 0
    minm = 999999999
    short = 0
    check = False

    while complete != n:
        for j in range(n):
            if processes[j][2] <= t and rt[j] < minm and rt[j] > 0:
                minm = rt[j]
                short = j
                check = True
        if not check:
            t += 1
            continue
        rt[short] -= 1
        minm = rt[short]
        if minm == 0:
            minm = 999999999
        if rt[short] == 0:
            complete += 1
            check = False
            fint = t + 1
            wt[short] = fint - processes[short][1] - processes[short][2]
            if wt[short] < 0:
                wt[short] = 0
        t += 1

def findTurnAroundTimeSRT(processes, n, wt, tat):
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

def findavgTimeSRT(processes, n):
    wt = [0] * n
    tat = [0] * n
    findWaitingTimeSRT(processes, n, wt)
    findTurnAroundTimeSRT(processes, n, wt, tat)
    return wt, tat

def round_robin(processes, burst_time, quantum):
    n = len(processes)
    queue = deque()
    waiting_time = [0] * n
    turnaround_time = [0] * n
    remaining_time = list(burst_time)
    time = 0

    while True:
        done = True
        for i in range(n):
            if remaining_time[i] > 0:
                done = False
                if remaining_time[i] > quantum:
                    time += quantum
                    remaining_time[i] -= quantum
                    queue.append(processes[i])
                else:
                    time += remaining_time[i]
                    waiting_time[i] = time - burst_time[i]
                    remaining_time[i] = 0
                    queue.append(processes[i])
                    turnaround_time[i] = time

        if done:
            break

    return waiting_time, turnaround_time

def calculate_averages(waiting_time, turnaround_time):
    n = len(waiting_time)
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return avg_waiting_time, avg_turnaround_time

def run_scheduler():
    quantum = int(quantum_entry.get())
    burst_times = [int(bt.get()) for bt in burst_time_entries]
    priorities = [int(p.get()) for p in priority_entries]

    processes = []
    for i in range(len(burst_times)):
        processes.append([f'P{i + 1}', burst_times[i], priorities[i]])

    # Run the selected scheduling algorithm
    algorithm = algorithm_choice.get()
    if algorithm == 'Round Robin':
        waiting_time, turnaround_time = round_robin(processes, burst_times, quantum)
    elif algorithm == 'FCFS':
        wt, tat = findavgTimeFCFS(processes, len(processes))
        waiting_time, turnaround_time = wt, tat
    elif algorithm == 'SJF':
        wt, tat = findavgTimeSJF(processes, len(processes))
        waiting_time, turnaround_time = wt, tat
    elif algorithm == 'Priority':
        wt, tat = findavgTimePriority(processes, len(processes))
        waiting_time, turnaround_time = wt, tat
    elif algorithm == 'SRT':
        wt, tat = findavgTimeSRT(processes, len(processes))
        waiting_time, turnaround_time = wt, tat
    else:
        # Handle unsupported algorithm
        waiting_time, turnaround_time = [], []

    avg_waiting, avg_turnaround = calculate_averages(waiting_time, turnaround_time)

    result_label.config(text=f"Average Waiting Time: {avg_waiting:.2f}\nAverage Turnaround Time: {avg_turnaround:.2f}")

root = tk.Tk()
root.title("Process Scheduling")

# Create and arrange input fields (quantum, burst times, priorities)
quantum_label = tk.Label(root, text="Quantum:")
quantum_label.pack()
quantum_entry = tk.Entry(root)
quantum_entry.pack()

burst_time_labels = []
burst_time_entries = []
priority_labels = []
priority_entries = []

for i in range(5):
    burst_time_labels.append(tk.Label(root, text=f"Burst Time for P{i + 1}:"))
    burst_time_labels[i].pack()
    burst_time_entries.append(tk.Entry(root))
    burst_time_entries[i].pack()

for i in range(5):
    priority_labels.append(tk.Label(root, text=f"Priority for P{i + 1}:"))
    priority_labels[i].pack()
    priority_entries.append(tk.Entry(root))
    priority_entries[i].pack()

# Add a dropdown for selecting the scheduling algorithm
algorithm_label = tk.Label(root, text="Select Scheduling Algorithm:")
algorithm_label.pack()
algorithm_choice = ttk.Combobox(root, values=['Round Robin', 'FCFS', 'SJF', 'Priority', 'SRT'])
algorithm_choice.pack()
algorithm_choice.set('Round Robin')

# Create a button to run the scheduler
run_button = tk.Button(root, text="Run Scheduler", command=run_scheduler)
run_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
