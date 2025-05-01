import random
from MLFQ import MLFQ, Process


def generate_processes(num_processes):
    processes = []
    for pid in range(1, num_processes + 1):
        arrival = random.randint(0, 50)  # Random arrival time
        burst = random.randint(1, 10)     # Random burst time
        processes.append(Process(pid, arrival, burst))
    return processes

def main():

    # Define time slices for each queue
    Q0 = 4
    Q1 = 8

    # initialize overall metrics
    total_turnaround = 0
    total_waiting = 0
    total_throughput = 0
    total_cpu_utilization = 0
    num_simulations = 10

    for x in range(1, num_simulations + 1):

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

        total_completion_time = sum(p.completion for p in processed)
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