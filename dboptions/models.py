# coding: utf-8
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


DBOPTIONS_CACHE_PREFIX = getattr(settings, "DBOPTIONS_CACHE_PREFIX", "DBOPTIONS_")

DBOPTIONS_CACHE_INTERVAL = getattr(settings, "DBOPTIONS_CACHE_INTERVAL", 60)

DBOPTIONS_LIST = getattr(settings, "DBOPTIONS", [])

DBOPTIONS_DICT = dict((x['name'], x) for x in DBOPTIONS_LIST)

DBOPTIONS_CHOICES = ((x['name'], x['name']) for x in DBOPTIONS_LIST)


def get_option_cache_key(option_name):
    return DBOPTIONS_CACHE_PREFIX + option_name


def cast_bool(value):
    if not value:
        return False
    return value is True or value.lower() in ["1", "true", "yes"]


cast_funcs = {
    "bool": cast_bool
}


def to_final_value(option_name, option_value):
    """
    :param option_name: the name of registered option
    :param option_value: the string value of option
    :return: final value of proper type
    """
    option = DBOPTIONS_DICT.get(option_name)
    if not option:
        raise ImproperlyConfigured(
            u"option {0} not registered in settings DBOPTIONS dictionary".format(option_name)
        )

    cast = option.get("cast")

    if cast:
        if callable(cast):
            cast_func = cast
        else:
            cast_func = cast_funcs.get(cast)
            if not cast_func:
                raise ImproperlyConfigured(
                    u"option {0} has unknown cast function in settings DBOPTIONS dictionary".format(option_name)
                )
        try:
            final_value = cast_func(option_value)
        except Exception:
            raise ValueError(
                u"option {0} with value {1} can not be casted to final value using "
                u"cast function from DBOPTIONS settings".format(
                    option_name, option_value
                )
            )
        else:
            return final_value
    else:
        # no transform required - just return string
        return option_value


class Option(models.Model):
    name = models.CharField(_("option key"), choices=DBOPTIONS_CHOICES, max_length=255, unique=True)
    value = models.CharField(_("option value"), max_length=255, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    is_active = models.BooleanField(_("is active"), default=True, help_text=_(u"when off – default value will be used"))

    class Meta:
        verbose_name = _("database option")
        verbose_name_plural = _("database options")
        app_label = 'dboptions'

    def __unicode__(self):
        return self.name

    @classmethod
    def get(cls, option_name):
        option = DBOPTIONS_DICT.get(option_name)
        if not option:
            raise ImproperlyConfigured(
                u"option {0} not registered in settings DBOPTIONS dictionary".format(option_name)
            )

        cache_key = get_option_cache_key(option_name)
        value = cache.get(cache_key)
        if value is not None:
            return value

        try:
            value = cls.objects.filter(is_active=True).get(name=option_name).value
        except cls.DoesNotExist:
            # try to return default value if exists
            if 'default' in option:
                value = option['default']
            else:
                raise ImproperlyConfigured(
                    u"option {0} not found in database and has no default value in DBOPTIONS".format(option_name)
                )

        final_value = to_final_value(option_name, value)
        cache.set(cache_key, final_value, DBOPTIONS_CACHE_INTERVAL)

        return final_value

    def enable(self):
        self.is_active = True
        self.save()

    def disable(self):
        self.is_active = False
        self.save()


def update_option_cache(sender, instance, **kwargs):
    cache_key = get_option_cache_key(instance.name)
    final_value = to_final_value(instance.name, instance.value)
    cache.set(cache_key, final_value, DBOPTIONS_CACHE_INTERVAL)


def delete_option_cache(sender, instance, **kwargs):
    cache_key = get_option_cache_key(instance.name)
    cache.delete(cache_key)


post_save.connect(update_option_cache, sender=Option)
post_delete.connect(delete_option_cache, sender=Option)
