from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.__repr__()
