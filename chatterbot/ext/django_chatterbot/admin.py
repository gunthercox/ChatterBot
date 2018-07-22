from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Response, Tag


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', )
    list_filter = ('text', 'created_at', )
    search_fields = ('text', )


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'response', 'occurrence', )
    search_fields = ['statement__text', 'response__text']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(Statement, StatementAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Tag, TagAdmin)
