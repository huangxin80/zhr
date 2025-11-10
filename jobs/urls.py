from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # 兼职列表和详情
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),

    # 发布和管理兼职
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('<int:pk>/close/', views.job_close, name='job_close'),

    # 申请兼职
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),

    # 个人中心
    path('my/published/', views.my_published, name='my_published'),
    path('my/applications/', views.my_applications, name='my_applications'),

    # 管理申请
    path('<int:pk>/applications/', views.manage_applications, name='manage_applications'),
    path('application/<int:pk>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('application/<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
    path('application/<int:pk>/complete/', views.complete_application, name='complete_application'),
]
