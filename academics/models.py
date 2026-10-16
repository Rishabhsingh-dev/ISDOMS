from django.db import models
from students.models import Student


# ==========================================
# SUBJECT MODEL
# ==========================================

class Subject(models.Model):

    subject_code = models.CharField(
        max_length=20,
        unique=True
    )

    subject_name = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100
    )

    semester = models.PositiveSmallIntegerField()

    credits = models.PositiveSmallIntegerField(
        default=3
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


# ==========================================
# ENROLLMENT MODEL
# ==========================================

class Enrollment(models.Model):

    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name='enrollments'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name='enrollments'
    )

    academic_year = models.CharField(
        max_length=9,
        default='2026-2027'
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='enrolled'
    )

    enrolled_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'student',
                    'subject',
                    'academic_year'
                ],
                name='unique_student_subject_year'
            )
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.subject.subject_code} "
            f"({self.academic_year})"
        )
