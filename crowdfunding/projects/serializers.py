from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField, IntegerField, URLField 
from .models import *

User = get_user_model()

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only="true",
    )
    class Meta:
        model = Comments
        exclude = ['visible', "project"]

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comments = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.SlugRelatedField(
        slug_field='username',
        queryset=get_user_model().objects.all()
    )
    project_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.ReadOnlyField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.id')
    end_date = serializers.DateTimeField()
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())
    animals = serializers.ReadOnlyField(source='owner.animals.name')
    animals_id = serializers.ReadOnlyField(source='owner.animals.id')
    is_approved = serializers.ReadOnlyField(source='owner.animals.is_approved')
    pledges = PledgeSerializer(many=True, read_only=True)

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        project.save()
        return project

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open',instance.is_open)
        instance.date_created = validated_data.get('date_created',instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.deadline = validated_data.get('end_date', instance.deadline)
        instance.category = validated_data.get('category', instance.category)
        instance.status.set(validated_data.get('status', instance.status))
        instance.save()
        return instance

class FavouriteSerializer(serializers.ModelSerializer):
    """ used by FavouriteListView """
    date = serializers.ReadOnlyField()

    class Meta:
        model = Favourite
        fields = '__all__'
        read_only_fields = ('owner',)

class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField()

class CategoryDetailSerializer(CategorySerializer):
    Project = ProjectSerializer(many=True, read_only=True)

class AnimalSpeciesSerializer(ModelSerializer):
    value = CharField(max_length=100, required=True, validators=[
        UniqueValidator(queryset=AnimalSpecies.objects.all())])

    class Meta:
        model = AnimalSpecies
        fields = ['id', 'value']


class AnimalsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    animal_name = CharField(max_length=50, required=True)
    age = IntegerField(min_value=0, required=True)
    animal_species_id =serializers.SlugRelatedField(many=False, slug_field="value", queryset=AnimalSpecies.objects.all())
    description = CharField(max_length=1000, required=True)
    breed = CharField(max_length=50, required=True)
    gender = CharField(max_length=50, required=True)
    image = URLField()
    location = serializers.CharField(max_length=100, required=True)
    is_adopted = serializers.BooleanField()
    status = serializers.SlugRelatedField(many=True, slug_field="value", queryset=AnimalStatusTag.objects.all())
    def create(self, validated_data):
        status = validated_data.pop('status')
        Animals = Animals.objects.create(**validated_data)
        Animals.status.set(AnimalStatusTag)
        Animals.save()
        return Animals

    def validate(self, attrs):
        if 'request' in self.context:
            request = self.context['request']

            if len(request.FILES.getlist('images')) > 6:
                return ValidationError('Maximum number of attached images is 6')

        return super().validate(attrs)

    class Meta:
        model = AnimalSpecies
        fields = '__all__'

class AnimalsDetailSerializer(AnimalsSerializer):

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.species = validated_data.get('species', instance.name)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.color = validated_data.get('color', instance.color)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)       
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.status.set(validated_data.get('status', instance.status))
        instance.owner_id = validated_data.get('owner', instance.id)
        instance.save()
        return instance

class AnimalStatusTagSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    value = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return AnimalStatusTag.objects.create(**validated_data)