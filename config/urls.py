from django.contrib import admin
from django.urls import path, include
from OrderSystem.views import (EmployeeOrderDashboardView, EmployeeLoginView, LandingPageView, OrderAcceptView,
                               OrderCompleteView, OrderRejectView, OrderStatusApiView, OrderDetailView,
                               TableView, CustomerCreateOrderView, OrderCountView
                               )
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('admin/', admin.site.urls),
    path('login/', EmployeeLoginView.as_view()),
    path('orders/', EmployeeOrderDashboardView.as_view(), name='orders_dashboard'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('order/<int:pk>/accept/', OrderAcceptView.as_view(), name='order_accept'),
    path('order/<int:pk>/complete', OrderCompleteView.as_view(), name='order_complete'),
    path('order/<int:pk>/reject', OrderRejectView.as_view(), name='order_reject'),
    path('api/order-statuses/', OrderStatusApiView.as_view(), name='order_status_api'),
    path('api/order-count/', OrderCountView.as_view(), name='order_count_api'),
    path('order/<int:pk>/detail/', OrderDetailView.as_view(), name='order_detail'),
    path('table/<int:pk>/', TableView.as_view(), name='table'),
    path('table/<int:table_id>/order/new/', CustomerCreateOrderView.as_view(), name='create_order'),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
]
