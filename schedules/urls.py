from django.urls import path
from . import views

app_name = 'schedules'
urlpatterns = [
    path('', views.index, name='index'),
    path('student/', views.students, name='students'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('register/', views.register, name='register'),
    path('class/', views.classes, name='classes'),
    path('class/<str:class_id>/', views.class_detail, name='class_detail'),
    path('class/<str:class_id>/<int:group_number>/', views.group_detail, name='group_detail'),
]
