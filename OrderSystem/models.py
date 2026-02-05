from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator


class Employee(AbstractUser):
    class Meta:
        verbose_name = "Zaměstnanec"
        verbose_name_plural = "Zaměstnanci"

    first_name = models.CharField("Jméno", max_length=150, blank=True)
    last_name = models.CharField("Příjmení", max_length=150, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


# Tabulka pro menu
class MenuItem(models.Model):
    class Meta:
        verbose_name = "Položka v menu"
        verbose_name_plural = "Položky v menu"

    class Category(models.TextChoices):
        TEA = "Čaj"
        COFFEE = "Káva"
        DESSERTS = "Zákusky"

    item_name = models.CharField(
        max_length=100,
        verbose_name="Položka",
        unique=True
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Cena"
    )

    category = models.CharField(
        max_length=100,
        choices=Category.choices,
        default=Category.TEA,
    )

    def get_category_name(self) -> str:
        return self.category

    def __str__(self):
        return f"{self.item_name} ({self.price} Kč)"


# Tabulka pro stoly
class Table(models.Model):
    class Meta:
        verbose_name = "Stůl"
        verbose_name_plural = "Stoly"

    table_name = models.CharField(
        max_length=100,
        verbose_name="Název/Číslo stolu",
        unique=True
    )

    def __str__(self):
        return self.table_name


# Tabulka pro objednávky
class Order(models.Model):
    class Meta:
        verbose_name = "Objednávka"
        verbose_name_plural = "Objednávky"

    class Status(models.TextChoices):
        UNACCEPTED = "Nepřijata"
        ACCEPTED = "Přijata"
        COMPLETED = "Dokončena"

    order_id = models.BigAutoField(primary_key=True)
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="Čas vytvoření objednávky")
    accepted_time = models.DateTimeField(null=True, blank=True, verbose_name="Čas přijetí objednávky")
    completed_time = models.DateTimeField(null=True, blank=True, verbose_name="Čas dokončení objednávky")
    late_accept = models.BooleanField(default=False)
    late_completion = models.BooleanField(default=False)

    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Zaměstnanec"
    )

    order_status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.UNACCEPTED,
        verbose_name="Stav objednávky",
    )

    declined_by = models.ManyToManyField(Employee, blank=True, related_name='declined_orders')

    def __str__(self):
        return f"Objednávka č. {self.order_id} ({self.table_id.table_name})"

    def _change_status(self, new_status: Status) -> None:

        if self.order_status == self.Status.COMPLETED:
            raise ValueError("Stav dokončené objednávky již nelze měnit.")

        self.order_status = new_status
        self.save()

    def get_actual_order_status(self) -> str:

        now = timezone.now()

        if self.order_status == self.Status.COMPLETED:
            return self.order_status

        # 1. Pravidlo: Nepřijatá do 10 minut
        if self.order_status == self.Status.UNACCEPTED:
            if now >= self.order_time + timedelta(minutes=10):
                if not self.late_accept:
                    self.late_accept = True
                    self.save()
                return 'Propásla'

        # 2. Pravidlo: Objednávka nedokončena do 15 minut
        elif self.order_status == self.Status.ACCEPTED and self.accepted_time:
            if now >= self.accepted_time + timedelta(minutes=15):
                if not self.late_completion:
                    self.late_completion = True
                    self.save()
                return 'Nestihnuta'

        return self.order_status

    def order_accepted(self, employee: Employee) -> None:

        if self.assigned_employee is not None:
            return

        self.accepted_time = timezone.now()
        self.assigned_employee = employee
        self._change_status(self.Status.ACCEPTED)

    def order_completed(self, employee: Employee) -> None:
        if employee == self.assigned_employee:
            completedTime = timezone.now()
            self.completed_time = completedTime
            self._change_status(self.Status.COMPLETED)
        else:
            raise ValueError("Objednávku může dokončit jen ten kdo za ní má odpovědnost")

    def order_declined_by(self, employee: Employee):
        if self.assigned_employee == employee:
            return
        self.declined_by.add(employee)
        self.save()

    def get_total_order_price(self):
        return sum(item.total_item_price() for item in self.items.all())


class OrderItem(models.Model):
    class Meta:
        verbose_name_plural = "Souhrn objednávky"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )

    def __str__(self):
        return f"{self.quantity}x {self.item.item_name}"

    def total_item_price(self):
        return self.quantity * self.item.price
