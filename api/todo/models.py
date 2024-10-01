from django.db import models

class Task(models.Model):
    text = models.TextField(verbose_name='Описание задачи', blank=False, null=False)
    is_done = models.BooleanField(default=False, verbose_name='Выполнено')
  
       

