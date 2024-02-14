from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def get_file_location(instance, filename):
    return f"files/{instance.folder.user.username}/{instance.folder.name}/{filename}"

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=200)
    folder = models.ForeignKey('self',on_delete=models.CASCADE, related_name='folders_within', null=True)

    def __str__(self):
        return f"{self.user} - {self.name}"
    

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, related_name='files')
    files = models.FileField(upload_to=get_file_location)

    def __str__(self):
        return f"{self.files}"
