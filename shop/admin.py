from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Category, Product
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Register the 'Category' model with a predefined list
    of fields displayed in admin site;
    Create slug automatically from name.
    """
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    """
    Register the 'Product' model with a predefined list
    of fields displayed in admin site;
    Set fields editable from admin site.
    Create slug automatically from name.
    """
    list_display = ['name',
                    'slug',
                    'price',
                    'available',
                    'created',
                    'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
