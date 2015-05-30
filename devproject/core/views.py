from django.http import HttpResponse
from django.views.generic import View


class HelloView(View):

    def get(self, request):
        return HttpResponse("<a href='/admin'>Admin</a>")
