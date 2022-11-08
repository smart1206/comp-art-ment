from django.contrib import admin
from .models import Art, Profile, PhotoArt, PhotoProfile


# Register your models here.
admin.site.register(Art)
admin.site.register(Profile)
admin.site.register(PhotoArt)
admin.site.register(PhotoProfile)
