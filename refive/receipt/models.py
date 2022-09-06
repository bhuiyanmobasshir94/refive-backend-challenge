import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

ALLOWED_TXT_EXTENSIONS = ["txt"]
ALLOWED_PDF_EXTENSIONS = ["pdf"]


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Receipt(BaseModel):
    receipt = models.FileField(
        upload_to="receipt/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_TXT_EXTENSIONS)],
        verbose_name=_("Receipt"),
    )
    marked_pdf = models.FileField(
        upload_to="marked-pdf/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_PDF_EXTENSIONS)],
        verbose_name=_("Marked PDF"),
        null=True,
        blank=True,
    )
    text_clusters = models.TextField(
        verbose_name=_("Text Clusters"), null=True, blank=True
    )
    bbox_clusters = models.TextField(
        verbose_name=_("Bbox Clusters"), null=True, blank=True
    )
    blocks = models.TextField(verbose_name=_("Blocks"), null=True, blank=True)

    def __str__(self):
        return self.receipt.name
