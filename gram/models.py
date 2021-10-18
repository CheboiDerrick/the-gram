from django.db import models
from django.contrib.auth.models import User


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
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    # get images by user
    @classmethod
    def get_images_by_user(cls, user):
        images = cls.objects.filter(user=user)
        return images

    # save image
    def save_image(self):
        self.save()

    # delete image
    def delete_image(self):
        self.delete()

    # update image caption
    def update_caption(self, new_caption):
        self.image_caption = new_caption
        self.save()

    # search images using image name
    @classmethod
    def search_by_image_name(cls, search_term):
        images = cls.objects.filter(
            image_name__icontains=search_term)
        return images

    #  get a single image using id
    @classmethod
    def get_single_image(cls, id):
        image = cls.objects.get(id=id)
        return image

    def __str__(self):
        return self.image_name



