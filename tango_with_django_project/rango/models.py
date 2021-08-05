from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    likes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    dislikes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    likeDislikeDefault = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.full_clean()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Video(models.Model):
    TITLE_MAX_LENGTH = 300
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Book(models.Model):
    TITLE_MAX_LENGTH = 300
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    picUrl = models.URLField()
   

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    cats = models.ManyToManyField(Category, default=None, blank=True)

    def __str__(self):
        return self.user.username


class Quote(models.Model):
    MAX_LENGTH = 500

    text = models.CharField(max_length = MAX_LENGTH)
    author = models.CharField(max_length = MAX_LENGTH)

    def __str__(self):
        return self.author
