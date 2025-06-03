from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import EventSerializer
from .smart_contract import create_event_on_chain
from .qrcode_generator import generate_event_qr

# Create your views here.
@api_view(['POST'])
def create_event(request):
    """
    Create a new event.
    """

    data = request.data
    serializer = EventSerializer(data=data)

    # Validate the serializer
    if serializer.is_valid():
        # Save the event to the database
        event = serializer.save()

        # Create the event on the blockchain
        try:
            tx_hash = create_event_on_chain(
                title=event.title,
                metadata=event.metadata,
                location=event.location,
                start_time=event.start_time,
                creator=event.creator
            )

            # Generate QR code for the event
            get_event_qrcode(event.id)
            # Update the event with the transaction hash in models
            event.transaction_hash = tx_hash
            event.save()
            return Response({"message": "Event created successfully", "event_id": event.id, "transaction_hash": tx_hash}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_event_qrcode(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found."}, status=404)
    
    # Generate the QR code for the event
    qrcode_data = generate_event_qr(event_id)

    # Return the QR code data
    return Response({
        "event_id": event_id, 
        "qrcode": qrcode_data},
        status=200
    )


@api_view(['POST'])
def check_in(request):
    user_address = request.data.get('user_address')
    event_id = request.data.get('event_id')

    # check if details are provided
    if not user_address or not event_id:
        return Response({"error": "User address and event ID are required."}, status=400)
    
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found."}, status=404)
    
    # Check if the user has already checked in
    if Attendance.objects.filter(attendee=user_address).exists():
        return Response({"error": "User has already checked in."}, status=400)
    
    # Create a new attendance record
    attendance = Attendance.objects.create(
        attendee=user_address,
        badge_hash=event.transaction_hash,  # Assuming the badge hash is the transaction hash
        event=event
    )