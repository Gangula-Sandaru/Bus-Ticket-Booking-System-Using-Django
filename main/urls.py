from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bus/", views.bus, name="bus"),
    path("time table/", views.time_table, name="time table"),
    path("booking/<int:route_id>", views.booking, name="booking"),
    # path("select seat/", views.select_seat, name="select seat"),
    path("payment/", views.payment, name="payment"),
    path("contact us/", views.contact_us, name="contact us"),
    path("about us/", views.about_us, name="about us"),
    path("subscribe success/", views.subscribe_success, name="subscribe success"),
    path("payment success/", views.payment_success, name="payment success"),
    # path("jsonView/", views.jsonView, name="json")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # to set the media
