from django.urls import path
from . import views

urlpatterns = [
    path('room-new/', views.add_room_view, name="add-room"),
    path('rooms/', views.rooms_view, name="rooms"),
    path('room-delete/<int:id_room>/', views.delete_room_view, name="delete-room"),
    path('room-modify/<int:id_room>/', views.modify_room_view, name="modify-room"),
    path('room-reservation/<int:id_room>/', views.reservation_room_view, name="reservation-room"),
    path('room/<int:id_room>/', views.details_room_view, name="details-room"),
    path('search/', views.search_room_view, name="rooms-search"),
]