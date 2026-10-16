from django.shortcuts import render

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from academics.models import Enrollment
from .models import ClassSession, AttendanceRecord


# ==========================================
# ATTENDANCE DASHBOARD
# ==========================================

@staff_member_required
def session_list(request):

    sessions = ClassSession.objects.select_related(
        "subject"
    ).order_by(
        "-session_date",
        "start_time"
    )

    return render(
        request,
        "attendance/session_list.html",
        {
            "sessions": sessions,
        }
    )


# ==========================================
# TAKE ATTENDANCE
# ==========================================

@staff_member_required
def take_attendance(request, session_id):

    session = get_object_or_404(
        ClassSession.objects.select_related("subject"),
        pk=session_id
    )

    enrollments = list(
        Enrollment.objects.filter(
            subject=session.subject,
            academic_year=session.academic_year,
            status="enrolled"
        ).select_related(
            "student"
        ).order_by(
            "student__student_id"
        )
    )

    # Find attendance records already saved for this session.
    existing_records = {
        record.student_id: record
        for record in AttendanceRecord.objects.filter(
            class_session=session
        )
    }

    # Display previously saved statuses when reopening the page.
    for enrollment in enrollments:
        record = existing_records.get(enrollment.student_id)

        enrollment.current_status = (
            record.status if record else ""
        )

    allowed_statuses = {
        value
        for value, label in AttendanceRecord.STATUS_CHOICES
    }

    if request.method == "POST":

        if not enrollments:
            messages.error(
                request,
                "No students are enrolled in this subject "
                "for this academic year."
            )

            return redirect(
                "attendance:take_attendance",
                session_id=session.pk
            )

        submitted_statuses = {}

        # Validate every student's attendance before saving.
        for enrollment in enrollments:

            student_pk = enrollment.student.pk

            status = request.POST.get(
                f"status_{student_pk}",
                ""
            )

            if status not in allowed_statuses:

                messages.error(
                    request,
                    "Please select a valid attendance status "
                    "for every student."
                )

                return render(
                    request,
                    "attendance/take_attendance.html",
                    {
                        "session": session,
                        "enrollments": enrollments,
                    }
                )

            submitted_statuses[student_pk] = status

        # Save all records together.
        with transaction.atomic():

            for enrollment in enrollments:

                student_pk = enrollment.student.pk

                AttendanceRecord.objects.update_or_create(
                    class_session=session,
                    student=enrollment.student,
                    defaults={
                        "status": submitted_statuses[student_pk],
                        "recording_method": "manual",
                    }
                )

        messages.success(
            request,
            f"Attendance saved successfully for "
            f"{len(enrollments)} students."
        )

        return redirect(
            "attendance:take_attendance",
            session_id=session.pk
        )

    return render(
        request,
        "attendance/take_attendance.html",
        {
            "session": session,
            "enrollments": enrollments,
        }
    )
# ==========================================
# ATTENDANCE REPORT
# ==========================================

@staff_member_required
def attendance_report(request):

    # Get all active student enrollments.
    enrollments = Enrollment.objects.filter(
        status="enrolled"
    ).select_related(
        "student",
        "subject"
    ).order_by(
        "student__student_id",
        "subject__subject_code"
    )

    report_rows = []

    # Calculate attendance separately for every
    # student-subject enrollment.
    for enrollment in enrollments:

        records = AttendanceRecord.objects.filter(
            student=enrollment.student,
            class_session__subject=enrollment.subject,
            class_session__academic_year=enrollment.academic_year
        ).exclude(
            status="excused"
        )

        total_classes = records.count()

        attended_classes = records.filter(
            status__in=["present", "late"]
        ).count()

        if total_classes > 0:
            percentage = round(
                attended_classes / total_classes * 100,
                2
            )
        else:
            percentage = None

        report_rows.append({
            "student_id": enrollment.student.student_id,
            "student_name": enrollment.student.full_name,
            "subject_code": enrollment.subject.subject_code,
            "subject_name": enrollment.subject.subject_name,
            "academic_year": enrollment.academic_year,
            "attended_classes": attended_classes,
            "total_classes": total_classes,
            "percentage": percentage,
        })

    return render(
        request,
        "attendance/attendance_report.html",
        {
            "report_rows": report_rows,
        }
    )