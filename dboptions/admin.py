# coding: utf-8
from django.contrib import admin
from dboptions.models import Option, DBOPTIONS_DICT
from dboptions.forms import OptionForm
from django.utils.translation import ugettext_lazy as _


class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'value', 'is_active', 'created_at', 'updated_at')
    list_editable = ('value', 'is_active', )
    form = OptionForm

    def description(self, obj):
        return DBOPTIONS_DICT.get(obj.name, {}).get('description', '')

    description.allow_tags = True
    description.short_description = _('option description')

    actions = ['delete_selected_with_post_delete_signal']

    def get_actions(self, request):
        actions = super(OptionAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_with_post_delete_signal(self, request, queryset):
        # we need this to force calling post_delete signal for every object
        for obj in queryset:
            obj.delete()

        self.message_user(request, _("options successfully deleted."))

    delete_selected_with_post_delete_signal.short_description = "Delete selected entries"


admin.site.register(Option, OptionAdmin)

