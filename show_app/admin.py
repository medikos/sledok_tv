from django.contrib import admin
from .models import Show, Actors, Genres, WebChannel, Episode, RusFields


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_tvmaze', 'type_show', 'status', 'web_channel')
    list_display_links = ('name', 'type_show')
    ordering = ('premired', 'type_show', 'status')
    sortable_by = ('premired', 'type_show', 'web_channel', 'id_tvmaze')
    search_fields = ('pk',)
    show_full_result_count = True
    list_per_page = 50
    empty_value_display = '-----'


@admin.register(RusFields)
class RusFieldsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')


admin.site.register(Actors)
# admin.site.register(Genres)
admin.site.register(WebChannel)
admin.site.register(Episode)
