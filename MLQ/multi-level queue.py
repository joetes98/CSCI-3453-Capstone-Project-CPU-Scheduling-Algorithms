# Define the Process class to represent each CPU task
class Process:
    def __init__(self, pid, priority, burst_time, queue_level, arrival_time):
        self.pid = pid                      # Unique process ID
        self.priority = priority            # Priority level
        self.burst_time = burst_time        # Total CPU time the process needs
        self.queue_level = queue_level      # Queue level the process is assigned to (0–4)
        self.arrival_time = arrival_time    # Time when the process enters the system
        self.waiting_time = 0               # Time spent waiting in the queue
        self.turnaround_time = 0            # Total time from arrival to completion

# Generate a list of random processes
def generate_processes(num_processes=10):
    processes = []
    for i in range(num_processes):
        pid = i + 1
        priority = random.randint(1, 10)         # Random priority 
        burst_time = random.randint(1, 10)       # Random burst time between 1 and 10
        queue_level = random.randint(0, 4)       # Assign to one of 5 queue levels
        arrival_time = random.randint(0, 10)     # Random arrival time between 0 and 10
        processes.append(Process(pid, priority, burst_time, queue_level, arrival_time))
    return processes

# Organize processes into queues based on their queue_level
def organize_into_queues(processes):
    queues = [[] for _ in range(5)]  # Initialize 5 queues (levels 0 to 4)
    for process in processes:
        queues[process.queue_level].append(process)
    # Sort each queue by arrival time to simulate realistic entry order
    for queue in queues:
        queue.sort(key=lambda p: p.arrival_time)
    return queues

# Simulate Multi-Level Queue Scheduling
def multilevel_queue_scheduling(queues):
    current_time = 0
    all_processes = []
    for level, queue in enumerate(queues):         # Process each queue level in order
        for process in queue:
            if current_time < process.arrival_time:
                current_time = process.arrival_time  # If CPU is idle, advance to arrival time
            process.waiting_time = current_time - process.arrival_time
            current_time += process.burst_time
            process.turnaround_time = current_time - process.arrival_time
            all_processes.append(process)           # Track all processes after execution
    return all_processes, current_time

# Main function to run 10 scheduling simulations with 10 processes each
def main():
    # Initialize accumulators for overall averages
    total_waiting_time = 0
    total_turnaround_time = 0
    total_cpu_utilization = 0
    total_throughput = 0
    num_runs = 10              # Number of simulation iterations
    num_processes = 10         # Number of processes per run

    for i in range(num_runs):
        print(f"\n--- Simulation Run {i+1} ---")
        processes = generate_processes(num_processes)             # Generate 10 processes
        queues = organize_into_queues(processes)                  # Sort them into queues
        finished_processes, total_time = multilevel_queue_scheduling(queues)  # Schedule them

        # Calculate metrics for this run
        average_waiting_time = sum(p.waiting_time for p in finished_processes) / len(finished_processes)
        average_turnaround_time = sum(p.turnaround_time for p in finished_processes) / len(finished_processes)
        cpu_utilization = (sum(p.burst_time for p in finished_processes) / total_time) * 100
        throughput = len(finished_processes) / total_time         # Completed processes per time unit

        # Accumulate totals for overall averages
        total_waiting_time += average_waiting_time
        total_turnaround_time += average_turnaround_time
        total_cpu_utilization += cpu_utilization
        total_throughput += throughput

        # Print metrics for this simulation run
        print(f"Average Waiting Time: {average_waiting_time:.2f}")
        print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
        print(f"CPU Utilization: {cpu_utilization:.2f}%")
        print(f"Throughput: {throughput:.4f} processes per time unit")

    # Display average metrics across all runs
    print("\n=== Overall Averages Across 10 Runs ===")
    print(f"Average Waiting Time: {total_waiting_time / num_runs:.2f}")
    print(f"Average Turnaround Time: {total_turnaround_time / num_runs:.2f}")
    print(f"Average CPU Utilization: {total_cpu_utilization / num_runs:.2f}%")
    print(f"Average Throughput: {total_throughput / num_runs:.4f} processes per time unit")

# Run the program
if __name__ == "__main__":
    main()