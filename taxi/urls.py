from django.urls import path
from . import views

app_name = "taxi"

urlpatterns = [
    path("", views.index, name="index"),
    path("cars/", views.CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", views.CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", views.CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", views.CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", views.CarDeleteView.as_view(), name="car-delete"),
    path("drivers/", views.DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/", views.DriverDetailView.as_view(), name="driver-detail"),
    path("drivers/create/", views.DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/license/", views.DriverLicenseUpdateView.as_view(), name="driver-license-update"),
    path("drivers/<int:pk>/delete/", views.DriverDeleteView.as_view(), name="driver-delete"),
]
