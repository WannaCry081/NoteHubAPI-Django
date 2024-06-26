import bleach
from rest_framework import serializers
from api.v1.models import Note


class NoteSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = Note
        fields = ["id", "title", "body", "team", "owner"]
        extra_kwargs = {
            "owner": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(NoteSerializer, self).__init__(*args, **kwargs)

        exclude_fields = []

        if "request" in self.context:
            request = self.context["request"].method

            if request in ["PUT", "PATCH"]:
                exclude_fields.extend(["team"])

            if exclude_fields is not None:
                for field in exclude_fields:
                    self.fields.pop(field, None)

    def validate(self, attrs):

        if "title" in attrs:
            attrs["title"] = bleach.clean(attrs["title"])
        if "body" in attrs:
            attrs["body"] = bleach.clean(attrs["body"])

        return attrs

    def to_representation(self, instance):

        data = super().to_representation(instance)

        data["owner"] = self.get_owner(instance)
        data["team"] = self.get_team(instance)

        return data

    def get_owner(self, instance):

        if instance:
            owner_instance = instance.owner
            return {
                "id": owner_instance.id,
                "email": owner_instance.email,
                "username": owner_instance.username,
            }

        return None

    def get_team(self, instance):

        if instance:
            team_instance = instance.team
            return {
                "id": team_instance.id,
                "profile": team_instance.profile,
                "name": team_instance.name,
                "description": team_instance.description,
            }

        return None
