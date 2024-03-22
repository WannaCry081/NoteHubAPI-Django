import bleach
from rest_framework import serializers
from api.models import Team


class TeamSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField(read_only = True)
    members = serializers.StringRelatedField(many=True, read_only = True)
    
    class Meta:
        
        model = Team
        fields = ["id", "profile", "name", "code", "description", "owner", "members"]
        extra_kwargs = {
            "owner" : {"read_only" : True},
            "code" : {"read_only" : True}
        }
    
    
    def validate(request, attrs):
        
        if "profile" in attrs: 
            attrs["profile"] = bleach.clean(attrs["profile"])
        if "name" in attrs:
            attrs["name"] = bleach.clean(attrs["name"])
        if "description" in attrs:
            attrs["description"] = bleach.clean(attrs["description"])
            
        return attrs
    
    
    def get_owner(self, instance):
        
        if instance:
            owner_instance = instance.owner
            return {
                "id" : owner_instance.id,
                "username" : owner_instance.username,
                "email" : owner_instance.email,
            }
            
        else:
            return None
        
    
    def get_members(self, instance):
        
        if instance:
            members_instance = instance.members.all()
            members = []
            
            for member in members_instance:
                members.append({
                    "id" : member.id,
                    "username" : member.username,
                    "first_name" : member.first_name,
                    "middle_name" : member.middle_name,
                    "last_name" : member.last_name,
                    "email" : member.email
                })
        
            return members
            
        else:
            return None        
    
    
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data["owner"] = self.get_owner(instance)
        data["members"] = self.get_members(instance)
        
        if "code" in data and self.context.get("request") and self.context["request"].method != "POST":
            del data["code"]
        
        return data