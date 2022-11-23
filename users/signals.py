# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from .models import *
# from django.dispatch import receiver


# @receiver(post_save,sender=User_Auth)
# def create_profile(sender,instance,created,**kwargs):
#     if created:
#         print(instance)
#         Profile.objects.create(user=instance)

# @receiver(post_save,sender=User_Auth)
# def save_profile(sender,instance,created,**kwargs):
#     if created:
#         instance.profile.save()