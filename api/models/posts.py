from django.db import models
from .users import User 


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
	content = models.TextField()
	liked_users = models.ManyToManyField(User, related_name="liked_posts", blank=True)
	viewed_posts_users = models.ManyToManyField(User, related_name="viewed_posts", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
			return f"{self.user.username} | {self.content}"
	
	
class Media(models.Model):
		post = models.ForeignKey(Post,  on_delete=models.CASCADE, related_name="medias")
		file = models.FileField(upload_to="media_files/")


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username} |  {self.content}"