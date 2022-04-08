import string
import random
from django.db import models
from django.conf import global_settings, settings
from django.contrib.auth import get_user_model
from django.forms import CharField, SlugField
from django.utils.timezone import now
#from users.models import Association

user = get_user_model()

def random_slug():
    return f''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    @property
    def tot_donated(self):
        query = self.project_pledges.all()
        return sum(pledge.amount for pledge in query)
    

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    goal = models.IntegerField()
    image = models.URLField(null=True)
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now=True, blank=True)
    deadline = models.DateTimeField(null=True)
    owner = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='projects',
        null=True
    )

class Comments(BaseModel):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment_txt = models.TextField(null=True)
    date_posted = models.DateTimeField(auto_now=True, blank=True)
    visible = models.BooleanField(default=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments'
    )


class Pledge(models.Model):
    amount = models.IntegerField()
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    # supporter = models.CharField(max_length=200)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )



class Favourite(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name = 'owner_favourites',
    )
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = 'projects_favourites'
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'project')

class AnimalSpecies(models.Model):
    value = models.CharField("Value", max_length=100,unique=True, null=False)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Animal Species'
        verbose_name_plural = 'Animal species'

class AnimalBreed(models.Model):
    value = models.CharField("Value", max_length=100,unique=True, null=False)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Breed of the Animal'
        verbose_name_plural = 'Animal Breeds'

class AnimalGender(models.Model):
    value = models.CharField("Value", max_length=20,unique=True, null=False)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Gender of the Animal'
        verbose_name_plural = 'Animal Gender'

class AnimalStatus(models.Model):
    value = models.CharField("Value", max_length=100,unique=True, null=False)
    def __str__(self):
        return str(self.value)
	
class Meta:
    verbose_name = 'Animal Status'
    verbose_name_plural = 'Animal Statuses'