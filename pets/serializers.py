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
    group = GroupSerializer()
    traits = TraitSerializer(many=True)


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
        group_dict = validated_data.pop("group")
        traits = validated_data.pop("traits")

        for key, value in validated_data.items():
            setattr(instance, key, value)

        # instance.name = validated_data.get("name", instance.name)
        # instance.age = validated_data.get("age", instance.age)
        # instance.weight = validated_data.get("weight", instance.weight)
        # instance.sex = validated_data.get("sex", instance.sex)
        # instance.group = Group.objects.get_or_create(scientific_name=validated_data["group"]["scientific_name"])[0]
        # instance.traits.set = [Trait.objects.get_or_create(name=trait["name"])[0] for trait in validated_data["traits"]]

        print("teste serializer")

        instance.save()

        return instance