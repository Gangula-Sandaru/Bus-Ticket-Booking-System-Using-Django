from django.contrib import admin
from .models import Passenger

from .models import Bus
from .models import Routes
from .models import BusBookingDetails, newsAndUpdate, ticketRefund
from .models import PassengerPayment, BusTicket, PostDestinations, GiveFeedBack


admin.site.register(Passenger) # register table in the abmin pane

admin.site.register(Bus)
admin.site.register(Routes)
admin.site.register(BusBookingDetails)
admin.site.register(PassengerPayment)
admin.site.register(BusTicket)
admin.site.register(PostDestinations)
admin.site.register(GiveFeedBack)
admin.site.register(newsAndUpdate)
admin.site.register(ticketRefund)
