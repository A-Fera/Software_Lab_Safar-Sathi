from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.AccommodationListView.as_view(), name='accommodation_list'),
    path('accommodation/<int:pk>/', views.accommodation_detail_view, name='accommodation_detail'),
    path('accommodation/create/', views.accommodation_create_view, name='accommodation_create'),
    path('accommodation/<int:pk>/edit/', views.accommodation_update_view, name='accommodation_update'),
    path('accommodation/<int:pk>/delete/', views.accommodation_delete_view, name='accommodation_delete'),
    path('accommodation/<int:accommodation_pk>/book/', views.booking_create_view, name='booking_create'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('booking/<int:booking_pk>/pay/', views.payment_create_view, name='payment_create'),
    path('booking/<int:pk>/cancel/', views.booking_cancel_view, name='booking_cancel'),
]
