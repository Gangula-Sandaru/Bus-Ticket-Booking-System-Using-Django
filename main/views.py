import socket

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
import requests
from .models import Routes, Passenger, PostDestinations, BusBookingDetails, Bus, PassengerPayment, BusTicket, \
    ticketRefund
from .models import GiveFeedBack, SubEmail
from .forms import PassengerForm, CreditCardForm, FeedBackForm, EmailSubscriptionForm
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import serializers
from administration.models import monthlySales
import json
import datetime
from django.core.mail import send_mail, EmailMessage
import random
from django.utils import timezone
import qrcode
from administration.views import error_500

TMP_DATA_DIC = {}


# Create your views here.
def index(request):
    post_data = PostDestinations.objects.all()
    no_user = 0
    no_bus = Bus.objects.all().count()
    no_route = Routes.objects.all().count()
    no_book = 0

    monthly_satatictic = monthlySales.objects.all()
    for monthly in monthly_satatictic:
        no_user += monthly.user_qty
        no_book += monthly.total_ticket_qty


    if request.method == 'POST':
        feed_form = FeedBackForm(request.POST)
        subscription = EmailSubscriptionForm(request.POST)
        # f_name = request.POST['first_name']
        # print(f_name)
        print('fff ')
        if feed_form.is_valid():
            print('valid')
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            message = request.POST['message']

            print(f_name, l_name, message)

            # adding feedback details to the database
            feed_back_details = GiveFeedBack(first_name=f_name, last_name=l_name, message=message)
            feed_back_details.save()
            return redirect('index')

        elif subscription.is_valid():
            email = request.POST['email']
            email_list = SubEmail(email_name=email)
            email_list.save()
            return redirect('subscribe success')

    else:
        feed_form = FeedBackForm()
        subscription = EmailSubscriptionForm()

    # if request.method == 'POST':
    #     subscription = EmailSubscriptionForm(request.POST)
    #     sub = request.POST['email']
    #     print(sub)
    #     if subscription.is_valid():
    #         print("valid")
    # else:
    #     subscription = EmailSubscriptionForm()

    # for the test purpose
    data = BusBookingDetails.objects.filter(pk=2)

    for d in data:
        passeger = Passenger.objects.filter(pk=d.passengerID.passengerID)
        print(data)
        print(passeger)

    contex_dic = {"post_data": post_data,
                  "user_count": no_user,
                  "bus_count": no_bus,
                  "route_count": no_route,
                  "book_count": no_book,
                  "feed_back": feed_form,
                  "subscription": subscription
                  }

    return render(request, 'main/home.html', contex_dic)


def bus(request):
    return render(request, "main/bus.html", {})


def time_table(request):
    start_location = end_location = route_time = " "

    if request.method == "POST":
        start_location = request.POST['start_location']
        end_location = request.POST['end_location']
        route_time = request.POST['route_time']
        date = request.POST['date']
        route_no = request.POST['route']

        print(date)
        print(route_time)
        # search = response.POST['search']
        # route_t = Routes.objects.filter(route_s)

        print(start_location, end_location)
        if start_location and end_location and not date:
            current_date = datetime.date.today()
            route_search = Routes.objects.filter(
                start_location__contains=start_location,
                end_location__icontains=end_location,

            )
            print(route_search.values())
            return render(
                request, "main/Time table.html",
                {
                    'routes': route_search,
                    'start': start_location,
                    'end': end_location
                }
            )

        elif start_location and end_location and date and not route_time:
            print('kkkkk')
            date_str = str(date)
            data_list = date_str.split('-')
            print(data_list)
            route_search = Routes.objects.filter(
                start_location__contains=start_location,
                end_location__icontains=end_location,
                route_date__year=data_list[0],
                route_date__month=data_list[1],
                route_date__day=data_list[2],

            )
            print(route_search)
            return render(
                request, "main/Time table.html",
                {
                    'routes': route_search,
                    'start': start_location,
                    'end': end_location
                }
            )
        elif start_location and end_location and date and route_time or route_no:
            date_str = str(date)
            data_list = date_str.split('-')

            time_str = str(route_time)
            time_list = time_str.split(':')
            print(data_list)
            print(route_time)
            print(route_no)

            route_search = Routes.objects.filter(
                start_location__contains=start_location,
                end_location__icontains=end_location,
                route_date__year=data_list[0],
                route_date__month=data_list[1],
                route_date__day=data_list[2],
                # route_time__hour=time_list[0],
                # route_time__minute=time_list[1],
                # route_time__second=0,
                # route_time__hour=time_list[0],
                # route_time__minute=time_list[1],
                route_no__exact=route_no

            )

            print(route_search)
            return render(
                request, "main/Time table.html",
                {
                    'routes': route_search,
                    'start': start_location,
                    'end': end_location
                }
            )

        else:
            not_available = "Routes Not available, Search again"
            return render(request, "main/Time table.html", {'zero_result': not_available})

    else:
        return render(request, "main/time table.html", {})


def booking(request, route_id):
    # temporary data dic
    global TMP_DATA_DIC
    # forms = PassengerFrom()
    route_id = Routes.objects.get(pk=route_id)# getting the data id from database that according to the user click
    route_time = route_id.route_time
    print(route_time)
    bookdata = BusBookingDetails.objects.filter(bus_plate_no__bus_plate_no__contains=route_id, booking_status__exact=1)
    print(route_id.bus_plate_no.no_of_seat)
    no_of_seat = list(range(route_id.bus_plate_no.no_of_seat))  # print the seat according to the particular bus plate
    # print(str(route_id) +" fdf ")
    TMP_DATA_DIC['plate_no'] = str(route_id)

    data = list(BusBookingDetails.objects.values())
    data2 = json.dumps(data, indent=4, sort_keys=True, default=str)
    print(data2)

    # seat_data_list = BusBookingDetails.objects.filter(bus_plate_no__exact=route_id.bus_plate_no).filter(route_time_actual__exact=route_id.route_time)
    # print(seat_data_list)

    form = PassengerForm(request.POST)
    if request.method == "POST":  # check whether it's post request
        if form.is_valid():
            seat_list1 = request.POST.get('seat_list')
            print(seat_list1, 'ffffffff')
            if seat_list1 is None:
                print('ff')
            TMP_DATA_DIC['seat_list'] = seat_list1

            seat_data = request.POST['seat']
            TMP_DATA_DIC['seat_list'] = seat_data
            print(type(seat_data))
            user_nic = request.POST['nic']
            user_emailaddr = request.POST['emailaddr']
            user_info_list = [user_nic, user_emailaddr]
            TMP_DATA_DIC['user_info'] = user_info_list
            TMP_DATA_DIC['route_id'] = route_id.route_id
            me = TMP_DATA_DIC['user_info']
            # if form.is_valid() and not seat_list1 is None:
            return redirect('payment')

            # else:
            #     mgs = 'Please select your seat before continue.'
            #     return render(request, "main/booking.html",
            #                   {'form': form, 'route': route_id, 'booked': bookdata, 'route_id': route_id, 'json': data2,
            #                    'seat': no_of_seat, 'mgs':mgs})
        else:
            form = PassengerForm(request.POST)
    else:
        form = PassengerForm()

    # if request.method == "POST":
    #     seat_list1 = request.POST.get('seat_list')
    #     print(seat_list1, 'ffffffff')
    #     if seat_list1 is None:
    #         print('ff')
    #     TMP_DATA_DIC['seat_list'] = seat_list1
    #
    # else:
    #     PassengerForm()

    return render(request, "main/booking.html",
                  {'form': form, 'route': route_id, 'booked': bookdata, 'route_id': route_id, 'json':data2,
                   'seat': no_of_seat, 'route_time': str(route_time)})


def select_seat(request):
    return render(request, "main/select seat.html", {})


def payment(request):
    contex_dic = {}  # create contex dictionary
    user_info_pay = TMP_DATA_DIC.get('user_info')
    route_id = TMP_DATA_DIC.get('route_id')  # get user info and route id of the clicked route

    # calculate the total price of the ticket
    km_price = 4.50
    km = Routes.objects.filter(pk=route_id).values('total_distance')
    km_distance = 0
    for dis in km:
        km_distance = float(str(dis['total_distance']))

    total_amount = float(km_distance * km_price)
    print(user_info_pay)
    plate_no = Routes.objects.filter(pk=route_id).values('bus_plate_no')

    # get the seat list that user clicked
    seat_list = TMP_DATA_DIC.get('seat_list')
    print(seat_list, "ddd")

    # get data from the database which come from session
    r_id = Routes.objects.filter(pk=route_id).values('total_distance')
    departure = Routes.objects.filter(pk=route_id).values('start_location')
    destination = Routes.objects.filter(pk=route_id).values('end_location')

    # destination = Routes.objects.filter(star)
    departure1 = ''
    for depar in departure:
        departure1 = depar['start_location']

    destination1 = ''
    for desti in destination:
        destination1 = desti['end_location']

    for distance in r_id:
        print(distance['total_distance'])  # getting the total distance from the database

    # seat_list = seat_list
    # is_private = request.POST.get('is_private', False)

    seat_remove_1 = str(seat_list).replace("[", "")  # remove the [ from the json string
    seat_remove_2 = str(seat_remove_1).replace("]", "")  # remove the ] from the json string
    seat_remove_3 = str(seat_remove_2).replace('"', "")
    seat_3 = seat_remove_3.split(",")  # split the modified array from the , sign

    print(seat_3, "yyyyyy")

    # create 2 list for the seat show and book
    seat_no_list_show = []
    seat_no_list_book = []

    # get each tickets from the split list and show the tickets and book
    for list in seat_3:
        if list.isnumeric():
            seat_no_list_show.append(int(list) + 1)
            seat_no_list_book.append(int(list))

    # if the user porches more than one tickets , then calculate the total price of the all tickets
    total_price = len(seat_no_list_book) * total_amount

    # generate invoice and get the plate no
    plate = TMP_DATA_DIC.get('plate_no')

    print(route_id)

    try:
        try:
            requests.head(url="http://www.google.com",
                          timeout=2)  # check whether site has active internet connection.

            # this exception used for if the values does not exit in for the booking.
            route_cc = Routes.objects.get(pk=route_id).route_no

            invoice_list = []
            for invoice in range(0, len(seat_no_list_book)):
                random6digitno = random.randint(0, 1000000)
                invoice_id = plate + str(random6digitno)
                if not BusTicket.objects.filter(invoiceno__exact=invoice_id) or ticketRefund.objects.filter(
                        invoiceno__exact=invoice_id):  # check whether the invoice no is exits in the database.
                    invoice_list.append(invoice_id)
                elif BusTicket.objects.filter(invoiceno__exact=invoice_id) or ticketRefund.objects.filter(
                        invoiceno__exact=invoice_id):
                    continue

                print(random6digitno)
                print(invoice_list)
            # current date and time

            date = datetime.date.today()
            c_now = datetime.datetime.now()
            time = c_now.strftime("%H:%M:%S %p")
            # print(date, time)

            credit_card_data = CreditCardForm(request.POST)
            if request.method == "POST":
                if credit_card_data.is_valid():
                    #  booking.................
                    #  adding passenger details to the database
                    user_info = TMP_DATA_DIC.get('user_info')
                    passenger = Passenger(nic=user_info[0], emailaddr=user_info[1], agreement=1)
                    passenger.save()
                    # print(user_info)

                    #  adding booking details to the database
                    # last person who book the ticket
                    person_id = Passenger.objects.latest('passengerID').passengerID
                    # print(person_id, '56')

                    for book in range(int(len(seat_no_list_book))):
                        print("success.....")
                        route_time_data = Routes.objects.get(pk=route_id)
                        print(route_time_data)
                        booking_data = BusBookingDetails(bus_plate_no_id=plate_no,
                                                         passengerID_id=person_id, seat_no=seat_no_list_book[book],
                                                         booking_status=1, route_time_actual=route_time_data.route_time,
                                                         booked_date=route_time_data.route_date)
                        booking_data.save()
                        # getting the bus booking id
                        book_id = BusBookingDetails.objects.latest('bus_booking_id').bus_booking_id
                        payment_data = PassengerPayment(total_amount=total_price, description=None,
                                                        bus_booking_id_id=book_id, passengerID_id=person_id)
                        payment_data.save()
                        # ticket info
                        payment_id = PassengerPayment.objects.latest('payment_id').payment_id
                        current_date = datetime.datetime.now()
                        due_date = current_date + datetime.timedelta(days=2) # expire date

                        ticket_data = BusTicket(total_amount=total_price,
                                                company_name=" Jagath Industries",
                                                ticket_status=1,
                                                bus_plate_no_id=plate_no,
                                                passengerID_id=person_id,
                                                payment_id_id=payment_id,
                                                c_time=current_date,
                                                ticket_expire_date=due_date,
                                                invoiceno=invoice_list[book]
                                                )
                        ticket_data.save()
                        print(plate_no)
                        # generating the sms message
                        bus_route_no = Routes.objects.filter(pk=route_id).values('route_no')
                        print(bus_route_no)

                        ticket_id = BusTicket.objects.latest('ticket_id').ticket_id
                        ticket_qr = BusTicket.objects.get(pk=ticket_id).ticket_qr_code.file
                        print(ticket_qr)

                        message2 = """
                                                    <table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;" bgcolor="#f6f6f6">
                                    <tbody>
                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                            <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                                            <td class="container" width="600" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"
                                                valign="top">
                                                <div class="content" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
                                                    <table class="main" width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px solid #e9e9e9;"
                                                    bgcolor="#fff">
                                                        <tbody>
                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <td class="" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #38414a; margin: 0; padding: 20px;"
                                                                    align="center" bgcolor="#71b6f9" valign="top">
                                                                    <a href=" http://127.0.0.1:8000/" style="font-size:32px;color:#fff;"> QuickBooking.lk</a> <br>
                                                                    <span style="margin-top: 10px;display: block;">We make your journey easy what ever you go.</span>
                                                                </td>
                                                            </tr>
                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                <td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;" valign="top">
                                                                    <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <tbody>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" colspan="2" valign="top">
                                                                                    <h1 style="text-align:center;">Thanks for your Business!</h1>
                                                                                    <h3 style="text-align: center; color: #999;">Your Ticket</h3>
                                                                                </td>
                                                                            </tr>
                                                                            
                                                                    
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-right: 200px; padding-top: 5px;">NIC: </td>
                                                                                <td style="padding-top: 5px;"> """ + \
                                   user_info[0] + """ </td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-right: 200px; padding-top: 5px;">Invoice NO: </td>
                                                                                <td style="padding-top: 5px;">""" + \
                                   invoice_list[book] + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-top: 5px;">Vehicale No: </td>
                                                                                <td style="padding-top: 5px;">""" + plate + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-top: 5px;">Bus Route NO: </td>
                                                                                <td style="padding-top: 5px;">""" + str(
                            route_cc) + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-top: 5px;">Departure: </td>
                                                                                <td style="padding-top: 5px;">""" + departure1 + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-top: 5px;">Destination: </td>
                                                                                <td style="padding-top: 5px;">""" + destination1 + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-top: 5px;">Seat No: </td>
                                                                                <td style="padding-top: 5px;">""" + str(
                            seat_no_list_book[book]) + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0; border-bottom: 2px solid #38414a;">
                                                                                <td style="padding-top: 5px;">Total Amount: </td>
                                                                                <td style="padding-top: 5px;">Rs. """ + str(
                            total_amount) + """</td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0; border-bottom: 2px solid #38414a;">
                                                                                <td style="padding-top: 5px;">Date: </td>
                                                                                <td style="padding-top: 5px;">""" + str(
                            date) + """</td>
    
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0; border-bottom: 2px solid #38414a;">
                                                                                <td style="padding-top: 5px;">Time: </td>
                                                                                <td style="padding-top: 5px;">""" + str(
                            time) + """</td
                                                                            </tr>
    
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px; text-align: center; padding-top: 30px;" valign="top" colspan="2">
                                                                                    <a href="#" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">View QuickBooking.lk</a>
                                                                                </td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; text-align: center; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px; background-color: rgb(1, 151, 144); color: #e9e9e9; padding: 5px;" colspan="2" valign="top">
                                                                                    <h3 style="text-align: center;">Connect with our social media links</h3>
                                                                                    Connect with our social media to get the latest news and updates.
                                                                                </td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px; text-align: center; padding-top: 30px;" colspan="2" valign="top">Thank for being a great customer. <br>
                                                                                    This email has been generated by the system. Do not replay to this email.
    
                                                                                </td>
    
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                    <div class="footer" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;">
                                                        <table width="100%" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <tbody>
                                                                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
    
                                                                    <td class="aligncenter content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; vertical-align: top; color: #999; text-align: center; margin: 0;" align="center" valign="top">If you have any problem with the details, please kindly contact our <a href=" http://127.0.0.1:8000/" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; color: #999; text-decoration: underline; margin: 0;">QuickBooking</a> Team.
                                                                    <p class="aligncenter content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; vertical-align: top; color: #999; text-align: center; margin: 0; padding: 0 0 20px;" align="center" valign="top"><a href=" http://127.0.0.1:8000/" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; color: #999; text-decoration: underline; margin: 0;">QuickBooking.lk</a>, No.54 Mathugama Road, Colombo, Sri Lanka. </p>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </td>
                                            <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                                        </tr>
                                    </tbody>
                                </table>
    
                                                """

                        # bus_route_no = busDetails.objects.filter(bus_route_no)
                        message = ("   .......Ticket information........\n\n" +
                                   "Nic no: " + user_info[0] + "\n" +
                                   "Telephone No: " + user_info[1] + "\n" +
                                   "Bus route No: " + str(bus_route_no[0]) + "\n" +
                                   "Ticket invoice: " + "\n" +
                                   "Price: " + str(total_price) + "\n" +
                                   "Date: " + str(date) + "\n" +
                                   "Time: " + str(time) + "\n"
                                   )
                        try:
                            #
                            # send_mail(
                            #     subject='Your ticket issued from QuickBooking.com',
                            #     message=message,
                            #     from_email='quickbooking.lk@gmail.com',
                            #     recipient_list=[user_info[1]],
                            #     fail_silently=False,
                            #     html_message=message2,
                            #
                            # )

                            subject = 'Your ticket issued from QuickBooking.com'
                            mgs = "your ticket has been issued"

                            mail = EmailMessage(subject, message2, 'quickbooking.lk@gmail.com', [user_info[1]])
                            mail.attach_file(
                                "set your absolute path. C:/example/example/media/media/" +
                                invoice_list[book] + "-qr.png")
                            mail.content_subtype = "html"

                            mail.send()

                            success_mgs = 'success'
                            print(message)
                        except socket.gaierror:
                            return redirect('error_400')

                    return redirect('payment success')
            else:
                credit_card_data = CreditCardForm()

            contex_dic = {
                "user_nic": user_info_pay[0],
                "user_phone_no": user_info_pay[1],
                "price": total_price,
                "credit_card_from": credit_card_data,
                "seat_no": seat_no_list_show,
                "invoce_id": invoice_list,
                "date": date,
                "time": time,

            }
        except requests.ConnectionError or requests.ConnectTimeout:
            return redirect('error_400')
    except Routes.DoesNotExist or ValueError:
        return redirect('error_500')

    return render(request, "main/payment.html", contex_dic)
    # return JsonResponse({"massage": "request handled"})


def contact_us(request):
    return render(request, "main/contact us.html", {})


def about_us(request):
    return render(request, "main/about us.html", {})


def jsonView(request):
    # data = list(BusBookingDetails.objects.values())
    # data2 = json.dumps(data,indent=4, sort_keys=True, default=str)
    # data2 = json.dumps(data, indent=4, sort_keys=True, default=str)
    # print(data2)
    return render(request, "main/json.html", {})


def subscribe_success(request):
    return render(request, "main/subscribe_success.html", {})


def payment_success(request):
    return render(request, "main/payment_success.html", {})
