from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import EventSerializer
from .smart_contract import create_event_on_chain

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
            # Update the event with the transaction hash in models
            event.transaction_hash = tx_hash
            event.save()
            return Response({"message": "Event created successfully", "event_id": event.id, "transaction_hash": tx_hash}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
    return Response(serializer.errors, status=400)