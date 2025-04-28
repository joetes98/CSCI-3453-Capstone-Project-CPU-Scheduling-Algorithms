class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.queueLevel = 0
        self.completion = None


class MLFQ:
    def __init__(self, processes, Q0, Q1, Q2):
        self.processes = processes
        self.Q0 = Q0
        self.Q1 = Q1
        self.Q2 = Q2

    def schedule(self):
        # Initialize queues
        queue0 = []
        queue1 = []
        queue2 = []
        processed = []

        # sort processes based on their arrival time
        self.processes.sort(key=lambda x: x.arrival)

        # intialize current time
        current_time = 0
        
        # while there are processes in the queues
        while queue0 or queue1 or queue2 or any(p.arrival > current_time for p in self.processes):
            # Add processes to queue 0 if they have arrived
            for process in self.processes:
                if process.arrival <= current_time and process.remaining > 0 and process not in queue0 + queue1 + queue2:
                    queue0.append(process)

            # check queue 0
            if queue0:
                process = queue0.pop(0)
                if process.remaining > self.Q0:
                    process.remaining -= self.Q0
                    current_time += self.Q0
                    queue1.append(process)
                    process.queueLevel = 1
                else:
                    current_time += process.remaining
                    process.remaining = 0
                    processed.append(process)
                    process.completion = current_time
                    process.queueLevel = -1
            
            # check queue 1
            elif queue1:
                process = queue1.pop(0)
                if process.remaining > self.Q1:
                    process.remaining -= self.Q1
                    current_time += self.Q1
                    queue2.append(process)
                    process.queueLevel = 2
                else:
                    current_time += process.remaining
                    process.remaining = 0
                    processed.append(process)
                    process.completion = current_time
                    process.queueLevel = -1

            # check queue 2
            elif queue2:
                process = queue2.pop(0)
                if process.remaining > self.Q2:
                    process.remaining -= self.Q2
                    current_time += self.Q2
                    queue2.append(process)
                    process.queueLevel = 2
                else:
                    current_time += process.remaining
                    process.remaining = 0
                    processed.append(process)
                    process.completion = current_time
                    process.queueLevel = -1
            
            # all queues are empty, find the next process to arrive
            else:
                next_process = min((p.arrival for p in self.processes if p.arrival > current_time))
                current_time = next_process
        
        return processed


def main():
    # Create 10 processes with varying arrival times and burst times
    # PID, Arrival Time, Burst Time
    processes = [
        Process(1, 0, 8),
        Process(2, 1, 4),
        Process(3, 2, 9),
        Process(4, 3, 5),
        Process(5, 4, 2),
        Process(6, 5, 6),
        Process(7, 6, 3),
        Process(8, 7, 7),
        Process(9, 8, 10),
        Process(10, 9, 1)
    ]

    # Define time slices for each queue
    Q0 = 4
    Q1 = 6
    Q2 = 8

    # Create an MLFQ scheduler
    scheduler = MLFQ(processes, Q0, Q1, Q2)

    # Run the scheduler
    processed = scheduler.schedule()
    
    turnaround = 0
    waiting = 0

    # Print results
    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Completion':<15}{'Turnaround':<15}{'Waiting':<10}")
    print("-" * 65)
    for p in processed:
        turnaround_time = p.completion - p.arrival
        turnaround += turnaround_time
        waiting_time = turnaround_time - p.burst
        waiting += waiting_time
        # display details
        print(f"{p.pid:<5}{p.arrival:<10}{p.burst:<10}{p.completion:<15}{turnaround_time:<15}{waiting_time:<10}")

    avg_turnaround = turnaround / len(processes)
    avg_waiting = waiting / len(processes)

    total_completion_time = sum(p.completion for p in processed)
    total_execution_time = sum(p.burst for p in processed)

    throughput = len(processed)/ max(p.completion for p in processed)
    cpu_utilization = (total_execution_time / total_completion_time) * 100

    print("\nSummary:")
    print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Throughput: {throughput:.2f} processes/unit")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")


if __name__ == '__main__':
    main()
