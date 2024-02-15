from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import shutil

# Create your models here.
def get_file_location(instance, filename):
    current_location = instance.folder
    path = ""
    while (current_location):
        path = f'/{current_location.name}' + path
        current_location = current_location.folder
    return f"files/{instance.folder.user.username}/{path}/{filename}"

def get_current_location(current_folder):
    username = current_folder.user.username
    path = ""
    while(current_folder):
        path = f"/{current_folder.name}" + path
        current_folder = current_folder.folder
    return f"media/files/{username}{path}"

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=200)
    folder = models.ForeignKey('self',on_delete=models.CASCADE, related_name='folders_within', null=True)

    def __str__(self):
        return f"{self.user} - {self.name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['folder', 'name'], name='unique_folder_name'),
            models.UniqueConstraint(fields=['name', 'user'], condition=Q(folder=None), name='unique_folder_on_home_page')
        ] 

    def delete(self, *args, **kwargs):
        try:
           shutil.rmtree(get_current_location(self))
        except:
           pass
        finally:
           super().delete(*args, **kwargs)
        

          

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, related_name='files')
    files = models.FileField(upload_to=get_file_location)
    filename= models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.files}"

    def save(self, *args, **kwargs):
        self.filename = self.files.name
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.files.storage.delete(self.files.name)
        super().delete(*args, **kwargs)
