from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    # صفحة تسجيل الدخول
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # لوحة تحكم الكيان
    path('entity/dashboard/', views.entity_dashboard, name='entity_dashboard'),
    path('entity/add-candidate/', views.add_candidate, name='add_candidate'),
    path('entity/add-voters/', views.add_voters_to_entity, name='add_voters_to_entity'),
    path('entity/upload-excel/', views.upload_excel_entity, name='upload_excel_entity'),
    
    # لوحة تحكم المرشح
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('candidate/add-pillar/', views.add_pillar, name='add_pillar'),
    path('candidate/add-voters/', views.add_voters_to_candidate, name='add_voters_to_candidate'),
    path('candidate/upload-excel/', views.upload_excel_candidate, name='upload_excel_candidate'),
    
    # لوحة تحكم الركيزة
    path('pillar/dashboard/', views.pillar_dashboard, name='pillar_dashboard'),
    path('pillar/add-voter/', views.add_voter, name='add_voter'),

    path('pillar/update-voter-status/<int:voter_id>/', views.update_voter_status, name='update_voter_status'),
    
    # لوحة تحكم الإدارة
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create-entity/', views.create_entity, name='create_entity'),
    path('admin/create-candidate/', views.create_candidate, name='create_candidate'),
    path('admin/manage-entities/', views.manage_entities, name='manage_entities'),
    path('admin/manage-candidates/', views.manage_candidates, name='manage_candidates'),
    path('admin/edit-entity/<int:entity_id>/', views.edit_entity, name='edit_entity'),
    path('admin/delete-entity/<int:entity_id>/', views.delete_entity, name='delete_entity'),
    path('admin/edit-candidate/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('admin/delete-candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('admin/appearance-settings/', views.appearance_settings, name='appearance_settings'),
    
    # صفحة تفاصيل الإحصائيات
    path('statistics/<str:stat_type>/', views.statistics_detail, name='statistics_detail'),
    
    # API endpoints
    path('api/get-voter-stats/', views.get_voter_stats, name='get_voter_stats'),
    path('get-pillars/<int:candidate_id>/', views.get_pillars_for_candidate, name='get_pillars_for_candidate'),
]