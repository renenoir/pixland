from django.contrib import admin

from pixlands.models import Topic, Image, ProfilePic, Comment, Like

admin.site.register(Topic)
admin.site.register(Image)
admin.site.register(ProfilePic)
admin.site.register(Comment)
admin.site.register(Like)
