"""stonks_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import stonks.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/swiftness_products", stonks.views.SwiftnessProductList.as_view({"get": "list", "post": "create"})),
    path("api/v1/swiftness_deposits", stonks.views.SwiftnessDepositList.as_view({"get": "list", "post": "create"})),
    path("api/v1/swiftness_insurances", stonks.views.SwiftnessInsuranceList.as_view({"get": "list", "post": "create"})),
    path("api/v1/parse_swiftness_zip", stonks.views.ParseSwiftnessZip.as_view()),
    path("", include("rest_framework.urls")),  # Login and logout views
]
