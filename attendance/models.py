from django.db import models

# Create your mfrom django.db import models


# ==========================================
# CLASS SESSION MODEL
# ==========================================

class ClassSession(models.Model):

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.PROTECT,
        related_name="class_sessions"
    )

    session_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField(
        null=True,
        blank=True
    )

    academic_year = models.CharField(
        max_length=9,
        default="2026-2027"
    )

    topic = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-session_date", "start_time"]

    def __str__(self):
        return (
            f"{self.subject.subject_code} - "
            f"{self.session_date} "
            f"({self.start_time})"
        )


# ==========================================
# ATTENDANCE RECORD MODEL
# ==========================================

class AttendanceRecord(models.Model):

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    ]

    METHOD_CHOICES = [
        ("manual", "Manual"),
        ("rfid", "RFID"),
        ("biometric", "Biometric"),
    ]

    class_session = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="attendance_records"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="absent"
    )

    recording_method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES,
        default="manual"
    )

    remarks = models.CharField(
        max_length=200,
        blank=True
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["class_session", "student"],
                name="uniq_attend_student_session"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.class_session} - "
            f"{self.get_status_display()}"
        )
