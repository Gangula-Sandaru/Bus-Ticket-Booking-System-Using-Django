from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.adminView, name="adminView"),
    path("logout/", views.logout_site, name="logout_me"),
    path("register/", views.register, name="register"),
    path("register success/", views.registration_success, name="register_success"),
    path("dashboard/", views.adminDashboard, name="adminDashboard"),
    path("get static/", views.get_static, name="get_static"),
    path("bus registration/", views.busRegistration, name="bus registration"),
    path("route registration/", views.routeRegistration, name="route registration"),
    path("bus and routes updates/", views.bus_and_routes_update, name="bus and route update"),
    path("view bus routes/<str:id>", views.view_bus_routes, name="view bus routes"),
    path("update bus routes/<int:route_id>", views.update_bus_route, name="update bus routes"),
    path("news latters/", views.newsLatters, name="news latter and update"),
    path("news latters/news latter success/", views.news_latter_success, name="news latter success"),
    path("inquiry/", views.inquiry, name="inquiry"),
    path("reviewd/", views.feedback_reviewed, name="review"),
    # path("inquiry_delete<int:id>/remove/", views.inquiry_delete, name="inquiry_delete"),
    # path("inquiry_pending_filter", views.filter_pending, name="pending_filter"),
    path("ticket_details/", views.ticket, name="ticket"),
    path("ticket_refund_success/", views.ticket_refund_success, name="refund_success"),
    path("ticket_refund_success/old/", views.ticket_refund_success_old, name="refund_success_old"),
    path("view_ticket/<int:id>/view ticket", views.viewTicket, name="viewTicket"),
    path("older view ticket/<int:id>/view older ticket", views.olderViewTicket, name="olderViewTicket"),
    path("older ticket details/", views.older_ticket_details, name="older_ticket_details"),
    path("scan qr code/", views.scan_qr_code, name="scan_qr_code"),
    path("del_bus/", views.del_bus_data, name="del bus"),
    path("update bus/<str:plate_no>", views.update_bus, name="update bus"),

    path("send_qr_ajax/", views.send_ajax_respond_QR, name="qr_ajax_calls"),
    # path("send_json_ajax_respond/<int:route_id>", views.send_json_ajax_respond, name="send_route_ajax_respond"),

    path("owner dashboard/", views.ownerDashboard, name="ownerDashboard"),
    path("500 error", views.error_500, name="error_500"),
    path("400 error", views.no_internet, name="error_400"),
]

# handeler404 = "helper.views.handel_not_found"
