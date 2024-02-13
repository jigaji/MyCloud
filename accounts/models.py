from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def get_profile_img_path(instance, filename):
    return f"{instance.user.username}/profile/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to=get_profile_img_path, blank=True)
