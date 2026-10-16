from django.urls import path
from . import views


app_name = "attendance"


urlpatterns = [

    path(
        "",
        views.session_list,
        name="session_list"
    ),

    path(
        "report/",
        views.attendance_report,
        name="report"
    ),

    path(
        "session/<int:session_id>/",
        views.take_attendance,
        name="take_attendance"
    ),

]