from .models import Profile
from mainapp.models import Folder

def create_profile(sender, instance, created, **kwargs): 
    if created:
        Profile.objects.create(user=instance)
        Folder.objects.create(user=instance, name="my_cloud")