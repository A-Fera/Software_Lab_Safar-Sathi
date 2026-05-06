from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.AccommodationListView.as_view(), name='accommodation_list'),
    path('<int:pk>/', views.accommodation_detail_view, name='accommodation_detail'),
    path('create/', views.accommodation_create_view, name='accommodation_create'),
    path('<int:pk>/edit/', views.accommodation_update_view, name='accommodation_update'),
    path('<int:pk>/delete/', views.accommodation_delete_view, name='accommodation_delete'),
    path('<int:accommodation_pk>/book/', views.booking_create_view, name='booking_create'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('booking/<int:booking_pk>/pay/', views.payment_create_view, name='payment_create'),
    path('booking/<int:pk>/cancel/', views.booking_cancel_view, name='booking_cancel'),
]
