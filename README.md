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
    },
    {
        "name": "DISABLE_NOTIFICATIONS",
        "default": False,
        "description": "allows to disable notifications on site",
        "cast": "bool"
    }
]
```

`cast` **can be callable** function that casts string option representation into Python object **or string** that
matches to one of the predefined cast function. At moment only `"bool"` available, which internally looks like this:

```python
def cast_bool(value):
    if not value:
        return False
    return value is True or value.lower() in ["1", "true", "yes"]
```

Now it's possible to add/change registered options in admin web interface.

And to use its value in code:
```python
from dboptions import Option

default_cache_interval = Option.get('DEFAULT_CACHE_INTERVAL')
```

See [test project example](https://github.com/FZambia/django-dboptions/tree/master/devproject)
