from django.contrib import admin
from tickets.models import Order, Ticket


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_filter = ("flight",)
