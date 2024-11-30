from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('operations/<int:operation_id>/', operation_details, name="operation_details"),
    path('operations/<int:operation_id>/add_to_calculation/', add_operation_to_draft_calculation, name="add_operation_to_draft_calculation"),
    path('calculations/<int:calculation_id>/delete/', delete_calculation, name="delete_calculation"),
    path('calculations/<int:calculation_id>/', calculation),
    path('process_operations/<int:calculation_id>/', process_operations, name='process_operations')
]
