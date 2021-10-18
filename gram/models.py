import datetime as dt
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related


# cloudinary
# from cloudinary.models import CloudinaryField

# Create your models here.
# post model
class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts', default=None)
    image_name = models.CharField(max_length=50)
    image_caption = models.TextField()
    image_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    # get images by user
    @classmethod
    def get_images_by_user(cls, user):
        posts = cls.objects.filter(user=user)
        return posts
    def delete_image(self):
        self.delete()

    # update image caption
    def update_caption(self, new_caption):
        self.image_caption = new_caption
        self.save()

    # search images using image name
    @classmethod
    def search_by_image_name(cls, search_term):
        posts = cls.objects.filter(
            image_name__icontains=search_term)
        return posts

    #  get a single image using id
    @classmethod
    def get_single_image(cls, id):
        post = cls.objects.get(id=id)
        return post

    def __str__(self):
        return self.image_name


# profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='accounts/profile_photos', default=None)
    bio = models.TextField(max_length=500, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)

    def update(self):
        self.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile

    def __str__(self):
        return self.user.username


# likes model
class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.likes


# comments model
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    comment_date = models.DateTimeField(auto_now_add=True)

    def save_comment(self):
        self.save()

    def __str__(self):
        return self.comment
