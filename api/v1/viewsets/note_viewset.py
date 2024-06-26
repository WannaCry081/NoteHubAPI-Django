from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.v1.models import Note, Team
from api.v1.serializers import NoteSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class NoteViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    ordering_fields = ["title", "body"]
    ordering = ["-created_at"]

    @swagger_auto_schema(
        operation_summary="Create a new note from the team.",
        operation_description="This endpoint creates a new note associated with the authenticated user and a team.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "body": openapi.Schema(type=openapi.TYPE_STRING),
                "team": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Created", NoteSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
            status.HTTP_404_NOT_FOUND: openapi.Response("Team not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                "Internal Server Error"
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create method for creating a new note.

        This endpoint creates a new note associated with the authenticated user and a team.

        Returns:
        - Created note details if successful.
        - Bad Request error if the request data is invalid.
        - Team not found error if the specified team does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)

            note = serializer.instance

            team = Team.objects.get(id=request.data["team"])
            team.notes.add(note)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response(
                {"detail": "Team not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Retrieve a note from the team.",
        operation_description="This endpoint gets a specific note from the specific team.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", NoteSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response("Note not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                "Internal Server Error"
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve method for retrieving a note.

        Returns:
        - Retrieved note details if found.
        - Note not found error if the note does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Note.DoesNotExist:
            return Response(
                {"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Update a note from the team.",
        operation_description="This endpoint will update all the information of the note data from the team.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "body": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response("OK", NoteSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
            status.HTTP_404_NOT_FOUND: openapi.Response("Note not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                "Internal Server Error"
            ),
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Update method for updating a note.

        Returns:
        - Updated note details if successful.
        - Bad Request error if the request data is invalid.
        - Note not found error if the note does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Reponse(
                {"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Partial update of a note from the team.",
        operation_description="This endpoint will update one or more information of the note data from the team.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "body": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response("OK", NoteSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
            status.HTTP_404_NOT_FOUND: openapi.Response("Note not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                "Internal Server Error"
            ),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update method for partially updating a note.

        Returns:
        - Partially updated note details if successful.
        - Bad Request error if the request data is invalid.
        - Note not found error if the note does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().partial_update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Response(
                {"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Delete a note from the team.",
        operation_description="This endpoint remove a specfic note from the team.",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("No Content"),
            status.HTTP_404_NOT_FOUND: openapi.Response("Note not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                "Internal Server Error"
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Destroy method for deleting a note.

        Returns:
        - No Content if the note is successfully deleted.
        - Note not found error if the note does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Note.DoesNotExist:
            return Response(
                {"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
