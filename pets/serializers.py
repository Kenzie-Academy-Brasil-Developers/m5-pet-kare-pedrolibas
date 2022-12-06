from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from pets.models import SexPet, Pet
from groups.models import Group
from traits.models import Trait


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexPet.choices, default=SexPet.NOT_INFORMED)
    traits_count = serializers.SerializerMethodField(read_only=True)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_traits_count(self, obj):
        return len(Pet.objects.get(id=obj.id).traits.all())

    def create(self, validated_data: dict):
        group_dict = validated_data.pop("group")
        traits = validated_data.pop("traits")
        
        pet = Pet.objects.create(**validated_data)

        group = Group.objects.get_or_create(scientific_name=group_dict["scientific_name"])
        pet.group = group[0]

        for trait in traits:
            trait_data = Trait.objects.get_or_create(name=trait["name"])
            pet.traits.add(trait_data[0])

        return pet


    def update(self, instance, validated_data: dict):
        if validated_data.get("group"):
            instance.group = Group.objects.get_or_create(scientific_name=validated_data["group"]["scientific_name"])[0]
            validated_data.pop("group")

        if validated_data.get("traits"):
            instance.traits.set([Trait.objects.get_or_create(name=trait["name"])[0] for trait in validated_data["traits"]])
            validated_data.pop("traits")

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance