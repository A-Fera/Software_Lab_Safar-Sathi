from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('destination/<int:destination_id>/', views.destination_review_view, name='destination_review'),
    path('destination/<int:destination_id>/all/', views.destination_review_list_view, name='destination_review_list'),
    path('accommodation/<int:accommodation_id>/', views.accommodation_review_view, name='accommodation_review'),
    path('accommodation/<int:accommodation_id>/all/', views.accommodation_review_list_view, name='accommodation_review_list'),
    path('guide/<int:guide_id>/', views.guide_review_view, name='guide_review'),
]
