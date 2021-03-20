import sys

from django.conf import settings
from django.urls import path
from django.http import HttpResponse


settings.configure(
  DEBUG=True,
  SECRET_KEY="a-bad-secret",
  ROOT_URLCONF=__name__,
)


def home(request):
  return HttpResponse("Home page...")


urlpatterns = [
  path('', home),
]


if __name__ == "__main__":
  from django.core.management import execute_from_command_line

  execute_from_command_line(sys.argv)