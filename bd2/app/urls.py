from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('workers/', views.WorkerListView.as_view(), name='worker_list'),
    path('workers/<int:pk>/', views.WorkerDetailView.as_view(), name='worker_detail'),
    path('subs/', views.SubListView.as_view(), name='sub_list'),
    path('subs/<int:pk>/', views.SubDetailView.as_view(), name='sub_detail'),
    path('subs/create/', views.SubCreateView.as_view(), name='sub_create'),
    path('subs/<int:pk>/delete', views.SubDeleteView.as_view(), name='sub_delete'),
    path('logs/', views.LogListView.as_view(), name='log_list'),
    path('logs/<int:pk>/', views.LogDetailView.as_view(), name='log_detail'),
]