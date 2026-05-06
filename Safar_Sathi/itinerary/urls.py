from django.urls import path
from . import views

app_name = 'itinerary'

urlpatterns = [
    path('', views.itinerary_list_view, name='itinerary_list'),
    path('<int:pk>/', views.itinerary_detail_view, name='itinerary_detail'),
    path('create/', views.itinerary_create_view, name='itinerary_create'),
    path('<int:pk>/edit/', views.itinerary_update_view, name='itinerary_update'),
    path('<int:pk>/delete/', views.itinerary_delete_view, name='itinerary_delete'),
    path('<int:itinerary_pk>/items/add/', views.item_create_view, name='item_create'),
    path('<int:itinerary_pk>/items/<int:item_pk>/edit/', views.item_update_view, name='item_update'),
    path('<int:itinerary_pk>/items/<int:item_pk>/delete/', views.item_delete_view, name='item_delete'),
]
