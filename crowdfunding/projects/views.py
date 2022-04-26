from pdb import post_mortem
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import AnimalBreed, AnimalGender, AnimalSpecies,  Project
from django.http import Http404
from rest_framework import status, permissions, generics, filters, status
from .models import Project, Pledge, Category, Comments, Favourite, Animals, AnimalBreed, AnimalGender,  AnimalSpecies, AnimalStatusTag
from .serializers import (
    AnimalBreedSerializer,
    AnimalGenderSerializer,
    AnimalSpeciesSerializer,
    AnimalsSerializer,
    AnimalsDetailSerializer,
    CommentsSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    PledgeSerializer,
    ProjectSerializer, 
    ProjectDetailSerializer, 
    FavouriteSerializer,
    AnimalStatusTagSerializer)
from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser
from users.models import CustomUser

# Create your views here.
def get_shared_permissions(action):
    return [AllowAny()] if action == 'retrieve' or action == 'list' else [IsAdminUser()]


# Projects & Pledges
class PledgeList(APIView):    

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class UsersPledges(generics.ListAPIView):
    # Get list of pledges that the current user has made
    serializer_class = PledgeSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = CustomUser.objects.get(pk=pk)
        return Pledge.objects.filter(supporter=user)

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
                
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            # return Project.objects.get(pk=pk)
            project =Project.objects.get(pk=pk)
            self.check_object_permissions(self.request,project)
            return project
        except Project.DoesNotExist:
            raise Http404
               
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(
            "Deleted",
            status = status.HTTP_204_NO_CONTENT
        )

# Animals
class AnimalsList(APIView):
    # Create Animal, get list of animals
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        animals = animals.objects.all()
        serializer = AnimalsSerializer(animals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnimalsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AnimalsDetail(APIView):
    # Get details of a single animals, update animals details
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            return Animals.objects.get(pk=pk)
        except Animals.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        animals = self.get_object(pk)
        serializer = AnimalsDetailSerializer(animals)
        return Response(serializer.data)

    def put(self, request, pk):
        animals = self.get_object(pk)
        data = request.data
        serializer = AnimalsDetailSerializer(
            instance=animals,
            data=data,
            partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

        def delete(self, request, pk):
            animals = self.get_object(pk)
            animals.delete()
            return Response(
                "Deleted",
                status = status.HTTP_204_NO_CONTENT
        )

# Filtered Views

class AnimalSpeciesView(generics.ListCreateAPIView):
    queryset = AnimalSpecies.objects.all()
    serializer_class = AnimalSpeciesSerializer

    def get_permissions(self):
        return get_shared_permissions(self.action)


class AnimalGenderView(generics.ListCreateAPIView):
    queryset = AnimalGender.objects.all()
    serializer_class = AnimalGenderSerializer

    def get_permissions(self):
        return get_shared_permissions(self.action)


class AnimalBreedView(generics.ListCreateAPIView):
    queryset = AnimalBreed.objects.all()
    serializer_class = AnimalBreedSerializer

    def get_permissions(self):
        return get_shared_permissions(self.action)

class AnimalStatusTag(APIView):
    # Create pet category, return list of all categories
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = AnimalStatusTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):
        animals = AnimalStatusTag.objects.all()
        serializer = AnimalStatusTagSerializer(animals, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    """ url: categories/<str:name>/"""
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'name'
    
    def get_object(self, **kwargs):
        try:
            if "slug" in kwargs:
                return Category.objects.get(slug=kwargs["slug"])
            return Category.objects.get(pk=kwargs["pk"])
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, **kwargs):
        category = self.get_object(**kwargs)
        serializer = CategorySerializer(category)
        return Response(serializer.data)  

class FavouriteListView(generics.ListCreateAPIView):
    """ 
    shows favourites of request user
    if favourite exists, remove, or create
    url: favourites 
    """
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
       returns list of all favourites for current authenticated user.
        """
        user = self.request.user
        return Favourite.objects.filter(owner=user)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.is_valid()
        data = serializer.validated_data
        project = data.get('project')
        user = self.request.user
        if project.favourites.filter(id=user.id).exists():
            project.favourites.remove(user)
        else:
            project.favourites.add(user)

class FavouriteView(APIView):
    """
    Favourite projects of (request.user)(url has id of project) 
    If requested favourite doesn't exist, it's'created, otherwise it's removed
    """

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        favourite = False
        project = self.get_object(pk)
        user = request.user
        if project.favourites.filter(id=user.id).exists():
            favourite = True
        return Response(f"{project},{user},{favourite}")

    def post(self, request, pk):
        project = self.get_object(pk)
        if project.favourite.filter(id=request.user.id).exists():
            project.favourite.remove(request.user)
            Favourite = False
        else:
            post.favourite.add(request.user)
            favourite = True

class CommentListApi(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comments.objects.filter(visible=True)
    serializer_class = CommentsSerializer

class CommentDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comments.objects.filter(visible=True)
    serializer_class = CommentsSerializer      

