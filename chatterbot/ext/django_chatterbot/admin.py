from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import (
    Statement, Response, Conversation, Tag
)


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', )
    list_filter = ('text', )
    search_fields = ('text', )


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'response', 'occurrence', )
    search_fields = ['statement__text', 'response__text']


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(Statement, StatementAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Tag, TagAdmin)
