from django.urls import path
from . import views

urlpatterns = [
    path('airports/<str:airport_id>/', views.airport_view, name='airport_details'),
    path('countries/<str:iso_country>/', views.country_view, name='country_details'),
    path('navaids/<str:navaid_id>/', views.navaid_view, name='navaid_details'),
    path('regions/<str:region_id>/', views.region_view, name='region_details'),
    path('runways/<str:runway_id>/', views.runway_view, name='runway_details'),
    path('results/', views.results_view, name='results'),
]
