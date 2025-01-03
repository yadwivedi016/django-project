from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.first_name

class Post(models.Model):
    POST_Categories = ( 
    (1, "Others"), 
    (2, "Java"), 
    (3, "C++"), 
    (4, "Javascripts"), 
    (5, "MySQL"), 
    (6, "Python")
    ) 
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    type = models.IntegerField(choices=POST_Categories)
    image = models.ImageField(
        upload_to='blog/', 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif','jpeg'])]
    )
    def __str__(self):
        return self.title
    
class Likes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Linking to User model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Linking to Post model
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    

class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Linking to User model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Linking to Post model
    comment = models.TextField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} comment on {self.post.title}"
    
class Friends(models.Model):
    user = models.ForeignKey("blog.CustomUser", on_delete=models.CASCADE)
    friend_id = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} is frend with {self.name}"
    
class Follow_Requests(models.Model):
    user = models.ForeignKey("blog.CustomUser", on_delete=models.CASCADE)
    request_name = models.CharField(max_length=100)
    request_id = models.IntegerField()

    def __str__(self):
        return self.request_name