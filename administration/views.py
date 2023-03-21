from datetime import datetime, timedelta
import datetime
import decimal
import socket
import requests
import django.db.utils
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main.models import BusTicket, Bus, Routes, SubEmail, GiveFeedBack, Passenger, ticketRefund
from .models import monthlySales
from .forms import LoginForm, busRegForm, routeRegForm, newsandupdateForm, ticket_searchForm, RegisterForm, \
    bus_searchForm
from .forms import del_form, del_form2, del_form3, feed_back_reviewed, make_refund

from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
import json
import time
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from administration.utils import get_the_current_date_as_list, get_the_current_date, get_the_current_date_p

TMP_DATA_DIC = {}


# Create your views here.
def base(request):
    superusers = User.objects.filter(is_superuser=True)

    return render(request, "Administration/base.html", {"superuser": superusers})


def adminView(request):
    loginForm = LoginForm(request.POST)
    if request.method == "POST":
        if loginForm.is_valid():
            userName = request.POST['userName']
            passwd = request.POST['passwd']
            user = authenticate(request, username=userName, password=passwd)
            superusers = User.objects.filter(username=user).filter(is_superuser=True)
            print(request)
            print(superusers)
            if user is not None:
                login(request, user)
                return redirect('adminDashboard')

            # elif user is not None and not user.is_superuser:
            #     login(request, user)
            #     return redirect('adminDashboard')

            else:
                messages.success(request, 'Invalid username or password, please try again')
                return redirect('adminView')

    else:
        loginForm = LoginForm()
        return render(request, "Administration/login.html", {"loginfrom": loginForm})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            if username and password and email:
                form.save()
                user = authenticate(request, username=username, password=password)
                # login(request, user)
                print(password)
                print(email)
                # messages.success(request, "Registration successful.")
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
                                                                        <td style="padding-right: 200px; padding-top: 5px;">Name: </td>
                                                                        <td style="padding-top: 5px;"><img src=''  ></td>
                                                                    </tr>
                                                                  
                                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <td style="padding-right: 200px; padding-top: 5px;">Username: </td>
                                                                        <td style="padding-top: 5px;"> """ + \
                           username+ """ </td>
                                                                    </tr>
                                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                        <td style="padding-right: 200px; padding-top: 5px;">Password: </td>
                                                                        <td style="padding-top: 5px;"> """ + \
                           password+ """ </td>
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

                try:
                    requests.head(url="http://www.google.com",
                                  timeout=2)
                    # time.sleep(5)
                    send_mail(
                        subject="Your Driver Account has been created successfully.",
                        message='',
                        from_email='gangula.dinu@gmail.com',
                        recipient_list=[str(email)],
                        fail_silently=False,
                        # html_message="<p> Your Driver <b> Account's Username </b> name is " + username + " and <br> <b> Password </b> is " + password + ".</p>"
                        html_message= message2
                    )
                    return redirect('register_success')
                except requests.ConnectionError or requests.ConnectTimeout:
                    return redirect('error_400')

        # messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, "Administration/register.html", {"register_form": form})


def registration_success(request):
    return render(request, 'Administration/registration_success.html', {})


def logout_site(request):
    logout(request)
    return redirect('adminView')


def adminDashboard(request):
    # 2022-01-03 - 2022-01-04

    ticket_info = []
    daily_track = []
    ticket_data = BusTicket.objects.all().order_by('-c_time')[:5]  # show sending order of the tickets issue dates
    # monthlySales.calculate_daily_sales()  # calculate daily earning

    current_date = str(datetime.date.today())
    date_c = current_date.split('-')  # take current day earnings.
    current_day_records = monthlySales.objects.filter(sale_id__year=date_c[0], sale_id__month=date_c[1],
                                                      sale_id__day=date_c[2])
    daily_earn = 0
    for daily_earn in current_day_records:
        daily_earn = daily_earn.daily_sale

    # show and calculate monthly sales

    #  get the current time
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    current_day = datetime.date.today().day

    #  format the current time as verified time input
    current_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)
    try:
        monthly_total = monthlySales.objects.get(pk=current_date)

        if monthly_total.sale_id == datetime.date.today():  # pie chart data update

            used_ticket = monthly_total.used_ticket_qty
            ticket_info.append(used_ticket)
            cancel_ticket = monthly_total.cancel_ticket_qty
            ticket_info.append(cancel_ticket)
            refund_ticket = monthly_total.refund_ticket_qty
            ticket_info.append(refund_ticket)
            pending_ticket = monthly_total.pending_ticket_qty
            ticket_info.append(pending_ticket)

        monthly_total = monthlySales.objects.all()

        for daily_satatic in monthly_total:  # line chart data update
            daily_track.append(float(daily_satatic.daily_sale))

    except monthlySales.DoesNotExist:
        assign_sale_key = monthlySales(sale_id=current_date)
        assign_sale_key.save()
        return render(request, "Administration/adminDashboard.html", {"tickets": ticket_data,
                                                                      "daily_earn": daily_earn,
                                                                      'ticket': ticket_info,
                                                                      "dailay_track": daily_track})

    return render(request, "Administration/adminDashboard.html", {"tickets": ticket_data,
                                                                  "daily_earn": daily_earn,
                                                                  'ticket': ticket_info,
                                                                  "dailay_track": daily_track})


def get_static(request):
    data = monthlySales.objects.all()

    return JsonResponse({"datalist": list(data.values())})


def busRegistration(request):
    # get_yesterday_date = str(datetime.date.today() - timedelta(days=1)).split('-')
    # get_today_date = str(datetime.date.today()).split('-')
    # get_tomorrow_date = str(datetime.date.today() + timedelta(days=1)).split('-')
    #
    # print(get_yesterday_date)
    # print(get_today_date)
    # print(get_tomorrow_date)
    #
    # get_yesterday_routes = Routes.objects.filter(
    #     route_date__year=get_yesterday_date[0],
    #     route_date__month=get_yesterday_date[1],
    #     route_date__day=get_yesterday_date[2],
    # )
    # get_today_routes = Routes.objects.filter(
    #     route_date__year=get_today_date[0],
    #     route_date__month=get_today_date[1],
    #     route_date__day=get_today_date[2],
    # )
    # print(get_yesterday_routes)
    # print(get_today_routes)

    # test code 33333333333333333333333333333333333333333333

    user = request.user
    print(user, 'kk')
    if request.method == "POST":
        busform = busRegForm(request.POST)
        if busform.is_valid():
            print("valid")
            plate_no = request.POST['bus_plate_no']
            driver_name = request.POST['driver_name']
            no_of_seat = request.POST['no_of_seat']
            vehicle_status = request.POST['vehicle_status']
            contact_no = request.POST['contact_no']
            other_details = request.POST['other_details']

            # remove if any dash
            modify_contact = str(contact_no).replace("-", "")
            if not Bus.objects.filter(bus_plate_no__exact=plate_no):
                bus_data = Bus(
                    bus_plate_no=plate_no,
                    driver_name=driver_name,
                    userName=request.user,
                    no_of_seat=no_of_seat,
                    vehicle_status=vehicle_status,
                    contact_no=modify_contact,
                    other_details=other_details,
                )
                bus_data.save()
                time.sleep(3)
                return redirect('route registration')
            else:
                messages.error(request, "Bus Number Plate Already Exit!")

        #
        # elif not busform.is_valid():
        #     return render(request, "Administration/bus_registration.html", {"busfrom": busform})

    else:
        busform = busRegForm()

    return render(request, "Administration/bus_registration.html", {"busfrom": busform})


def routeRegistration(request):
    if request.method == "POST":
        routeform = routeRegForm(request.POST)
        # route_time = request.POST['route_time']
        # print(route_time)
        if routeform.is_valid():
            print('valid')
            bus_plate_no = request.POST['plate_no']

            route_no = request.POST['route_no']
            start_location = request.POST['start_location']
            end_location = request.POST['end_location']
            route_date = request.POST['route_date']  # todo this code will blow up. fix this/ date and time
            route_time = request.POST['route_time']
            total_distance = request.POST['total_distance']
            # avg_run_time = request.POST['avg_run_time']
            route_status = request.POST['route_status']
            # route_avl = request.POST['route_available']
            # print(route_avl, '44') # todo remove booloadn field
            print(route_time)
            add_new_routes = Routes(
                bus_plate_no=Bus(bus_plate_no=bus_plate_no),
                route_no=route_no,
                start_location=start_location,
                end_location=end_location,
                route_date=route_date,
                route_time=str(route_time),
                total_distance=total_distance,
                # avg_run_time=avg_run_time,
                route_status=route_status,
                # route_available=route_avl,
            )

            add_new_routes.save()
            routeform = routeRegForm()
            messages.success(request, 'Data added successfully into the database.')

    else:
        routeform = routeRegForm()
    return render(request, "Administration/route_registration.html", {"routeform": routeform})


# def handel_not_found(request, exception):
#     return render(request, "Administration/404.html", {})


def newsLatters(request):
    if request.method == "POST":
        newsform = newsandupdateForm(request.POST)
        subject = request.POST['subject']

        if newsform.is_valid():
            mgs = request.POST['edit']
            user_mail_addr = SubEmail.objects.all()
            # email_list = []
            try:
                for mail in user_mail_addr:
                    send_mail(
                        subject=subject,
                        message='',
                        from_email='gangula.dinu@gmail.com',
                        recipient_list=[str(mail)],
                        fail_silently=False,
                        html_message=mgs
                    )
            except socket.gaierror:
                return redirect('error_400')

            messages.success(request, 'The mails has been send successfully')
            newsform = newsandupdateForm()

            return redirect('news latter success')
    else:

        newsform = newsandupdateForm()
        return render(request, "Administration/news_latter.html", {"newsform": newsform})

    return render(request, "Administration/news_latter.html", {"newsform": newsform})


def news_latter_success(request):
    return render(request, "Administration/news_latter_success.html", {})


def inquiry(request):
    feed_back = GiveFeedBack.objects.all()
    total = GiveFeedBack.objects.all().count()
    total_pending = GiveFeedBack.objects.filter(message_status__exact=0).count()
    total_complete = GiveFeedBack.objects.filter(message_status__exact=1).count()
    data = list(GiveFeedBack.objects.values())
    feed_back_pop = json.dumps(data, indent=4, sort_keys=True, default=str)

    all_ticket = BusTicket.get_all_tickets()
    filter_ok = request.GET.get("inquiry_data")
    if filter_ok:
        result = GiveFeedBack.objects.filter(message_status__exact=filter_ok)

        return render(request, "Administration/inquiry.html", {"total": total,
                                                               "total_pending": total_pending,
                                                               "total_complete": total_complete,
                                                               "inquiry_data": result,
                                                               "feed_back_popup": feed_back_pop,
                                                               # "feedback_del": form,
                                                               # "feedback_reviewd": reviewd
                                                               })

    if request.method == "POST":
        form = del_form3(request.POST)
        reviewd = feed_back_reviewed(request.POST)
        if form.is_valid():
            del_feedback_id = request.POST.get('del_feedback')
            feedback_del = GiveFeedBack.objects.filter(feed_back_id__exact=del_feedback_id)
            feedback_del.delete()

            messages.success(request, "Delete Successfully.")

            return redirect("inquiry")


    else:
        form = del_form3()
        reviewd = feed_back_reviewed()

    return render(request, "Administration/inquiry.html",
                  {"total": total,
                   "total_pending": total_pending,
                   "total_complete": total_complete,
                   "inquiry_data": feed_back,
                   "feed_back_popup": feed_back_pop,
                   "feedback_del": form,
                   "feedback_reviewd": reviewd
                   }
                  )


def feedback_reviewed(request):
    if request.method == "POST":
        reviewd = feed_back_reviewed(request.POST)
        if reviewd.is_valid():
            if reviewd.is_valid():
                reviewd = request.POST.get('feedback_reviewed')
                messages.success(request, "Reviewed Successfully.")
                make_review = GiveFeedBack.objects.get(pk=reviewd)
                make_review.message_status = 1
                make_review.save()
                return redirect("inquiry")


# def inquiry_delete(request, id):
#     delete_record = GiveFeedBack.objects.get(pk=id)
#     print("im in")
#     if request.method == "POST":
#         form = del_form3(request.POST)
#         if form.is_valid():
#             print("in ddd")
#             delete_record.delete()
#             return redirect('inquiry')
#
#
#     else:
#         form = del_form3()
#
#     context_dic = {
#         "delete": delete_record,
#         "feedback_del": form,
#     }
#
#     return render(request, "Administration/inquiry_delete.html", context_dic)


# def filter_pending(request):
#     pending = GiveFeedBack.objects.filter(message_status__exact=0)
#     print(pending)
#
#     return render(request, "Administration/inquiry.html", {"feed": pending})


def ticket(request):
    total = BusTicket.objects.all().count()
    total_ticket = monthlySales.objects.all()

    ticket_pending = 0
    ticket_used = 0
    ticket_refund = 0
    ticket_cancel = 0
    total = 0

    for ticket_values in total_ticket:
        if not ticket_values.pending_ticket_qty == None:
            ticket_pending += ticket_values.pending_ticket_qty
            ticket_used += ticket_values.used_ticket_qty
            ticket_refund += ticket_values.refund_ticket_qty
            ticket_cancel += ticket_values.cancel_ticket_qty
            total += ticket_values.total_ticket_qty

    total_pending = ticket_pending
    total_Used = ticket_used
    total_Refund = ticket_refund

    # else:
    #     all = BusTicket.objects.all()
    #     return render(request, "Administration/ticket.html", {"ticket_pending": all})
    # return reverse(request, 'ticket')

    if request.method == "POST":
        searchFrom = ticket_searchForm(request.POST)
        if searchFrom.is_valid():
            result = request.POST['search_from']
            if result:
                all_ticket = BusTicket.objects.filter(invoiceno__exact=result)
                if len(all_ticket) == 0:
                    all_ticket = ticketRefund.objects.filter(invoiceno__exact=result)
                    if len(all_ticket) == 0:
                        message = "There is no any matching Invoices"
                        return render(request, "Administration/ticket.html",
                                      {"total": total,
                                       "total_pending": total_pending,
                                       "total_used": total_Used,
                                       "total_Refund": total_Refund,
                                       "ticket_pending": all_ticket,
                                       "ticket_search_from": searchFrom,
                                       "cancel": ticket_cancel,
                                       "mgs": message
                                       }
                                      )
    # todo complate search invalid

    all_ticket = BusTicket.get_all_tickets()
    filter_ok = request.GET.get("ticket_pending")
    if filter_ok:
        result = BusTicket.objects.filter(ticket_status__exact=filter_ok)
        return render(request, "Administration/ticket.html",
                      {"total": total,
                       "total_pending": total_pending,
                       "total_used": total_Used,
                       "total_Refund": total_Refund,
                       "ticket_pending": result,
                       # "ticket_search_from": searchFrom,
                       "cancel": ticket_cancel,
                       # "mgs": message
                       }
                      )

    searchFrom = ticket_searchForm()

    return render(request, "Administration/ticket.html",
                  {"total": total,
                   "total_pending": total_pending,
                   "total_used": total_Used,
                   "total_Refund": total_Refund,
                   "ticket_pending": all_ticket,
                   "ticket_search_from": searchFrom,
                   "cancel": ticket_cancel,
                   # "mgs": message
                   }
                  )


def older_ticket_details(request):
    total_ticket = monthlySales.objects.all()

    ticket_pending = 0
    ticket_used = 0
    ticket_refund = 0
    ticket_cancel = 0
    total = 0
    for ticket_values in total_ticket:
        if not ticket_values.pending_ticket_qty == None:
            ticket_pending += ticket_values.pending_ticket_qty
            ticket_used += ticket_values.used_ticket_qty
            ticket_refund += ticket_values.refund_ticket_qty
            ticket_cancel += ticket_values.cancel_ticket_qty
            total += ticket_values.total_ticket_qty

    total_pending = ticket_pending
    total_Used = ticket_used
    total_Refund = ticket_refund

    # total_pending = BusTicket.objects.filter(ticket_status__exact=1).count()

    # else:
    #     all = BusTicket.objects.all()
    #     return render(request, "Administration/ticket.html", {"ticket_pending": all})
    # return reverse(request, 'ticket')

    if request.method == "POST":
        searchFrom = ticket_searchForm(request.POST)
        if searchFrom.is_valid():
            result = request.POST['search_from']
            if result:
                all_ticket = ticketRefund.objects.filter(invoiceno__exact=result)
                if len(all_ticket) == 0:
                    all_ticket = ticketRefund.objects.filter(invoiceno__exact=result)

            # todo complete search invalid

    searchFrom = ticket_searchForm()

    all_ticket = ticketRefund.get_all_tickets()
    filter_ok = request.GET.get("ticket_pending")
    if filter_ok:
        result = ticketRefund.objects.filter(ticket_status__exact=filter_ok)
        return render(request, "Administration/older_ticket_data.html",
                      {"total": total,
                       "total_pending": total_pending,
                       "total_used": total_Used,
                       "total_Refund": total_Refund,
                       "ticket_pending": result,
                       "ticket_search_from": searchFrom,
                       "cancel": ticket_cancel,

                       }
                      )

    return render(request, "Administration/older_ticket_data.html",
                  {"total": total,
                   "total_pending": total_pending,
                   "total_used": total_Used,
                   "total_Refund": total_Refund,
                   "ticket_pending": all_ticket,
                   "ticket_search_from": searchFrom,
                   "cancel": ticket_cancel,
                   }
                  )


def viewTicket(request, id):
    ticket_refund = BusTicket.objects.get(pk=id)
    issue_ticket_price = ticket_refund.total_amount
    reduce_75_precentage = issue_ticket_price * (75 / 100)
    if request.method == "POST":
        # refund2 = ticketRefund.objects.get(pk=id)
        form = make_refund(request.POST)

        if form.is_valid():
            try:
                requests.head(url="http://www.google.com",
                              timeout=2)  # check whether site has active internet connection.

                refund_ticket = request.POST['refund_ticket']
                refund = BusTicket.objects.get(pk=id)
                refund.ticket_status = 3
                refund.save()

                #  when you refund, get the sale static and reduce pending by 1 and add refund by 1
                get_date = get_the_current_date_p()

                change_status = monthlySales.objects.get(
                    sale_id__year=get_date[0],
                    sale_id__month=get_date[1],
                    sale_id__day=get_date[2],
                )
                change_status.pending_ticket_qty -= 1
                change_status.refund_ticket_qty += 1
                change_status.refund_ticket_amount += refund.total_amount
                change_status.save()

                ticket_date = refund.c_time  # getting the ticket issue date
                reduce_price = monthlySales.objects.get(
                    pk=ticket_date)  # getting the correspond day to reduce the money
                try:
                    if reduce_price:
                        issue_ticket_price = refund.total_amount
                        reduce_75_precentage = issue_ticket_price * (
                                75 / 100)  # reduce the percentage of the current ticket price
                        reduce_price.daily_sale -= decimal.Decimal(reduce_75_precentage)
                        reduce_price.save()

                        passanger_id = refund.passengerID
                        passenger_data = Passenger.objects.get(pk=passanger_id.passengerID)
                        passanger_email = passenger_data.emailaddr
                        print(passanger_email)
                        send_mail(
                            subject="Your ticket has been refunded 75% percentage",
                            message='',
                            from_email='gangula.dinu@gmail.com',
                            recipient_list=[str(passanger_email)],
                            fail_silently=False,
                            html_message="<p> your ticket (" + str(
                                refund.invoiceno) + ") has been refunded. payment has been send to the bank. \n refunded amount: " + str(
                                reduce_75_precentage) + " \n thank you.</p>"
                        )
                    return redirect('refund_success')
                except socket.gaierror:
                    return redirect('error_400')
            except requests.ConnectionError or requests.ConnectTimeout:
                return redirect('error_400')

    else:
        form = make_refund()
    return render(request, "Administration/view_ticket.html",
                  {
                      "ticket_data": ticket_refund,
                      'reduce': reduce_75_precentage,
                      "form": form
                  }
                  )


def ticket_refund_success(request):
    return render(request, "Administration/refund_success.html", {})


def ticket_refund_success_old(request):
    return render(request, "Administration/refund_success _old.html", {})


def olderViewTicket(request, id):
    ticket_refund = ticketRefund.objects.get(pk=id)
    issue_ticket_price = ticket_refund.total_amount
    reduce_75_precentage = issue_ticket_price * (75 / 100)
    if request.method == "POST":
        # refund2 = ticketRefund.objects.get(pk=id)
        form = make_refund(request.POST)

        if form.is_valid():
            try:
                requests.head(url="http://www.google.com",
                              timeout=2)  # check whether site has active internet connection.

                refund_ticket = request.POST['refund_ticket']
                refund = ticketRefund.objects.get(pk=id)
                refund.ticket_status = 3
                refund.save()

                #  when you refund, get the sale static and reduce pending by 1 and add refund by 1
                get_date = get_the_current_date_p()

                change_status = monthlySales.objects.get(
                    sale_id__year=get_date[0],
                    sale_id__month=get_date[1],
                    sale_id__day=get_date[2],
                )
                change_status.pending_ticket_qty -= 1
                change_status.refund_ticket_qty += 1
                change_status.refund_ticket_amount += refund.total_amount
                change_status.save()

                ticket_date = refund.c_time  # getting the ticket issue date
                reduce_price = monthlySales.objects.get(
                    pk=ticket_date)  # getting the correspond day to reduce the money
                try:
                    if reduce_price:
                        issue_ticket_price = refund.total_amount
                        reduce_75_precentage = issue_ticket_price * (
                                75 / 100)  # reduce the percentage of the current ticket price
                        reduce_price.daily_sale -= decimal.Decimal(reduce_75_precentage)
                        reduce_price.save()

                        passanger_id = refund.passengerID
                        passenger_data = Passenger.objects.get(pk=passanger_id.passengerID)
                        passanger_email = passenger_data.emailaddr
                        print(passanger_email)
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
            
                                                                                <td style="padding-top: 5px;">Refund information.</td>
                                                                            </tr>

                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-right: 200px; padding-top: 5px;">Username: </td>
                                                                                <td style="padding-top: 5px;"> """ + \
                                   refund.invoiceno + """ </td>
                                                                            </tr>
                                                                            <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                                                <td style="padding-right: 200px; padding-top: 5px;">Password: </td>
                                                                                <td style="padding-top: 5px;"> """ + \
                                   str(reduce_75_precentage) + """ </td>
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
                        send_mail(
                            subject="Your ticket has been refunded 75% percentage",
                            message='',
                            from_email='gangula.dinu@gmail.com',
                            recipient_list=[str(passanger_email)],
                            fail_silently=False,
                            html_message="<p> your ticket (" + str(
                                refund.invoiceno) + ") has been refunded. payment has been send to the bank. \n refunded amount: " + str(
                                reduce_75_precentage) + " \n thank you.</p>"
                        )
                    return redirect('refund_success_old')
                except socket.gaierror:
                    return redirect('error_400')
            except requests.ConnectionError or requests.ConnectTimeout:
                return redirect('error_400')

    else:
        form = make_refund()
    return render(request, "Administration/view_ticket_old.html",
                  {
                      "ticket_data": ticket_refund,
                      'reduce': reduce_75_precentage,
                      "form": form
                  }
                  )


#
# def olderViewTicket(request, id):
#     older_ticket_refund = ticketRefund.objects.get(pk=id)
#     issue_ticket_price = older_ticket_refund.total_amount
#     reduce_75_precentage = issue_ticket_price * (75 / 100)
#     if request.method == "POST":
#         # refund2 = ticketRefund.objects.get(pk=id)
#         form = make_refund(request.POST)
#         if form.is_valid():
#             try:
#                 requests.head(url="http://www.google.com", timeout=2)  # check whether site has active internet connection.
#
#                 # refund_ticket = request.POST['refund_ticket_old']
#                 refund = ticketRefund.objects.get(pk=id)
#                 refund.ticket_status = 3
#                 refund.save()
#
#                 #  when you refund, get the sale static and reduce pending by 1 and add refund by 1
#                 get_date = get_the_current_date_as_list()
#                 try:
#                     change_status = monthlySales.objects.get(
#                         sale_id__year=get_date[0],
#                         sale_id__month=get_date[1],
#                         sale_id__day=get_date[2],
#                     )
#                 except ObjectDoesNotExist or monthlySales.DoesNotExist:
#                     add_today_data = monthlySales(
#                         sale_id__year=get_date[0],
#                         sale_id__month=get_date[1],
#                         sale_id__day=get_date[2],
#                     )
#                     add_today_data.save()
#
#                     change_status = monthlySales.objects.get(
#                         sale_id__year=get_date[0],
#                         sale_id__month=get_date[1],
#                         sale_id__day=get_date[2],
#                     )
#                     change_status.pending_ticket_qty -= 1
#                     change_status.refund_ticket_qty += 1
#                     change_status.refund_ticket_amount += refund.total_amount
#                     change_status.save()
#
#                 ticket_date = refund.c_time  # getting the ticket issue date
#                 reduce_price = monthlySales.objects.get(pk=ticket_date)  # getting to correspond day to reduce the money
#                 try:
#                     if reduce_price:
#                         issue_ticket_price = refund.total_amount
#                         reduce_75_precentage = issue_ticket_price * (
#                                 75 / 100)  # reduce the percentage of the current ticket price
#                         reduce_price.daily_sale -= decimal.Decimal(reduce_75_precentage)
#                         reduce_price.save()
#
#                         passanger_id = refund.passengerID
#                         passenger_data = Passenger.objects.get(pk=passanger_id.passengerID)
#                         passanger_email = passenger_data.emailaddr
#                         print(passanger_email)
#                         send_mail(
#                             subject="Your ticket has been refunded 75% percentage",
#                             message='',
#                             from_email='gangula.dinu@gmail.com',
#                             recipient_list=[str(passanger_email)],
#                             fail_silently=False,
#                             html_message="<p> your ticket (" + str(
#                                 refund.invoiceno) + ") has been refunded. payment has been send to the bank. \n refunded amount: " + str(
#                                 reduce_75_precentage) + " \n thank you.</p>"
#                         )
#                     return redirect('refund_success_old')
#                 except socket.gaierror:
#                     return redirect('error_400')
#             except requests.ConnectionError or requests.ConnectTimeout:
#                 return redirect('error_400')
#     else:
#         form = make_refund()
#     return render(request, "Administration/view_ticket.html",
#                   {
#                       "ticket_data": older_ticket_refund,
#                       'reduce': reduce_75_precentage,
#                       "form": form
#                   }
#            )


def scan_qr_code(request):
    scanned_ticket = request.POST.get('scanned_ticket')
    TMP_DATA_DIC['scanned_qr_code'] = scanned_ticket
    send_ajax_respond_QR(request)
    return render(request, "Administration/scan_qr_code.html", {})


def send_ajax_respond_QR(request):
    scanned_ticket = TMP_DATA_DIC.get('scanned_qr_code')
    check_ticket = BusTicket.objects.filter(invoiceno__exact=scanned_ticket) or ticketRefund.objects.filter(
        invoiceno__exact=scanned_ticket)
    print(check_ticket)
    if check_ticket:
        ticket_no = ''
        tickets = BusTicket.objects.filter(invoiceno__exact=scanned_ticket).filter(ticket_status__exact=1)
        print(tickets)
        ticketsrefund = ticketRefund.objects.filter(invoiceno__exact=scanned_ticket).filter(ticket_status__exact=1)

        for make_use in tickets:
            make_use.ticket_status = 0
            ticket_no = BusTicket.objects.filter(invoiceno__exact=scanned_ticket).filter(ticket_status__exact=1 or 0)
            # todo ticket number don't show
            make_use.save()

        for make_use in ticketsrefund:
            make_use.ticket_status = 0
            ticket_no = ticketRefund.objects.filter(invoiceno__exact=scanned_ticket).filter(ticket_status__exact=1 or 0)

            make_use.save()
        return JsonResponse({"status": 1, 'ticket_no': ticket_no})
    else:
        return JsonResponse({"status": 0})


def bus_and_routes_update(request):
    #  get the total tickets, available and not available tickets.
    total_bus = Bus.objects.all().count()
    total_route = Routes.objects.all().count()
    available_bus = Bus.objects.filter(vehicle_status__exact=1).count()
    not_available_bus = Bus.objects.filter(vehicle_status__exact=0).count()

    all_bus = Bus.objects.all()  # get the all buses from the database
    filter_ok = request.GET.get("bus_status")
    form = bus_searchForm(request.POST)
    if filter_ok:
        result = Bus.objects.filter(vehicle_status=filter_ok)
        return render(request, "Administration/bus_n_routes_updates.html",
                      {
                          "all_buses": result,
                          'bus_Reg_from': form,

                          'total_b': total_bus,
                          'total_route': total_route,
                          'available': available_bus,
                          'not_available_bus': not_available_bus
                      }
                      )

    if request.method == "POST":
        route_delete = del_form2(request.POST)
        if form.is_valid():
            # search = request.POST['sebus']
            # print(search)
            # search_result = Bus.objects.filter()
            bus_data = Bus.objects.all
            context_dictionary = {
                'all_buses': bus_data,
                'bus_Reg_from': form,

                'total_b': total_bus,
                'total_route': total_route,
                'available': available_bus,
                'not_available_bus': not_available_bus
            }

            # todo complete search invalid
            return render(request, "Administration/bus_n_routes_updates.html", context_dictionary)

    else:
        form = bus_searchForm()
        route_delete = del_form2()

    context_dictionary = {
        'all_buses': all_bus,
        'bus_Reg_from': form,
        'bus_del': route_delete,
        'total_b': total_bus,
        'total_route': total_route,
        'available': available_bus,
        'not_available_bus': not_available_bus

    }
    return render(request, "Administration/bus_n_routes_updates.html", context_dictionary)


def del_bus_data(request):  # delete the bus
    if request.method == "POST":
        bus_delete = del_form2(request.POST)
        if bus_delete.is_valid():
            del_id = request.POST['del_bus']
            print(del_id, '555')
            del_bus = Bus.objects.get(pk=del_id)
            print(del_bus.driver_name)
            del_particular_bus_route = Routes.objects.all().filter(bus_plate_no__exact=del_bus)
            try:
                for delete_each in del_particular_bus_route:
                    delete_each.delete()  # delete all the bus route that associate with delete bus in the database
                del_bus.delete()  # delete the bus
                messages.success(request, "Deleted successfully!")
            except django.db.utils.IntegrityError:
                messages.error(request, "Failed!, you can't delete this record until database clean up.")
            # del_route.delete()

        return redirect('bus and route update')


def view_bus_routes(request, id):
    total_bus = Bus.objects.all().count()
    total_route = Routes.objects.all().count()
    available_route = Routes.objects.filter(route_status__exact=1).count()
    not_available_route = Routes.objects.filter(route_status__exact=0).count()

    TMP_DATA_DIC['previous_view_bus_id'] = id
    get_bus_routes = Routes.objects.filter(bus_plate_no__exact=id)

    if request.method == "POST":
        route_delete = del_form(request.POST)
        if route_delete.is_valid():
            del_id = request.POST['del_field']
            del_route = Routes.objects.get(pk=del_id)
            del_route.delete()
        messages.success(request, "Deleted successfully!")
        return redirect('view bus routes', id)
    else:
        route_delete = del_form()

    # all_route = Routes.objects.all()  # get the all buses from the database
    filter_ok = request.GET.get("route_status")
    # form = bus_searchForm(request.POST)
    if filter_ok:
        result = Routes.objects.filter(route_status__exact=filter_ok)
        return render(request, "Administration/view_bus_routes.html",
                      {
                          'routes': result,
                          'route_del': route_delete,
                          'total_b': total_bus,
                          'total_route': total_route,
                          'available': available_route,
                          'not_available_bus': not_available_route,
                          'previous_id': id,
                      }
                      )

    context_dictionary = {
        'routes': get_bus_routes,
        'route_del': route_delete,
        'total_b': total_bus,
        'total_route': total_route,
        'available': available_route,
        'not_available_bus': not_available_route,
        'previous_id': id,

    }
    return render(request, "Administration/view_bus_routes.html", context_dictionary)


def update_bus_route(request, route_id):
    # calling the ajax function
    # send_json_ajax_respond(request, route_id)

    # get_the_particular_bus_route = Routes.objects.get(pk=route_id)

    route_e = Routes.objects.get(pk=route_id)
    print(route_e.route_no)
    print(route_e.start_location)
    if request.method == "POST":
        route_form = routeRegForm(request.POST)
        if route_form.is_valid():
            bus_number_plate = request.POST['plate_no']

            bus_noo = Bus.objects.get(pk=bus_number_plate)

            bus_route_no = request.POST['route_no']
            bus_start_location = request.POST['start_location']
            bus_end_location = request.POST['end_location']
            bus_route_date = request.POST['route_date']
            bus_route_time = request.POST['route_time']
            bus_total_distance = request.POST['total_distance']
            # bus_avg_run_time = request.POST['avg_run_time']
            bus_route_status = request.POST['route_status']

            route_e.bus_plate_no = bus_noo
            route_e.route_no = bus_route_no
            route_e.start_location = bus_start_location
            route_e.end_location = bus_end_location
            route_e.route_date = bus_route_date
            route_e.route_time = bus_route_time
            route_e.total_distance = bus_total_distance
            # route_e.avg_run_time = bus_avg_run_time
            route_e.route_status = bus_route_status

            route_e.save()
            messages.success(request, "Updated Successfully")

            # return redirect('update bus routes', route_id)
            return redirect('view bus routes', bus_noo)

    else:
        print(route_e.bus_plate_no)
        print(route_e.route_no)
        print(route_e.start_location)
        route_form = routeRegForm(
            initial={
                'plate_no': route_e.bus_plate_no,
                'route_no': route_e.route_no,
                'start_location': route_e.start_location,
                'end_location': route_e.end_location,

                'total_distance': route_e.total_distance,
                # 'avg_run_time': route_e.avg_run_time,
                'route_status': route_e.route_status,  # todo not showing initial value
                'route_time': route_e.route_time,
                'route_date': route_e.route_date,
            }

        )

    context_dictionary = {

        "route_form": route_form,
        'route_id': route_id
        # "route_data": get_the_particular_bus_route

    }
    return render(request, 'Administration/route_update.html', context_dictionary)


def update_bus(request, plate_no):
    bus_id = get_object_or_404(Bus, pk=plate_no)
    if request.method == "POST":
        print("hi hi hi hi")
        bus_form = busRegForm(request.POST)
        if bus_form.is_valid():
            plate = request.POST['bus_plate_no']
            driver_name = request.POST['driver_name']
            no_of_seat = request.POST['no_of_seat']
            vehicle_status = request.POST['vehicle_status']
            contact_no = request.POST['contact_no']
            other_details = request.POST['other_details']
            modify_contact = str(contact_no).replace("-", "")
            #  update the data
            bus_id.bus_plate_no = plate
            bus_id.driver_name = driver_name
            bus_id.no_of_seat = no_of_seat
            bus_id.vehicle_status = vehicle_status
            bus_id.contact_no = modify_contact
            bus_id.other_details = other_details

            bus_id.save()

            messages.success(request, "Updated Successfully")

            return redirect('bus and route update')

    else:
        bus_form = busRegForm(
            initial={
                'bus_plate_no': bus_id.bus_plate_no,
                'driver_name': bus_id.driver_name,
                'no_of_seat': bus_id.no_of_seat,
                'vehicle_status': bus_id.vehicle_status,
                'contact_no': bus_id.contact_no,
                'other_details': bus_id.other_details

            }
        )
    context_dictionary = {
        "busform": bus_form,
        "bus_id": plate_no
    }
    return render(request, "Administration/bus_update.html", context_dictionary)


# def del_routes(request):
#     if request.method == "POST":
#         del_id = request.POST['del_val']
#         print(del_id)
#     return redirect('update bus routes')


def ownerDashboard(request):
    return render(request, "Administration/ownerDashboard.html", {})


def error_500(request):
    return render(request, "Administration/error_500.html", {})


def no_internet(request):
    return render(request, "Administration/400_no_internet.html", {})
