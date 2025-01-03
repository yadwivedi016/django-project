from django.contrib import admin
from.models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Friends)
admin.site.register(Follow_Requests)

