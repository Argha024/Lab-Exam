from django.contrib import admin
from .models import Employee, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'joining_date')
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee_name', 'status', 'due_date', 'days_left')
    search_fields = ('title',)
    list_filter = ('status',)

    def employee_name(self, obj):
        return obj.employee.name
    employee_name.admin_order_field = 'employee'
    employee_name.short_description = "Assigned Employee"

    def days_left(self, obj):
        return obj.days_left()
    days_left.short_description = "Days Left"
