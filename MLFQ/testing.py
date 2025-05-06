import random
from MLFQ import Process, MLFQ

def generate_processes(num_processes):
    processes = []
    for pid in range(1, num_processes + 1):
        arrival = random.randint(0, 50)  # Random arrival time
        burst = random.randint(1, 10)     # Random burst time
        processes.append(Process(pid, arrival, burst))
    return processes

def main():

    processes = generate_processes(10)



if __name__ == "__main__":
    main()