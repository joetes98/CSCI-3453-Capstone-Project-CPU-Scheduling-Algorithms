import random

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.queueLevel = 0
        self.completion = None
        self.completed = False


class MLFQ:
    def __init__(self, processes, Q0, Q1):
        self.processes = processes
        self.Q0 = Q0
        self.Q1 = Q1

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
        
        # while there are processes in the queues or there are processes yet to arrive
        while queue0 or queue1 or queue2 or any(p.remaining > 0 for p in self.processes):
            # Add processes to queue 0 if they have arrived
            for process in self.processes:
                if process.arrival <= current_time and process.remaining > 0 and process not in queue0 + queue1 + queue2:
                    queue0.append(process)

            # check queue 0 (highest priority)
            if queue0:
                process = queue0.pop(0)
                time_slice = min(self.Q0, process.remaining)
                for _ in range(time_slice):
                    current_time += 1
                    process.remaining -= 1

                    # Add new processes to queue 0 if they arrive
                    for new_process in self.processes:
                        if (new_process.arrival == current_time and new_process.remaining > 0 and new_process not in queue0 + queue1 + queue2):
                            queue0.append(new_process)
                            
                
                if process.remaining > 0:
                    queue1.append(process)
                    process.queueLevel = 1
                else:
                    process.completion = current_time
                    process.completed = True
                    processed.append(process)
                    process.queueLevel = -1
                # continue
            
            # Check queue 1
            elif queue1:
                process = queue1.pop(0)
                time_slice = min(self.Q1, process.remaining)
                preempted = False
                for _ in range(time_slice):
                    current_time += 1
                    process.remaining -= 1

                    # Check for preemption (process arrived in queue 0)
                    for new_process in self.processes:
                        if new_process.arrival == current_time and new_process.remaining > 0 and new_process not in queue0 + queue1 + queue2:
                            queue0.append(new_process)
                            queue0.sort(key=lambda x: x.arrival)  # Order by arrival
                            queue1.insert(0, process)  # Place current process at the front of queue1
                            preempted = True
                            break
                    if preempted:
                        break
                if preempted:
                    continue
                
                if process.remaining > 0:
                    queue2.append(process)
                    process.queueLevel = 2
                else:
                    process.completion = current_time
                    process.completed = True
                    processed.append(process)
                    process.queueLevel = -1
                # continue

            # Check queue 2 (lowest priority)
            elif queue2:
                process = queue2.pop(0)
                preempted = False
                # Run process until completion (FCFS)
                while process.remaining > 0:
                    current_time += 1
                    process.remaining -= 1

                    # Check for preemption
                    for new_process in self.processes:
                        if new_process.arrival == current_time and new_process.remaining > 0 and new_process not in queue0 + queue1 + queue2:
                            queue0.append(new_process)
                            queue0.sort(key=lambda x: x.arrival)  # Order by arrival
                            queue2.insert(0, process)  # Place current process at the front of queue2
                            preempted = True
                            break
                    if preempted:
                        break
                if preempted:
                    continue
                
                # Process completed
                process.completion = current_time
                process.completed = True
                processed.append(process)
                process.queueLevel = -1
                # continue
            
            # all queues are empty, find the next process to arrive
            else:
                next_process = min((p.arrival for p in self.processes if p.remaining > 0 and p.arrival > current_time), default=None)
                if next_process is not None:
                    current_time = next_process
                else:
                    break # Exit loop if CPU idle
        
        return processed
    
def generate_processes(num_processes):
    processes = []
    for pid in range(1, num_processes + 1):
        arrival = random.randint(0, 10)  # Random arrival time
        burst = random.randint(1, 10)     # Random burst time
        processes.append(Process(pid, arrival, burst))
    return processes

def main():

    # Define time slices for each queue
    Q0 = 2
    Q1 = 4

    # initialize overall metrics
    total_turnaround = 0
    total_waiting = 0
    total_throughput = 0
    total_cpu_utilization = 0
    num_simulations = 10

    for _ in range(1, num_simulations + 1):

        # Generate random processes
        processes = generate_processes(10)

        # Create an MLFQ scheduler
        scheduler = MLFQ(processes, Q0, Q1)

        # Run the scheduler
        processed = scheduler.schedule()
    
        turnaround = 0
        waiting = 0

        # Print results
        print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Completion':<15}{'Turnaround':<15}{'Waiting':<10}")
        print("-"*65)
        for p in processed:
            turnaround_time = p.completion - p.arrival
            turnaround += turnaround_time
            waiting_time = turnaround_time - p.burst
            waiting += waiting_time
            # display details
            print(f"{p.pid:<5}{p.arrival:<10}{p.burst:<10}{p.completion:<15}{turnaround_time:<15}{waiting_time:<10}")

        avg_turnaround = turnaround /len(processes)
        avg_waiting = waiting /len(processes)

        # total_completion_time = sum(p.completion for p in processed)
        total_execution_time = sum(p.burst for p in processed)

        throughput = len(processed)/max(p.completion for p in processed)
        cpu_utilization = (total_execution_time/(max(p.completion for p in processed) - min(p.arrival for p in processed)))*100

        # Metrics
        total_turnaround += avg_turnaround
        total_waiting += avg_waiting
        total_throughput += throughput
        total_cpu_utilization += cpu_utilization

    

        print("\nSummary:")
        print(f"\nAverage Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time: {avg_waiting:.2f}")
        print(f"Throughput: {throughput:.2f} processes/unit")
        print(f"CPU Utilization: {cpu_utilization:.2f}%")

    # Overall Average Metrics
    overall_avg_turnaround = total_turnaround/num_simulations
    overall_avg_waiting = total_waiting/num_simulations
    overall_avg_throughput = total_throughput/num_simulations
    overall_avg_cpu_utilization = total_cpu_utilization/num_simulations

    # Print overall summary
    print("\nOverall Summary (Across All Simulations):")
    print("="*50)
    print(f"Average Turnaround Time: {overall_avg_turnaround:.2f}")
    print(f"Average Waiting Time: {overall_avg_waiting:.2f}")
    print(f"Average Throughput: {overall_avg_throughput:.2f} processes/unit")
    print(f"Average CPU Utilization: {overall_avg_cpu_utilization:.2f}%")


if __name__ == '__main__':
    main()