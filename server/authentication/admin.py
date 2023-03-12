from django.contrib import admin
from .models import GazpromUser, Well, Check

admin.site.register(GazpromUser)
admin.site.register(Well)
admin.site.register(Check)
