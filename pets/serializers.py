from rest_framework import serializers

class GroupSerializer(serializers.Serializer):
    scientific_name = serializers.CharField()


class TraitSerializer(serializers.Serializer):
    name = serializers.CharField()


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    traits = TraitSerializer(many=True)