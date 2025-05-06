import math
import random

#Hunter Tanksley
#Rate Monotonic Scheduling

class Ratemonotonic:
    def __init__(self, taskId, executionTime, period):
        self.taskId = taskId
        self.executionTime = executionTime
        self.period = period
        self.remainingTime = executionTime
        self.nextDeadline = period
        self.completionTimes = []
        self.burstTimes = 0
        self.waitingTimes = 0
        self.turnaroundTimes = 0
        
    
    def RMS(tasks, simulationTime):
        tasks.sort(key=lambda x: x.period)  # Sort tasks by period
        time = 0
        schedule = []
        cpuBusyTime = 0
        tt = 0

        while time < simulationTime:
            # Find the task with the shortest period
            runnableTasks=[task for task in tasks if task.remainingTime > 0 and time < task.nextDeadline]
            if runnableTasks:
                currentTask = min(runnableTasks, key=lambda x: x.period) # Select the task with the shortest period
                schedule.append((time, currentTask.taskId)) 
                currentTask.remainingTime -= 1 # Execute the task
                cpuBusyTime += 1 # CPU busy time

                if currentTask.remainingTime == 0:
                    currentTask.completionTimes.append(time + 1) # Task completed
                    tt = (time + 1) - (currentTask.nextDeadline - currentTask.period)
                    currentTask.turnaroundTimes += tt
                    currentTask.burstTimes += currentTask.executionTime # Turnaround time
            else:
                schedule.append((time, "Idle")) # CPU idle time
                
            time += 1
            for task in tasks:
                if time == task.nextDeadline:
                    if task.remainingTime > 0:
                        print(f"Task {task.taskId} missed its deadline at time {time}.") # Missed deadline
                    task.remainingTime = task.executionTime # Reset remaining time
                    task.nextDeadline += task.period # Update next deadline

        totalTasksCompleted = 0
        totalTurnaroundTime = 0
        totalWaitingTime = 0
        tt=0

        for task in tasks:
            if task.completionTimes:
                tt = task.turnaroundTimes # Turnaround time for each task execution
                task.waitingTimes = tt - task.burstTimes # Waiting time for each task
                totalTurnaroundTime += tt # Total turnaround time among each execution
                totalWaitingTime += task.waitingTimes # Total waiting time among each execution
                totalTasksCompleted += len(task.completionTimes) # Total tasks completed for a task

        avgTurnaroundTime = totalTurnaroundTime / totalTasksCompleted if totalTasksCompleted > 0 else 0 # Average turnaround time
        avgWaitingTime = totalWaitingTime / totalTasksCompleted if totalTasksCompleted > 0 else 0 # Average waiting time
        throughput = totalTasksCompleted / simulationTime # Throughput
        cpuUtilization = cpuBusyTime / simulationTime * 100 # CPU utilization

        print("\nAverage Metrics:")
        print(f"Average Turnaround Time: {avgTurnaroundTime:.2f}")
        print(f"Average Waiting Time: {avgWaitingTime:.2f}")
        print(f"Throughput: {throughput:.4f} tasks/unit time")
        print(f"CPU Utilization: {cpuUtilization:.2f}%\n")

        return schedule, totalTurnaroundTime, totalWaitingTime, throughput, cpuUtilization # Return the metrics
    
    
if __name__ == "__main__":
    tasks = [] 
    cpuU = 0 #keeps track of CPU utilization
    turnaround = 0 #keeps track of turnaround time
    waiting = 0 #keeps track of waiting time
    throughput = 0 #keeps track of throughput
    tCU = 0 #keeps track of CPU utilization for all cases
    tTT = 0 #keeps track of turnaround time for all cases
    tWT = 0 #keeps track of waiting time for all cases
    tTP = 0 #keeps track of throughput for all cases

    for i in range(10): # 10 cases
        print(f"=====Case {i+1}=====")
        for j in range(10): # 3 tasks
            # Randomly generate task parameters
            taskId = f"T{j+1}"
            executionTime = random.randint(1, 9)
            period = random.randint(15, 25)
            tasks.append(Ratemonotonic(taskId, executionTime, period))
            print(f"Task: {taskId}, Execution Time: {executionTime}, Period: {period}")
        simTime = 30    # Randomly generate simulation time
        print(f"\nSimulation Time: {simTime}\n")
        schedule, turnaround, waiting, throughput, cpuU = Ratemonotonic.RMS(tasks, simTime) # Call the RMS method
        print("Time | Task ID")
        print("---------------------")
        for time, taskId in schedule: # Print the schedule
            print(f"{time:4} | {taskId}")
        print("\n=========================\n")
        tCU += cpuU # Add CPU utilization to the total
        tTT += turnaround # Add turnaround time to the total
        tWT += waiting # Add waiting time to the total
        tTP += throughput # Add throughput to the total
        tasks.clear() # Clear the tasks for the next case

    # Calculate the average metrics for all cases
    cpuU = tCU / 10
    turnaround = tTT / 10
    waiting = tWT / 10
    throughput = tTP / 10

    print("\n=====Overall Average Metrics Among 10 Cases=====\n")
    print(f"Average CPU Utilization: {cpuU:.2f}%")
    print(f"Average Turnaround Time: {turnaround:.2f}")
    print(f"Average Waiting Time: {waiting:.2f}")
    print(f"Average Throughput: {throughput:.4f} processes/time unit")
    print("\n=========================\n")
