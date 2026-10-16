from django.db import models

# Create your modfrom django.db import models


class Student(models.Model):

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100
    )

    semester = models.PositiveSmallIntegerField()

    section = models.CharField(
        max_length=10,
        default="A"
    )

    email = models.EmailField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
