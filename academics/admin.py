
from django.contrib import admin
from .models import Subject, Enrollment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        'subject_code',
        'subject_name',
        'department',
        'semester',
        'credits',
        'is_active',
    )

    search_fields = (
        'subject_code',
        'subject_name',
    )

    list_filter = (
        'department',
        'semester',
        'is_active',
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'subject',
        'academic_year',
        'status',
        'enrolled_on',
    )

    search_fields = (
        'student__student_id',
        'student__full_name',
        'subject__subject_code',
        'subject__subject_name',
    )

    list_filter = (
        'academic_year',
        'status',
    )



