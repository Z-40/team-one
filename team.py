from datetime import datetime
from typing import List


class Milestone:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.achieved = False


class Roadmap:
    def __init__(self, milestones: List[Milestone]):
        self.milestones = milestones
        self.current_milestone = milestones[0]
        self.current_milestone_index = 0

    def change_milestone_order(self, milestone: Milestone, before: Milestone):
        self.milestones.remove(milestone)
        # If `before` is None, append and set current milestone to `milestone`
        if not before:
            self.milestones.append(milestone)
            self.current_milestone = milestone
        else:
            before_index = self.milestones.index(before)
            # We cannot have an achieved milestone before one which has not been achieved
            if not ((before.achieved and milestone.achieved) or
                    (not before.achieved and milestone.achieved)):
                raise Exception("Cannot place before achieved milestone")
            else:
                self.current_milestone_index += 1
                self.milestones.insert(before_index, milestone)

    def achieve_milestone(self):
        self.milestones[self.current_milestone_index].achieved = True
        self.current_milestone = self.milestones[self.current_milestone_index + 1]
        self.current_milestone_index += 1

    def unachieve_milestone(self):
        previous = self.current_milestone.index - 1
        self.milestones[previous].achieved = False
        self.current_milestone = self.milestones[previous]
        self.current_milestone_index = previous


    def delete_milestone(self, milestone: Milestone):
        if self.milestones.index(milestone) < self.current_milestone_index:
            self.current_milestone_index -= 1
        self.milestones.remove(milestone)


class Task:
    def __init__(self, name: str, assignee: str, deadline: datetime, files: List[str], is_urgent=False):
        self.name = name
        self.assignee = assignee
        self.files = files
        self.deadline = deadline
        self.is_urgent = is_urgent
        self.is_complete = False


class Planner:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.deadlines = [(task, task.deadline) for task in self.tasks if task.deadline]
        self.urgent_tasks = [task for task in self.tasks if task.urgent]
        self.completed_tasks = []

    def add_task(self, task: Task):
        if task.is_complete:
            raise AttributeError("Cannot add a task which has already been completed")
        else:
            self.tasks.append(task)
            if task.deadline:
                self.deadlines.append(task.deadline)
            if task.is_urgent:
                self.urgent_tasks.append(task)

    def remove_task(self, task: Task):
        self.tasks.remove(task)


class Member:
    def __init__(self, username: str, planner: Planner):
        self.username = username
        self.planner = planner

    def assign_task(self, task: Task):
        self.planner.add_task(task)

    def remove_assigned_task(self, task: Task):
        self.planner.remove_task(task)


class Project:
    def __init__(self, title, description, team, roadmap):
        self.title = title
        self.description = description
        self.team = team
        self.roadmap = roadmap
