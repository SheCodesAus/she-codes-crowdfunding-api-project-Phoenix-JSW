import string
import random
from datetime import datetime, timedelta
from django.db import models
from django.conf import global_settings
from django.contrib.auth import get_user_model
from django.forms import CharField, SlugField, TimeField
from django.utils.timezone import now
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


user = get_user_model()

def random_slug():
    return f''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AnimalStatusTag(models.Model):
    value = models.CharField("Value", max_length=200)

    def __str__(self):
        return str(self.value)
	
class Meta:
    verbose_name = 'Statustag'
    verbose_name_plural = 'Statustag'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

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

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    goal = models.IntegerField()
    image = models.URLField(null=True)
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now=True, blank=True)
    end_date = models.DateTimeField(null=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='projects',
        null=True
    )
    favourites = models.ManyToManyField(
    get_user_model(), related_name='project_favourites',
    through='Favourite'
    )
    animals = models.ForeignKey(
        "Animals",
        on_delete=models.CASCADE,
        related_name='animals',
        null=True
    )
    # status = models.ManyToManyField(
    #     AnimalStatusTag,
    #     related_name = "project",
    #     related_query_name = "Projects"
    # )

    @property
    def is_open(self):
        if self.end_date is None:
            return True
        return (self.end_date) > now()
    
    @property
    def tot_donated(self):
        query = self.project_pledges.all()
        return sum(pledge.amount for pledge in query)

class Pledge(models.Model):
    amount = models.IntegerField()
    comments = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )

class AnimalSpecies(models.Model):
    value = models.CharField("Value", max_length=100,unique=True, null=False)

    def __str__(self):
        return (self.value)

    class Meta:
        verbose_name = 'Animal Species'
        verbose_name_plural = 'Animal species'


class Animals(models.Model):
    image = models.URLField()
    animal_name = models.CharField("Name", max_length=50)
    animal_species = models.ForeignKey(AnimalSpecies, on_delete=models. PROTECT, verbose_name="Animal Species")
    breed = models.CharField("breed", max_length=50)
    gender = models.CharField("gender", max_length=50)
    description = models.TextField("description", max_length=1000, help_text="Describe the Animals Personality", null=True)
    age = models. PositiveSmallIntegerField("Full Years")
    location = models.CharField("Name", max_length=100)
    is_adopted = models.BooleanField()
    status = models.ManyToManyField(
        AnimalStatusTag,
        related_name = "animals",
        related_query_name = "animal"
    )

    @property

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('animal-detail', args=(self.pk,))

class Foster(models.Model):
    user = models.OneToOneField(get_user_model(),
        on_delete=models.CASCADE,
        related_name="Foster",
        null=True)
    name = models.CharField(max_length=200)  # animal name
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')
    comment = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Adopt(models.Model):
    user = models.OneToOneField(get_user_model(),
        on_delete=models.CASCADE,
        related_name="Adopt",
        null=True)
    name = models.CharField(max_length=200)  # animal name
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')
    comment = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Support(models.Model):
    user = models.OneToOneField(get_user_model(),
        on_delete=models.CASCADE,
        related_name="Support",
        null=True)
    name = models.CharField(max_length=200)  # animal name
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')
    comment = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Favourite(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name = 'owner_favourites',
    )
    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = 'project_favourites'
    )
    date_added = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = ('owner', 'project')