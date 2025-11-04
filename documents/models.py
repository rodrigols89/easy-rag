from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_file_size(value):
    max_size = 50 * 1024 * 1024  # 50 megabytes
    if value.size > max_size:
        raise ValidationError(
            "O arquivo excede o tamanho máximo permitido de 50MB."
        )


def validate_file_extension(value):
    valid_extensions = [".txt", ".pdf", ".docx", ".md"]
    if not any(str(value).lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError(
            "Tipo de arquivo inválido. Use apenas: .txt, .pdf, .docx ou .md."
        )


class File(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.FileField(
        upload_to="uploads/",
        validators=[validate_file_size, validate_file_extension],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} (de {self.user.username})"
