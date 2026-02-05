from django.test import TestCase
from .models import Order, Table, Employee
from datetime import timedelta
from django.utils import timezone


class OrderLateAcceptStatusTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_name="T1")
        self.emp = Employee.objects.create(username="E1")
        self.emp2 = Employee.objects.create(username="E2")

    def test_missed_order(self):
        """Objednávka nebyla přijata do 10 minut"""
        order = Order.objects.create(table_id=self.table, assigned_employee=self.emp)
        Order.objects.filter(pk=order.order_id).update(
            order_time=timezone.now() - timedelta(minutes=10)
        )
        order.refresh_from_db()
        self.assertEqual(order.get_actual_order_status(), "Propásla")

    def test_late_order(self):
        """Příprava trvá déle než 15 minut"""

        order = Order.objects.create(table_id=self.table)
        order.order_accepted(self.emp)

        Order.objects.filter(pk=order.order_id).update(
            accepted_time=timezone.now() - timedelta(minutes=15)
        )
        order.refresh_from_db()

        self.assertEqual(order.get_actual_order_status(), "Nestihnuta")

    def test_completion_after_rejection(self):
        order = Order.objects.create(table_id=self.table)
        order.order_declined_by(self.emp2)
        order.order_accepted(self.emp)

        self.assertEqual(order.get_actual_order_status(), Order.Status.ACCEPTED)

        order.order_completed(self.emp)
        order.refresh_from_db()

        self.assertEqual(order.order_status, Order.Status.COMPLETED)

    def test_unauthorized_completion_fails(self):
        """Test: Pokus o dokončení objednávky jiným zaměstnancem vyhodí ValueError"""
        order = Order.objects.create(table_id=self.table)
        order.order_accepted(self.emp)

        with self.assertRaises(ValueError) as cm:
            order.order_completed(self.emp2)

        self.assertEqual(str(cm.exception), "Objednávku může dokončit jen ten kdo za ní má odpovědnost")
