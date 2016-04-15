# django-dboptions

The missing simple Django database configuration options

```
pip install django-dboptions
```

Add `dboptions` to INSTALLED_APPS

Run migrations.

Add `DBOPTIONS` list with registered options into `settings.py`:

```python
DBOPTIONS = [
    {
        "name": "DEFAULT_CACHE_INTERVAL",
        "default": 60,
        "description": "sets cache interval in seconds",
        "cast": int
    }
]
```

Now it's possible to add/change registered options in admin web interface.

And to use its value in code:
```python
from dboptions import Option

default_cache_interval = Option.get('DEFAULT_CACHE_INTERVAL')
```

See [test project example](https://github.com/FZambia/django-dboptions/tree/master/devproject)
