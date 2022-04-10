from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from django.http import Http404
from rest_framework import status, permissions, generics
from .models import Project, Pledge, Category, Comments, Favourite
from .serializers import (
    CommentsSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    PledgeSerializer,
    ProjectSerializer, 
    ProjectDetailSerializer, 
    FavouriteSerializer)
from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly

# Create your views here.
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

class CommentListApi(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comments.objects.filter(visible=True)
    serializer_class = CommentsSerializer

class CommentDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comments.objects.filter(visible=True)
    serializer_class = CommentsSerializer

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
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class FavouriteListView(generics.ListCreateAPIView):
    """ 
    shows favourites of request user
    if favourite exists, remove, or create
    url: favourites 
    """
    serializer_class = FavouriteSerializer
    permission_classes = [IsOwnerOrReadOnly]

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




        

