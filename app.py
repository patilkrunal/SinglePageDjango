import os
import sys

from django.conf import settings
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.core.wsgi import get_wsgi_application
from django.template import RequestContext, Template
from django import forms

CSV_LIST = "emaillist.csv"

settings.configure(
  DEBUG = os.environ.get("DEBUG", ""),
  ALLOWED_HOST = ["*"],
  SECRET_KEY = os.environ.get("SECRET_KEY", "a-bad-secret"),
  ROOT_URLCONF = __name__,
  TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}],
  MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionMiddleware",
  )
)


class EnlistForm(forms.Form):
  email = forms.EmailField(
    required=True, 
    label=False, 
    widget=forms.EmailInput(attrs={"placeholder": "Enter your Email"}))

  referrer = forms.CharField(required=False, widget=forms.HiddenInput())


def home(request):
  if request.method == "POST":
    form = EnlistForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data["email"]
      referrer = form.cleaned_data["referrer"]
      ip = request.META.get("REMOTE_ADDR")
      
      with open(CSV_LIST, "a") as csv:
        csv.write(f"{email},{referrer},{ip}\n")
      return HttpResponseRedirect("/thanks/")
  else:
    form = EnlistForm(initial={"referrer": request.META.get("HTTP_REFERER")})
    context = RequestContext(
      request, {"content": "Sign up for early access", "form": form}
    )

  return HttpResponse(MAIN_HTML.render(context))

def thanks(request):
  context = RequestContext(
    request, 
    {"content": "Thank you for signing up. We will contact you!", "form": None}
  )

  return HttpResponse(MAIN_HTML.render(context))
  


urlpatterns = [
  path('', home),
  path("thanks/", thanks),
]

app = get_wsgi_application()

MAIN_HTML = Template("""
  <html>
    <head>
      <title>Coming Soon | Flying Cars</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
      @import url('https://fonts.googleapis.com/css2?family=Exo:wght@400;500;600;700;800;900&display=swap');
      *{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Exo', sans-serif;
      }
      html,body{
        display: grid;
        height: 100%;
        width: 100%;
        place-items: center;
        background-color: #343434;
        /* Thanks to Hero Patterns for the background */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 28' width='56' height='28'%3E%3Cpath fill='%23000000' fill-opacity='0.4' d='M56 26v2h-7.75c2.3-1.27 4.94-2 7.75-2zm-26 2a2 2 0 1 0-4 0h-4.09A25.98 25.98 0 0 0 0 16v-2c.67 0 1.34.02 2 .07V14a2 2 0 0 0-2-2v-2a4 4 0 0 1 3.98 3.6 28.09 28.09 0 0 1 2.8-3.86A8 8 0 0 0 0 6V4a9.99 9.99 0 0 1 8.17 4.23c.94-.95 1.96-1.83 3.03-2.63A13.98 13.98 0 0 0 0 0h7.75c2 1.1 3.73 2.63 5.1 4.45 1.12-.72 2.3-1.37 3.53-1.93A20.1 20.1 0 0 0 14.28 0h2.7c.45.56.88 1.14 1.29 1.74 1.3-.48 2.63-.87 4-1.15-.11-.2-.23-.4-.36-.59H26v.07a28.4 28.4 0 0 1 4 0V0h4.09l-.37.59c1.38.28 2.72.67 4.01 1.15.4-.6.84-1.18 1.3-1.74h2.69a20.1 20.1 0 0 0-2.1 2.52c1.23.56 2.41 1.2 3.54 1.93A16.08 16.08 0 0 1 48.25 0H56c-4.58 0-8.65 2.2-11.2 5.6 1.07.8 2.09 1.68 3.03 2.63A9.99 9.99 0 0 1 56 4v2a8 8 0 0 0-6.77 3.74c1.03 1.2 1.97 2.5 2.79 3.86A4 4 0 0 1 56 10v2a2 2 0 0 0-2 2.07 28.4 28.4 0 0 1 2-.07v2c-9.2 0-17.3 4.78-21.91 12H30zM7.75 28H0v-2c2.81 0 5.46.73 7.75 2zM56 20v2c-5.6 0-10.65 2.3-14.28 6h-2.7c4.04-4.89 10.15-8 16.98-8zm-39.03 8h-2.69C10.65 24.3 5.6 22 0 22v-2c6.83 0 12.94 3.11 16.97 8zm15.01-.4a28.09 28.09 0 0 1 2.8-3.86 8 8 0 0 0-13.55 0c1.03 1.2 1.97 2.5 2.79 3.86a4 4 0 0 1 7.96 0zm14.29-11.86c1.3-.48 2.63-.87 4-1.15a25.99 25.99 0 0 0-44.55 0c1.38.28 2.72.67 4.01 1.15a21.98 21.98 0 0 1 36.54 0zm-5.43 2.71c1.13-.72 2.3-1.37 3.54-1.93a19.98 19.98 0 0 0-32.76 0c1.23.56 2.41 1.2 3.54 1.93a15.98 15.98 0 0 1 25.68 0zm-4.67 3.78c.94-.95 1.96-1.83 3.03-2.63a13.98 13.98 0 0 0-22.4 0c1.07.8 2.09 1.68 3.03 2.63a9.99 9.99 0 0 1 16.34 0z'%3E%3C/path%3E%3C/svg%3E");
      }
      ::selection{
        color: #fff;
        background: #FC4782;
      }
      .wrapper{
        color: #eee;
        max-width: 900px;
        text-align: center;
        padding: 0 50px;
      }
      .signup {
        margin-top: 30px;
        margin-bottom: 10px;
      }
      .content {
        margin-top: 40px;
        margin-bottom: 10px;
      }
      </style>
    </head>
    <body>
      <div class="wrapper">
        <svg width="600" height="300" version="1.1" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,312)"><path d="m218.36-289.66h163.29c29.039 0 52.417 23.378 52.417 52.417v45.564c0 29.039-23.378 52.417-52.417 52.417h-163.29c-29.039 0-52.417-23.378-52.417-52.417v-45.564c0-29.039 23.378-52.417 52.417-52.417z" fill="#204a87" stop-color="#000000" stroke="#eeeeec" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/><g fill="#729fcf" stroke="#eeeeec" stroke-linejoin="round" stroke-width="4"><path d="m240.88-162.15c21.473-37.192 42.946-74.385 64.419-111.58" stop-color="#000000"/><g stroke-linecap="round"><path d="m276.15-249.32h-72.081" stop-color="#000000"/><path d="m259.9-221.32h-56.025" stop-color="#000000"/><path d="m267.69-235.32h-63.714" stop-color="#000000"/><path d="m370.37-162.15c-21.473-37.192-42.946-74.385-64.419-111.58" stop-color="#000000"/><path d="m332-249.93h72.081" stop-color="#000000"/><path d="m348.25-221.93h56.025" stop-color="#000000"/><path d="m340.46-235.93h63.714" stop-color="#000000"/><path d="m240.88-162.15c21.473-26.526 42.946-53.051 64.419-79.577" stop-color="#000000"/></g><path d="m370.37-162.15c-21.473-26.526-42.946-53.051-64.419-79.577" stop-color="#000000"/></g><g fill="#eeeeec"><path d="m183.74-116.06-6.3858 17.316h12.795zm-2.6568-4.6378h5.337l13.261 34.795h-4.8942l-3.1696-8.9261h-15.685l-3.1696 8.9261h-4.9641z" style="text-decoration-color:#000000;text-decoration-line:none"/><path d="m222.66-120.7h4.7078v34.795h-4.7078z" style="text-decoration-color:#000000;text-decoration-line:none"/><path d="m271.14-102.22q1.5149.51273 2.9365 2.1907 1.445 1.678 2.8899 4.6145l4.7777 9.5087h-5.0573l-4.4514-8.9261q-1.7246-3.4959-3.356-4.6378-1.6081-1.142-4.4048-1.142h-5.1273v14.706h-4.7078v-34.795h10.627q5.9663 0 8.9028 2.4937t2.9365 7.5278q0 3.2861-1.5382 5.4535-1.5149 2.1674-4.4281 3.0064zm-11.793-14.613v12.352h5.9196q3.4026 0 5.1273-1.5615 1.7479-1.5848 1.7479-4.6378t-1.7479-4.5912q-1.7246-1.5615-5.1273-1.5615z" style="text-decoration-color:#000000;text-decoration-line:none"/><path d="m329.38-118.02v4.9641q-2.3772-2.214-5.0806-3.3094-2.6802-1.0954-5.7099-1.0954-5.9663 0-9.1358 3.659-3.1696 3.6357-3.1696 10.534 0 6.8752 3.1696 10.534 3.1696 3.6357 9.1358 3.6357 3.0297 0 5.7099-1.0954 2.7035-1.0954 5.0806-3.3094v4.9175q-2.4704 1.678-5.2438 2.517-2.7501.83901-5.8264.83901-7.9006 0-12.445-4.8243-4.5446-4.8476-4.5446-13.214 0-8.39 4.5446-13.214 4.5446-4.8476 12.445-4.8476 3.123 0 5.873.839 2.7734.8157 5.1972 2.4704z" style="text-decoration-color:#000000;text-decoration-line:none"/><path d="m366.18-116.06-6.3858 17.316h12.795zm-2.6568-4.6378h5.337l13.261 34.795h-4.8942l-3.1696-8.9261h-15.685l-3.1696 8.9261h-4.9641z" style="text-decoration-color:#000000;text-decoration-line:none"/><path d="m421.6-102.22q1.5149.51273 2.9365 2.1907 1.445 1.678 2.8899 4.6145l4.7777 9.5087h-5.0573l-4.4514-8.9261q-1.7246-3.4959-3.356-4.6378-1.6081-1.142-4.4048-1.142h-5.1272v14.706h-4.7078v-34.795h10.627q5.9663 0 8.9028 2.4937t2.9365 7.5278q0 3.2861-1.5382 5.4535-1.5149 2.1674-4.4281 3.0064zm-11.793-14.613v12.352h5.9196q3.4026 0 5.1272-1.5615 1.7479-1.5848 1.7479-4.6378t-1.7479-4.5912q-1.7246-1.5615-5.1272-1.5615z" style="text-decoration-color:#000000;text-decoration-line:none"/></g></g></svg>
        <h1>All Your Traffic Problems Solved!</h1>
        <h2>Feel the future with affordable levitating cars.</h2>
        <div class="content">
          {{ content }}
          {% if form %}
            <form action='.' method="post" class"enlist_form">
              {% csrf_token %}
              {{ form.non_field.errors }}
              {{ form.email.errors }}
              {{ form.referrer.errors }}
              {{ form.referrer }}
              {{ form.email }}
              <button type="submit">Add me</button>
            </form>
          {% endif %}
        </div>
      </div>
    </body>
  </html>
""")

if __name__ == "__main__":
  from django.core.management import execute_from_command_line

  execute_from_command_line(sys.argv)