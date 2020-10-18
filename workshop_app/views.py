from django.shortcuts import render, redirect
from .models import Room, Reservation
import datetime


def rooms_view(request):
    rooms = Room.objects.all().order_by('name')
    for room in rooms:
        reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
        room.reserved = datetime.date.today() in reservation_dates
    return render(
                request,
                'workshop_app/rooms.html',
                context={"rooms": rooms}
            )


def add_room_view(request):
    if request.method == 'GET':
        return render(request, 'workshop_app/add_room.html')

    if request.method == 'POST':
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")
        if capacity:
            capacity = int(capacity)
        else:
            capacity = 0
        if projector == "1":
            projector = True
        else:
            projector = False

        if not name:
            return render(
                        request,
                        'workshop_app/add_room.html',
                        context={"error": "Brak nazwy sali"}
                    )

        if Room.objects.filter(name=name).first():
            return render(
                        request,
                        'workshop_app/add_room.html',
                        context={"error": "Sala już istnieje w bazie danych"}
                    )

        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect("rooms")


def delete_room_view(request, id_room):
    room = Room.objects.get(id=id_room)
    room.delete()
    return redirect("rooms")


def modify_room_view(request, id_room):
    room = Room.objects.get(id=id_room)
    if request.method == 'GET':
        return render(
                    request,
                    'workshop_app/modify_room.html',
                    context={"room": room}
                )

    if request.method == 'POST':
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")
        if capacity:
            capacity = int(capacity)
        else:
            capacity = 0
        if projector == "1":
            projector = True
        else:
            projector = False

        if not name:
            return render(
                        request,
                        'workshop_app/modify_room.html',
                        context={"room": room, "error": "Brak nazwy sali"}
                    )

        if name != room.name and Room.objects.filter(name=name).first():
            return render(
                        request,
                        'workshop_app/modify_room.html',
                        context={"error": "Sala już istnieje w bazie danych"}
                    )

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()
        return redirect("rooms")


def reservation_room_view(request, id_room):
    room = Room.objects.get(id=id_room)
    reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
    if request.method == 'GET':
        return render(
                    request,
                    'workshop_app/reservation.html',
                    context={"room": room, "reservations": reservations}
                )

    if request.method == 'POST':
        date = request.POST.get("date-reservation")
        message = request.POST.get("message")
        if Reservation.objects.filter(room=room).filter(date=date):
            return render(
                        request,
                        'workshop_app/reservation.html',
                        context={
                            "room": room,
                            "reservations": reservations,
                            "error": "Sala już zajęta!"
                        }
                    )

        if date < str(datetime.date.today()):
            return render(
                        request,
                        'workshop_app/reservation.html',
                        context={
                            "room": room,
                            "reservations": reservations,
                            "error": "Źle wprowadzona data!"
                        }
                    )

        Reservation.objects.create(room=room, date=date, message=message)
        return redirect("rooms")


def details_room_view(request, id_room):
    room = Room.objects.get(id=id_room)
    reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
    return render(
                request,
                'workshop_app/details_room.html',
                context={"room": room, "reservations": reservations}
            )


def search_room_view(request):
    name = request.GET.get("name")
    capacity = request.GET.get("capacity")
    projector = request.GET.get("projector")
    if name or capacity or projector:
        capacity = int(capacity) if capacity else 0
        projector = True if projector == "1" else False
        rooms = Room.objects.all().order_by('name')
        if projector:
            rooms = rooms.filter(projector=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__icontains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = str(datetime.date.today()) in reservation_dates
        return render(
                    request,
                    'workshop_app/rooms_search.html',
                    context={
                        "rooms": rooms,
                        "form": {"name": name, "capacity": capacity, "projector": projector}
                    }
                )
    else:
        return render(request, 'workshop_app/rooms_search.html')
