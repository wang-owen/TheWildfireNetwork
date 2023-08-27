from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util


def index(request):
    if not request.session["postal"] or not request.session["city"]:
        user_ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
        if user_ip_address:
            ip = user_ip_address.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        try:
            g = GeoIP2()
            location = g.city("192.206.151.131")
            request.session["city"] = location["city"]
            request.session["postal"] = location["postal_code"]
        except:
            request.session["city"] = None
            request.session["postal"] = None

    location = util.Location(request.session["city"], request.session["postal"])
    return render(request, "home/index.html", {"response": location.getForecast()})


def changeLocation(request):
    return HttpResponse("Change Location")


def predict(request):
    if request.method == "POST":
        # verify if city and postal are valid
        form = predictForm(request.POST)
        if form.is_valid():
            request.session["postal"] = form.cleaned_data["postal"]
            request.session["city"] = form.cleaned_data["city"]
            return HttpResponseRedirect(reverse("index"))

    return render(request, "home/predict.html", {"predictForm": predictForm()})


class predictForm(forms.Form):
    postal = forms.CharField(label="Postal Code")
    city = forms.CharField(label="City")
