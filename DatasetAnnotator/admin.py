from django.contrib import admin

from .models import *

admin.site.register(Badge)
admin.site.register(Comment)
admin.site.register(PostHistory)
admin.site.register(PostLink)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Vote)

