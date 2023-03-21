import qrcode
from django.db import models
from django.db.models import Model
from ckeditor.fields import RichTextField

from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from administration.manager import ticketManager
from django.contrib.auth.models import User


# Create your models here.


# class Owner(models.Model):  # this is the table for owner
#     userName = models.CharField(db_column="userName", primary_key=True, max_length=20)
#     firstName = models.CharField(db_column="firstName", max_length=20)
#     lastName = models.CharField(db_column="lastName", max_length=20, null=True)
#     dob = models.DateField(db_column="dob", blank=True, null=True)
#     email = models.EmailField(db_column="email", max_length=50, blank=True, null=True)
#     country = models.CharField(db_column="country", max_length=30, null=True)
#     passwd = models.CharField(db_column="passwd", max_length=50)
#     contactNo = models.CharField(db_column="contactNo", max_length=10, blank=True, null=True)
#     hotLine = models.CharField(db_column="hotline", max_length=10, blank=True, null=True)
#     otherDetails = models.CharField(db_column="otherDetails", max_length=200, blank=True, null=True)
#     accountStatus = models.BooleanField(db_column="accStatus", blank=True, null=True)
#
#     class Meta:
#         db_table = "owner"
#
#     def __str__(self):
#         return self.userName


class Bus(models.Model):  # this is the bus table
    bus_plate_no = models.CharField(db_column="busPlateNo", max_length=20, primary_key=True)
    driver_name = models.CharField(db_column="driverName", max_length=50, blank=True, null=True)
    no_of_seat = models.IntegerField(db_column='no_of_seat', blank=True, null=True)
    vehicle_status = models.BooleanField(db_column="vehicleStatus", blank=True, null=True)
    contact_no = models.CharField(db_column="contactNo", max_length=10, blank=True, null=True)
    other_details = models.TextField(db_column="otherDetails", max_length=200, blank=True, null=True)
    # userName = models.ForeignKey(Owner, models.DO_NOTHING, db_column="userName", blank=True, null=True)
    register_date = models.DateTimeField(db_column='registerdate', auto_now_add=True, null=True)
    userName = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column="userName", blank=True, null=True)

    class Meta:
        db_table = "bus"

    def __str__(self):
        return self.bus_plate_no


#
# class busDetails(models.Model):
#     bus_data_id = models.AutoField(db_column="busDataId", primary_key=True)
#     bus_plate_no = models.ForeignKey(Bus, db_column="busPlateNo", on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'bus_details'
#
#     def __str__(self):
#         bus_plate = str(self.bus_plate_no)
#         return bus_plate


class Routes(models.Model):
    route_id = models.AutoField(db_column="route_id", primary_key=True)
    route_no = models.CharField(db_column="routeNo", default="None", max_length=10, blank=True, null=True)
    start_location = models.CharField(db_column="startLocation", default="None", max_length=25, blank=True, null=True)
    end_location = models.CharField(db_column="endLocation", default="None", max_length=25, blank=True, null=True)
    route_date = models.DateField(db_column="routeDate", blank=True, null=True)
    route_time = models.TimeField(db_column="routeTime", blank=True, null=True)
    total_distance = models.DecimalField(db_column="totalDistance", decimal_places=2, max_digits=8, blank=True,
                                         null=True, max_length=10)
    # avg_run_time = models.DecimalField(db_column="avgRunTime", decimal_places=2, blank=True, max_digits=4, null=True,
    #                                    max_length=5)
    route_status = models.BooleanField(db_column="vehicleStatus", blank=True, null=True)
    # if the user delete the owner table it will not delete the name of the user in the bus column
    bus_plate_no = models.ForeignKey(Bus, db_column='busPlateNo', on_delete=models.CASCADE)
    c_time = models.DateField(db_column="c_time", blank=True, auto_now_add=True)
    route_available = models.BooleanField(db_column='route_available', blank=True, null=True)

    class Meta:
        db_table = 'routes'

    def __str__(self):
        bus_plate = str(self.bus_plate_no)
        return bus_plate


class Passenger(models.Model):
    passengerID = models.AutoField(db_column='PassengerDetailId', primary_key=True)
    nic = models.CharField(db_column='nic', max_length=12)
    # firstname = models.CharField(db_column='firstName', max_length=20)
    # lastname = models.CharField(db_column='lastName', max_length=20, blank=True, null=True)
    emailaddr = models.CharField(db_column='emailaddr', max_length=50, blank=True, null=True)
    # gender = models.BooleanField(db_column='gender', choices=(("1", "Male"), ("2", "Female")))
    agreement = models.BooleanField(db_column='agreement', default=0)
    select_bus = models.ManyToManyField(Bus)
    userSelectRoutes = models.ManyToManyField(Routes)
    passenger_count = models.BooleanField(db_column='passenger_qty', blank=True, null=True, default=0)

    # userSearch_taxi = models.ManyToManyField(Taxi, null=True, blank=True)

    class Meta:
        db_table = 'passenger'

    def __str__(self):
        return self.nic


class BusBookingDetails(models.Model):
    bus_booking_id = models.AutoField(db_column='bus_booking_id', primary_key=True)
    seat_no = models.IntegerField(db_column='seat_no')
    passengerID = models.ForeignKey(Passenger, models.DO_NOTHING, db_column='PassengerDetailId')
    bus_plate_no = models.ForeignKey(Bus, models.DO_NOTHING, max_length=20, db_column='busPlateNo')
    # seat_id = models.ForeignKey(BusSeat, models.DO_NOTHING, db_column='seat_id')
    booking_status = models.BooleanField(db_column='booking_status', blank=True, null=True, default=0)
    route_time_actual = models.TimeField(db_column="routeTime", blank=True, null=True)
    c_time = models.DateTimeField(db_column='c_time', blank=True, auto_now_add=True)
    booked_date = models.DateField(db_column='booked_date', blank=True, null=True)

    class Meta:
        db_table = 'bus_booking_details'

    def __str__(self):
        return self.passengerID.nic


class PassengerPayment(models.Model):
    payment_id = models.AutoField(db_column='payment_id', primary_key=True)
    passengerID = models.ForeignKey(Passenger, models.DO_NOTHING, db_column='passengerID')
    bus_booking_id = models.ForeignKey(BusBookingDetails, models.DO_NOTHING, db_column='bus_booking_id')
    # taxi_book_id = models.ForeignKey(TaxiBookingDetails, models.DO_NOTHING, db_column='taxi_book_id')
    # card_type = models.BooleanField(db_column='card_type')
    total_amount = models.IntegerField(db_column='total_amount', blank=True, null=True)
    description = models.TextField(db_column='description', max_length=200, blank=True, null=True)
    c_time = models.DateTimeField(db_column='c_time', blank=True, auto_now_add=True)

    class Meta:
        db_table = 'passenger_payment'

    def __str__(self):
        return self.passengerID.nic


class BusTicket(models.Model):
    ticket_id = models.AutoField(db_column='ticket_id', primary_key=True)
    passengerID = models.ForeignKey(Passenger, models.DO_NOTHING, db_column='passengerID')
    bus_plate_no = models.ForeignKey(Bus, models.DO_NOTHING, db_column='bus_plate_no')
    # seat_id = models.ForeignKey(BusSeat, models.DO_NOTHING, db_column='seat_id')
    payment_id = models.ForeignKey(PassengerPayment, models.DO_NOTHING, db_column='payment_id')
    total_amount = models.IntegerField(db_column='total_amount', blank=True, null=True)
    company_name = models.CharField(db_column='company_name', max_length=30, blank=True, null=True)
    ticket_status = models.IntegerField(db_column="ticket_status", default=1)
    c_time = models.DateTimeField(db_column='c_time', blank=True)
    ticket_expire_date = models.DateTimeField(db_column='expire_date', blank=True, null=True)
    invoiceno = models.CharField(db_column='invoice', max_length=15, blank=True,
                                 null=True)  # todo remove the blank and null
    ticket_counted = models.BooleanField(db_column='ticket_count', blank=True, null=True, default=0)
    ticket_refund_counted = models.BooleanField(db_column='ticket_refund_counted', blank=True, null=True, default=0)
    ticket_used_counted = models.BooleanField(db_column='ticket_used_counted', blank=True, null=True, default=0)
    ticket_cancel_counted = models.BooleanField(db_column='ticket_cancel_counted', blank=True, null=True, default=0)
    ticket_qr_code = models.ImageField(db_column='qr_code', blank=True, null=True, upload_to='media/')

    # object = ticketManager()

    class Meta:
        db_table = 'bus_ticket'

    def __str__(self):
        return self.passengerID.nic

    def save(self, *args, **kwargs):
        data = self.invoiceno

        qr_image = qrcode.make(data)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        draw_img = ImageDraw.Draw(qr_offset)
        qr_offset.paste(qr_image)
        file_name = f'{self.invoiceno}-qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.ticket_qr_code.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)

    @staticmethod  # filters
    def get_all_tickets():
        return BusTicket.objects.all().order_by('-c_time')

    @staticmethod
    def get_pennding_ticket(status):
        return BusTicket.objects.filter(ticket_status__exact=status)


class ticketRefund(models.Model):
    ticket_id = models.AutoField(db_column='ticket_id', primary_key=True)
    passengerID = models.ForeignKey(Passenger, models.DO_NOTHING, db_column='passengerID')
    bus_plate_no = models.ForeignKey(Bus, models.DO_NOTHING, db_column='bus_plate_no')
    # seat_id = models.ForeignKey(BusSeat, models.DO_NOTHING, db_column='seat_id')
    payment_id = models.ForeignKey(PassengerPayment, models.DO_NOTHING, db_column='payment_id')
    total_amount = models.IntegerField(db_column='total_amount', blank=True, null=True)
    company_name = models.CharField(db_column='company_name', max_length=30, blank=True, null=True)
    ticket_status = models.IntegerField(db_column="ticket_status", default=1)
    c_time = models.DateTimeField(db_column='c_time', blank=True)
    ticket_expire_date = models.DateTimeField(db_column='expire_date', blank=True, null=True)
    invoiceno = models.CharField(db_column='invoice', max_length=15, blank=True,
                                 null=True)  # todo remove the blank and null
    ticket_counted = models.BooleanField(db_column='ticket_count', blank=True, null=True, default=0)
    ticket_qr_code = models.ImageField(db_column='qr_code', blank=True, null=True, upload_to='media/')

    class Meta:
        db_table = 'refund_ticket'

    def __str__(self):
        return self.passengerID.nic

    @staticmethod  # filters
    def get_all_tickets():
        return ticketRefund.objects.all().order_by('-c_time')


# additional tables
class PostDestinations(models.Model):
    Post_id = models.AutoField(db_column='post_id', primary_key=True)
    head_line = models.TextField(db_column='head_line', max_length=100)
    picture = models.ImageField(db_column='picture', null=True, blank=True)
    picture_url = models.URLField(db_column='picture_url', null=True, blank=True)
    description = models.TextField(db_column='description', max_length=300)
    c_time = models.DateTimeField(db_column='current_time', auto_now_add=True, blank=True)
    userName = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column="userName", blank=True, null=True)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.head_line


class GiveFeedBack(models.Model):
    feed_back_id = models.AutoField(db_column='feed_back_id', primary_key=True)
    first_name = models.CharField(db_column='first_name', max_length=25)
    last_name = models.CharField(db_column='last_name', max_length=25)
    message = models.CharField(db_column='message', max_length=500)
    message_status = models.IntegerField(db_column='status', default=0)
    message_date = models.DateTimeField(db_column='date', auto_now_add=True)

    # owner_name = models.ForeignKey(Owner, models.DO_NOTHING, db_column="userName")

    class Meta:
        db_table = 'feed_back'

    def __str__(self):
        return self.first_name + " " + self.last_name


class SubEmail(models.Model):
    # sub_id = models.AutoField(db_column='sub_id' )
    email_name = models.EmailField(db_column='email_address', primary_key=True)
    # reg_date = models.DateTimeField(db_column='date', auto_now_add=True)

    class Meta:
        db_table = 'email_subscription'

    def __str__(self):
        return self.email_name


class newsAndUpdate(models.Model):
    newsandupdate_id = models.AutoField(primary_key=True, db_column='newsandupdate_id')
    subject = models.CharField(db_column='subject', max_length=200)
    email = RichTextField(blank=True, null=True)

    class Meta:
        db_table = 'newsandupdate'

    def __str__(self):
        return self.subject
