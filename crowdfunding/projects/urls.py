from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .import views

urlpatterns = [
    path('animals/', views.AnimalsList.as_view(), name="animal-detail"),
    path('animals/<int:pk>/', views.AnimalsDetail.as_view(), name="animal-detail"),
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('<int:pk>/pledges/', views.UsersPledges.as_view()),
    path('comment/', views.CommentListApi.as_view(), name="comment-list"),
    path('animalstatus/', views.AnimalStatusTag.as_view()),
    path('comment/<int:pk>/', views.CommentDetailApi.as_view(), name="comment-detail"),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name="category-detail"),
    path('category/<str:slug>/', views.CategoryDetail.as_view(), name="category-detail-slug"),
    path('favourites/', views.FavouriteListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)