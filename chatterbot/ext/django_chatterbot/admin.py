from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Response


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', )
    list_filter = ('text', )
    search_fields = ('text', )


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'occurrence', )


admin.site.register(Statement, StatementAdmin)
admin.site.register(Response, ResponseAdmin)
