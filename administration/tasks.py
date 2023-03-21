from __future__ import unicode_literals, absolute_import
import decimal
import time

import celery
from django.http import JsonResponse

from celery import shared_task
import administration.utils
from main.models import BusBookingDetails, BusTicket, ticketRefund, Passenger, PassengerPayment, Routes
from .models import monthlySales
from datetime import datetime, timedelta
import datetime
import time


@shared_task
def calculate_daily_sales():
    current_date = str(datetime.date.today())
    # current_date = '2022-12-04'
    date_c = current_date.split('-')
    current_day_records = BusTicket.objects.filter(c_time__year=date_c[0], c_time__month=date_c[1],
                                                   c_time__day=date_c[2]).filter(ticket_counted__exact=0)
    if current_day_records:
        for dates in current_day_records:
            day_sale = monthlySales.objects.filter(sale_id__year=date_c[0], sale_id__month=date_c[1],
                                                   sale_id__day=date_c[2])
            if day_sale:
                # update current ticket prince
                day_sale_update = monthlySales.objects.get(pk=current_date)
                day_sale_update.daily_sale += dates.total_amount
                day_sale_update.pending_ticket_qty += 1
                day_sale_update.pending_ticket_amount += dates.total_amount
                day_sale_update.total_ticket_qty += 1
                day_sale_update.save()

                # get the current ticket id and turn into counted ticket
                current_id = dates.ticket_id
                update_ticket = BusTicket.objects.get(pk=current_id)

                update_ticket.ticket_counted = 1
                update_ticket.save()
            else:
                day_sale_update = monthlySales(
                    sale_id=str(current_date),
                    daily_sale=0,
                    cancel_ticket_qty=0,
                    cancel_ticket_amount=0.00,
                    pending_ticket_qty=0,
                    pending_ticket_amount=0.00,
                    used_ticket_qty=0,
                    used_ticket_amount=0.00,
                    total_ticket_qty=0,
                    refund_ticket_qty=0,
                    refund_ticket_amount=0.00,  # todo make these default in the database
                    user_qty=0,
                )
                day_sale_update.save()
    #  get the current time
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    current_day = datetime.date.today().day

    #  format the current time as verified time input
    current_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)

    passenger_data = Passenger.objects.filter(passenger_count=0)
    if passenger_data:
        update_data = monthlySales.objects.get(pk=current_date)
        for user in passenger_data:
            update_data.user_qty += 1
            user.passenger_count = 1
            update_data.save()
            user.save()

    current_day_used_tickets = BusTicket.objects.filter(c_time__year=date_c[0], c_time__month=date_c[1],
                                                        c_time__day=date_c[2]).filter(ticket_counted__exact=1).filter(
        ticket_status__exact=0).filter(ticket_used_counted__exact=0)
    if current_day_used_tickets:
        for used_tickets in current_day_used_tickets:
            update_used_tickets = monthlySales.objects.get(pk=current_date)
            if used_tickets.ticket_used_counted == 0 and used_tickets.ticket_status == 0:
                used_tickets.ticket_used_counted = 1
                update_used_tickets.used_ticket_qty += 1
                used_tickets.save()
                update_used_tickets.save()

    # if the departure time is due the route will not available / disable until next day
    disabling_routes = Routes.objects.all()
    for disable in disabling_routes:
        # get the current time of the day
        get_the_current_time = time.strftime("%H:%M:%S")
        if disable.route_status == 1:  # if the route is available but the time is passed

            if str(disable.route_time) <= str(get_the_current_time):
                print(str(disable) + ' ' + str(disable.route_time) + ' ' + str(disable.route_status))
                disable.route_status = 0
                disable.save()


@shared_task
def print2():
    print("hi hi hi")


# @shared_task
# def copy_pending_ticket_to_the_recovery_db():
#     # older_used_ticket_data = BusTicket.objects.filter(ticket_status__exact=0)
#     # if older_used_ticket_data:
#     #     older_used_ticket_data.delete()
#
#     older_pending_ticket_data = BusTicket.objects.filter(ticket_status__exact=1)
#     if older_pending_ticket_data:
#         for pending in older_pending_ticket_data:
#             print(pending.invoiceno)
#             if not ticketRefund.objects.filter(
#                     invoiceno__exact=pending.invoiceno):  # check whether ticket is exit in the refund
#                 trasferData = ticketRefund(
#                     total_amount=pending.total_amount,
#                     company_name=pending.company_name,
#                     ticket_status=pending.ticket_status,
#                     c_time=pending.c_time,
#                     ticket_expire_date=pending.ticket_expire_date,
#                     invoiceno=pending.invoiceno,
#                     ticket_counted=pending.ticket_counted,
#                     ticket_qr_code=pending.ticket_qr_code,
#                     bus_plate_no=pending.bus_plate_no,
#                     passengerID=pending.passengerID,
#                     payment_id=pending.payment_id,
#
#                 )
#                 trasferData.save()
#                 print("saving data successfully")


@shared_task
def copy_n_del_ticket_to_the_recovery__db():
    older_pending_ticket_data = BusTicket.objects.filter(ticket_status__exact=1)
    if older_pending_ticket_data:
        for pending in older_pending_ticket_data:
            print(pending.invoiceno)
            if not ticketRefund.objects.filter(
                    invoiceno__exact=pending.invoiceno):  # check whether ticket is exit in the refund
                trasferData = ticketRefund(
                    total_amount=pending.total_amount,
                    company_name=pending.company_name,
                    ticket_status=pending.ticket_status,
                    c_time=pending.c_time,
                    ticket_expire_date=pending.ticket_expire_date,
                    invoiceno=pending.invoiceno,
                    ticket_counted=pending.ticket_counted,
                    ticket_qr_code=pending.ticket_qr_code,
                    bus_plate_no=pending.bus_plate_no,
                    passengerID=pending.passengerID,
                    payment_id=pending.payment_id,

                )
                trasferData.save()
                print("saving data successfully")

    older_delete_ticket_data_pending = BusTicket.objects.filter(ticket_status__exact=1)

    # older_delete_ticket_data_used = BusTicket.objects.filter(ticket_status__exact=0)
    # older_delete_ticket_data_cancel = BusTicket.objects.filter(ticket_status__exact=2)
    # older_delete_ticket_data_delete = BusTicket.objects.filter(ticket_status__exact=3)
    delete_all_data_from_db = BusTicket.objects.all()

    print("gagnula gangula")
    print(older_delete_ticket_data_pending)

    for delete_record in delete_all_data_from_db:
        passenger_id = delete_record.passengerID.passengerID
        payment_id = delete_record.payment_id.payment_id
        booking_id = delete_record.payment_id.bus_booking_id.bus_booking_id

        print(passenger_id, payment_id, booking_id)
        print("gangula")
        delete_record.delete()
        delete_payment = PassengerPayment.objects.filter(pk=payment_id)
        delete_payment.delete()
        delete_booking = BusBookingDetails.objects.filter(pk=booking_id)
        delete_booking.delete()
        delete_passenger = Passenger.objects.filter(pk=passenger_id)
        delete_passenger.delete()
        print("delete successfully")


@shared_task
def delete_records_more_then_3_days():
    #  get the current time
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    current_day = datetime.date.today().day

    #  format the current time as verified time input
    current_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)

    # time_threshold = datetime.date.today() - timedelta(days=1)  # get the 3 days old ticket from the backup
    time_threshold = datetime.date.today()  # get the 3 days old ticket from the backup
    filter_date = str(time_threshold).split('-')

    print(filter_date)
    results = ticketRefund.objects.filter(
        ticket_expire_date__day=filter_date[2],
        ticket_expire_date__month=filter_date[1],
        ticket_expire_date__year=filter_date[0],
    )  # filter all 3 days old tickets
    print(results)
    for ticket in results:
        print(ticket.invoiceno)
        update_data = monthlySales.objects.get(pk=current_date)  # update the current day tickets details
        # if the ticket not refunded, before delete the tickets, it will cancel and then delete
        if ticket.ticket_status == 1:
            update_data.cancel_ticket_qty += 1
            update_data.pending_ticket_qty -= 1  ###############
            # update_data.cancel_ticket_amount += ticket.total_amount
            update_data.save()
            ticket.delete()  # delete the ticket

        if ticket.ticket_status == 3:
            update_data.refund_ticket_qty += 1
            reduce_75_precentage = ticket.total_amount * (75 / 100)  # reduce the percentage of the current ticket price
            update_data.refund_ticket_amount += decimal.Decimal(-reduce_75_precentage)
            update_data.save()

            ticket.delete()

    #  get all the tickets and check if it has used tickets, if yes then delete right way
    used_tickets = ticketRefund.objects.all()
    for use_ticket in used_tickets:
        update = monthlySales.objects.get(pk=current_date)
        if use_ticket.ticket_status == 0:  # update used ticket details to the database.

            update.used_ticket_qty += 1
            update.used_ticket_amount += use_ticket.total_amount
            update.save()

            use_ticket.delete()  # delete the ticket

    # get_all_refund_ticket = ticketRefund.objects.all()
    # for check_each_records in get_all_refund_ticket:
    #     print(check_each_records)


# @shared_task
# def delete_test_every24_hours():
#     older_used_ticket_data = ticketRefund.objects.filter(ticket_status__exact=1)
#
#     if older_used_ticket_data:
#         print("i'm in")
#         older_used_ticket_data.delete()


@shared_task
def reschedule_routes_and_clean_up_db():
    route = Routes.objects.all()
    booking_details = BusBookingDetails.objects.all()
    payment_data = PassengerPayment.objects.all()
    passenger = Passenger.objects.all()
    print(route)
    # automate the everyday route and change the date of the route
    # and also change the not available route to the available routes



    for every_day_route in route:
        # print(every_day_route)
        today_date = datetime.datetime.today()
        every_day_route.route_date = today_date
        if every_day_route.route_status == 0:
            for pay in payment_data:
                pay.delete()

            for pay in booking_details:
                pay.delete()

            for pay in passenger:
                pay.delete()
            every_day_route.route_status = 1
            every_day_route.save()

    # for every_day_route in route:
    #     print(every_day_route)
    #     today_date = datetime.datetime.today()
    #
    #     every_day_route.route_date = today_date
    #     if every_day_route.route_status == 0:
    #         every_day_route.route_status = 1
    #     every_day_route.save()

    # get_yesterday_date = str(datetime.datetime.today() - timedelta(days=1)).split('-')
    # get_today_date = str(datetime.datetime.today()).split('-')
    # get_tomorrow_date = str(datetime.datetime.today() + timedelta(days=2)).split('-')
    #
    # print(get_yesterday_date)
    # print(get_today_date)
    # print(get_tomorrow_date)
    # get_yesterday_routes = Routes.objects.filter(
    #     route_date__year=get_yesterday_date[0],
    #     route_date__month=get_yesterday_date[1],
    #     route_date__day=get_yesterday_date[2],
    # )
    # print(get_yesterday_routes)
