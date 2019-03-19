from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=30, blank=True)
#     section = models.CharField(max_length=20, blank=True)
#     department = models.CharField(max_length=20, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Attendance(models.Model):
	student_name = models.CharField(max_length = 30, blank = True)
	subjects = models.TextField()

	def __str__(self):
		return str(self.student_name)
