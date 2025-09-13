from django.contrib import admin
from .models import Quote, QuoteItem

class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    autocomplete_fields = ['producto']

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'fecha', 'total', 'activo']
    list_filter = ['fecha', 'activo']
    search_fields = ['numero', 'cliente__nombre']
    inlines = [QuoteItemInline]
    readonly_fields = ['total']
