from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Tag


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'in_response_to', 'conversation', 'created_at', )
    list_filter = ('text', 'created_at', )
    search_fields = ('text', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(Statement, StatementAdmin)
admin.site.register(Tag, TagAdmin)
