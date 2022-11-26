from django.contrib import admin

from .models import Keyword, Watchlist, FlaggedMessage


admin.site.register(Keyword)
admin.site.register(Watchlist)
admin.site.register(FlaggedMessage)
