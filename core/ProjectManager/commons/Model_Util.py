from re import T
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _

class BaseModelQuerySet(models.QuerySet):

    def delete(self):
        return self.update(
                is_deleted = True,
                deleted_at = timezone.now(),
        )


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return BaseModelQuerySet(self.model, self._db).filter(is_deleted=False)

class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    is_deleted = models.BooleanField(null=True, blank=True, editable=False, verbose_name=_("Is deleted"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Deleted at"))

    objects = BaseModelManager

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

