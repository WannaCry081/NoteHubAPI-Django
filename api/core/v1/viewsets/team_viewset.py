from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import Team
from api.core.v1.serializers import TeamSerializer, JoinTeamSerializer
from api.core.v1.permissions import IsOwner


class TeamViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get_permissions(self):
        
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
         
        return super().get_permissions()
    
    
    def get_serializer_class(self):
        
        if self.action == "join":
            return JoinTeamSerializer
        
        return super().get_serializer_class()
    
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
        
    def create(self, request, *args,  **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            
        except:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    @action(methods = ["POST"], detail = True)
    def join(self, request, pk = None):
        try: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            team = Team.objects.filter(
                code=serializer.validated_data["code"]).first()

            if team and request.user in team.members.all():
                return Response(
                    {"detail": "User is already a member."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            team.members.add(request.user)
            
            return Response(
                {"detail": "User successfully added to the team."},
                status=status.HTTP_201_CREATED
            )
            
        except Team.DoesNotExist:
            return Response(
                {"detail": "Team does not exist."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            return Response( 
                {"detail" : "Internal Server Error"},
                status = status.HTTP_200_OK
            )
    

    @action(methods = ["DELETE"], detail = True)
    def leave(self, request, pk = None):
        try:
            team = self.queryset.filter(id = pk).first()
            
            if team and request.user == team.owner:
                return Response(
                    {"detail" : "User is an owner."},
                    status = status.HTTP_400_BAD_REQUEST
                ) 
            
            if not (team and request.user in team.members.all()):
                return Response(
                    {"detail" : "User is not a member of the team."},
                    status = status.HTTP_400_BAD_REQUEST
                ) 
            
            team.members.remove(request.user)

            return Response(
                {"detail": "User successfully left the team."},
                status=status.HTTP_200_OK
            )
            
        except Team.DoesNotExist:
            return Response(
                {"detail": "Team does not exist."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e: 
            return Response( 
                {"detail" : "Internal Server Error"},
                status = status.HTTP_200_OK
            )