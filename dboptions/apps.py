# coding: utf-8

from django.apps import AppConfig


class DBOptionsConfig(AppConfig):
    name = 'dboptions'

    def ready(self):
        self.module.autodiscover()
        self.module.init_signals()
