from django.contrib import admin
from .models import ClassSession, AttendanceRecord


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 1

    fields = (
        "student",
        "status",
        "recording_method",
        "remarks",
    )


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "session_date",
        "start_time",
        "academic_year",
        "topic",
    )

    list_filter = (
        "academic_year",
        "session_date",
        "subject",
    )

    search_fields = (
        "subject__subject_code",
        "subject__subject_name",
        "topic",
    )

    date_hierarchy = "session_date"
    list_select_related = ("subject",)
    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "class_session",
        "status",
        "recording_method",
        "recorded_at",
    )

    list_filter = (
        "status",
        "recording_method",
    )

    search_fields = (
        "student__student_id",
        "student__full_name",
        "class_session__subject__subject_code",
    )

    list_select_related = (
        "student",
        "class_session",
        "class_session__subject",
    )