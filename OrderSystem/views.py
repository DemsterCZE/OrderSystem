from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db import transaction


class LandingPageView(ListView):
    model = Table
    template_name = 'LandingPage.html'
    context_object_name = 'tables'


class EmployeeLoginView(LoginView):
    template_name = 'EmployeeLoginPage.html'


@method_decorator(login_required, name='dispatch')
class EmployeeOrderDashboardView(ListView):
    model = Order
    template_name = 'EmployeeOrderDashboard.html'
    context_object_name = 'orders'

    def get_queryset(self):
        current_employee = self.request.user
        return Order.objects.exclude(order_status=Order.Status.COMPLETED).exclude(
            declined_by=current_employee).order_by('order_time')


## View pro přijmutí objednávky
@method_decorator(login_required, name='dispatch')
class OrderAcceptView(View):
    def post(self, request, pk):
        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=pk)
            if order.assigned_employee:
                return redirect('orders_dashboard')
            try:
                employee = request.user
                order.order_accepted(employee)
            except AttributeError:
                print("Při přijímání objednávky se stala chyba")
            return redirect('orders_dashboard')


## View pro dokončení objednávky
@method_decorator(login_required, name='dispatch')
class OrderCompleteView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        try:
            employee = request.user
            order.order_completed(employee)
        except AttributeError:
            print("Při dokončování objednávky se stala chyba")
        return redirect('orders_dashboard')


## View pro odmítnutí objednávky
@method_decorator(login_required, name='dispatch')
class OrderRejectView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        try:
            employee = request.user
            order.order_declined_by(employee)

        except AttributeError:
            print("Při odmítání objednávky se stala chyba")
        return redirect('orders_dashboard')


## View pro zkontrolování stavu objednávek
class OrderStatusApiView(View):
    def get(self, request, *args, **kwargs):
        table_id = request.GET.get('table_id')

        if request.user.is_authenticated:
            orders = Order.objects.exclude(order_status=Order.Status.COMPLETED)
        elif table_id:
            orders = Order.objects.filter(table_id=table_id).exclude(order_status=Order.Status.COMPLETED)
        else:
            return JsonResponse({"orders": []}, status=403)

        data = []
        for order in orders:
            data.append({
                "id": order.order_id,
                "status": order.get_actual_order_status(),
            })

        return JsonResponse({"orders": data})


## View pro zhlédnutí souhrnu objednávky
@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    template_name = 'OrderDetail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.exclude(order_status=Order.Status.COMPLETED)


## View pro zhlédnutí stolu
class TableView(DetailView):
    model = Table
    template_name = 'TablePage.html'
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_orders'] = (Order.objects.filter(table_id=self.object)
                                    .exclude(order_status=Order.Status.COMPLETED)
                                    .prefetch_related('items__item'))

        context['table_total'] = sum(order.get_total_order_price() for order in context['active_orders'])
        return context


## View pro vytvoření objednávky
class CustomerCreateOrderView(View):
    template_name = 'CreateOrder.html'

    def get(self, request, table_id):
        table = get_object_or_404(Table, pk=table_id)
        menu_items = MenuItem.objects.all().order_by('category')
        return render(request, self.template_name, {
            'table': table,
            'menu_items': menu_items
        })

    def post(self, request, table_id):
        table = get_object_or_404(Table, pk=table_id)
        menu_items = MenuItem.objects.all()

        items_to_create = []
        for item in menu_items:
            quantity = request.POST.get(f'quantity_{item.id}', 0)
            if quantity and int(quantity) > 0:
                items_to_create.append((item, int(quantity)))

        if not items_to_create:
            return self.get(request, table_id)


        new_order = Order.objects.create(table_id=table)
        for menu_item, qty in items_to_create:
            OrderItem.objects.create(
                order=new_order,
                item=menu_item,
                quantity=qty
            )

        return redirect('table', pk=table.pk)


@method_decorator(login_required, name='dispatch')
class OrderCountView(View):
    def get(self, request):
        order_count = Order.objects.exclude(order_status=Order.Status.COMPLETED).count()
        data = []
        data.append({"count": order_count})

        return JsonResponse({"orders": data})
