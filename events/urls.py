from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.event_Overviews , name="home") ,
    path('names/' , views.view_event , name="view_event_list"),
    path('names/<int:id>/' , views.view_event , name="view_event_detail"),
    path('create/' , views.create_event , name="create_event"),
    path('<int:event_id>/update' , views.update_event , name="update_evet"),
    path('<int:event_id>/delete' , views.delete_event , name="delete_event"),
]
