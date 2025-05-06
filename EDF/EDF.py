import heapq

class Task:
    _pid_counter = 1

    def __init__(self, execution_time, deadline, arrival_time):
        self.pid = Task._pid_counter
        Task._pid_counter += 1

        self.execution_time = execution_time  # burst time
        self.deadline = deadline
        self.arrival_time = arrival_time

        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def __lt__(self, other):
        return self.deadline < other.deadline

class EDFScheduler:
    def __init__(self):
        self.time = 0
        self.task_queue = []
        self.completed_tasks = []

    def add_task(self, task):
        heapq.heappush(self.task_queue, task)

    def run(self, tasks, max_time):
        tasks.sort(key=lambda x: x.arrival_time)

        while self.time < max_time:
            while tasks and tasks[0].arrival_time <= self.time:
                self.add_task(tasks.pop(0))

            if self.task_queue:
                current_task = heapq.heappop(self.task_queue)

                start_time = self.time
                self.time += current_task.execution_time
                current_task.completion_time = self.time
                current_task.turnaround_time = current_task.completion_time - current_task.arrival_time
                current_task.waiting_time = current_task.turnaround_time - current_task.execution_time

                self.completed_tasks.append(current_task)
            else:
                if tasks:
                    self.time = tasks[0].arrival_time
                else:
                    break

        self.display_results()

    def display_results(self):
        print("\nPID | Arrival | Burst | Deadline | Completion | Turnaround | Waiting")
        print("----------------------------------------------------------------------")
        for t in sorted(self.completed_tasks, key=lambda x: x.pid):
            print(f"{t.pid:3} | {t.arrival_time:7} | {t.execution_time:5} | {t.deadline:8} |"
                  f" {t.completion_time:10} | {t.turnaround_time:10} | {t.waiting_time:7}")

# Test tasks
tasks = [
    Task(2, 6, 0),
    Task(3, 5, 1),
    Task(1, 4, 2),
    Task(4, 7, 3),
    Task(2, 8, 4),
    Task(1, 9, 5)
]

scheduler = EDFScheduler()
scheduler.run(tasks, max_time=20)