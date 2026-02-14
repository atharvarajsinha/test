from django.db import models


class CompilationRecord(models.Model):
    source_code = models.TextField()
    source_language = models.CharField(max_length=16)
    target_language = models.CharField(max_length=16)
    tokens_file_path = models.CharField(max_length=512)
    ast_file_path = models.CharField(max_length=512)
    ir_file_path = models.CharField(max_length=512)
    converted_code = models.TextField()
    original_output = models.TextField(blank=True)
    converted_output = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_language}->{self.target_language} @ {self.timestamp.isoformat()}"
