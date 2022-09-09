from django.db import models
from django.db.models import Manager
from commons.ModelUtil import BaseModel
# Create your models here.


class Project(BaseModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)


    def __str__(self) -> str:
        return self.title


class ProjectRecycle(Project):

    deleted = Manager()

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return self.title


class Task(BaseModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)


    def __str__(self) -> str:
        return self.title


class TaskRecycle(Task):

    deleted = Manager()

    class Meta:
        proxy = True

    def __str__(self) -> str:
        return self.title

