from django.db import models
from django.db.models import Manager
from commons.ModelUtil import BaseModel
from user.models import User

class Project(BaseModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(to= User, on_delete=models.PROTECT, related_name="projects")


    def __str__(self) -> str:
        return self.title


class ProjectRecycle(Project):

    deleted = Manager()

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return super().title


class Task(BaseModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(to= Project, on_delete=models.CASCADE, related_name="tasks")


    def __str__(self) -> str:
        return self.title


class TaskRecycle(Task):

    deleted = Manager()

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return super().title




class AssignTask(BaseModel):
    user = models.ForeignKey(to= User, on_delete=models.CASCADE, related_name="assined_task")
    task = models.ForeignKey(to= Task, on_delete=models.CASCADE, related_name="assined_task")


    def __str__(self) -> str:
        return self.task.title


class AssignTaskRecycle(AssignTask):

    deleted = Manager()

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return super().task.title

