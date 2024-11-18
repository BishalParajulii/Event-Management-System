from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from .models import Event , Participant
from .serializers import EventSerializer , ParticipantSerializer


@api_view(['GET'])
def event_Overviews(request):
    api_urls = {
        'all_events' : '/all' ,
        'Add' : '/create' ,
        'update' : '/update/pk' ,
        'delete' : 'name/pk/delete'
    }
    return Response(api_urls)

@api_view(['GET'])
def view_event(request, id=None):
    if id is None:
        # Retrieve all events
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    else:
        try:
            # Retrieve a specific event by ID
            event = Event.objects.get(id=id)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_event(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        # Pass 'request' as part of the context when initializing the serializer
        serializer = EventSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            # Save the event
            event = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_event(request, event_id):
    try:
        # Fetch the event by ID
        event = Event.objects.get(id=event_id)

        # Check if the authenticated user is the creator of the event
        if event.created_by != request.user:
            return Response(
                {'detail': 'You do not have permission to update this event.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # If the user is the creator, update the event
        serializer = EventSerializer(event, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Event.DoesNotExist:
        return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def delete_event(request, event_id):
    try:
        # Fetch the event by id
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the logged-in user is the creator of the event
    if event.created_by != request.user:
        return Response({'detail': 'You are not authorized to delete this event.'}, status=status.HTTP_403_FORBIDDEN)

    # Delete the event
    event.delete()

    # Return a response indicating successful deletion
    return Response({'detail': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
