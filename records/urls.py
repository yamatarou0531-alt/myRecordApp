from django.urls import path
from . import views

app_name="sake"

urlpatterns = [
    path("",views.sake_list, name="sake_list"),
    path("new/", views.sake_create, name="sake_create"),
    path("<int:pk>/",views.sake_detail, name="sake_detail"),
    path("<int:pk>/update/", views.sake_update, name="sake_update"),
    path("<int:pk>/delete/", views.sake_delete, name="sake_delete")
]