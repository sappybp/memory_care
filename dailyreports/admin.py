from django.contrib import admin

from .models import Visitor, Dailyreport, Inspection


class VisitorsAdmin(admin.ModelAdmin):
    list_display = ["tsusho_name", "toroku_date"]
    list_filter = ["toroku_date"]

class DailyreportsAdmin(admin.ModelAdmin):
    list_filter = ["toroku_date"]

class InspectionAdmin(admin.ModelAdmin):
    list_filter = ["toroku_date"]


admin.site.register(Visitor, VisitorsAdmin)
admin.site.register(Dailyreport, DailyreportsAdmin)
admin.site.register(Inspection, InspectionAdmin)