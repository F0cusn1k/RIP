from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для операций
    path('api/operations/', search_operations),  # GET
    path('api/operations/<int:operation_id>/', get_operation_by_id),  # GET
    path('api/operations/<int:operation_id>/update/', update_operation),  # PUT
    path('api/operations/<int:operation_id>/update_image/', update_operation_image),  # POST
    path('api/operations/<int:operation_id>/delete/', delete_operation),  # DELETE
    path('api/operations/create/', create_operation),  # POST

    # Набор методов для вычислений
    path('api/calculations/', search_calculations),  # GET
    path('api/calculations/<int:calculation_id>/', get_calculation_by_id),  # GET
    path('api/calculations/<int:calculation_id>/update/', update_calculation),  # PUT
    path('api/calculations/<int:calculation_id>/update_status_user/', update_status_user),  # PUT
    path('api/calculations/<int:calculation_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/calculations/<int:calculation_id>/delete/', delete_calculation),  # DELETE
    path('api/calculations/create/', create_calculation),  # POST

    # Набор методов для связи операций и вычислений
    path('api/calculations/<int:calculation_id>/operations/<int:operation_id>/add/', add_operation_to_calculation),  # POST
    path('api/calculations/<int:calculation_id>/operations/<int:operation_id>/delete/', delete_operation_from_calculation),  # DELETE
    path('api/calculations/<int:calculation_id>/operations/<int:operation_id>/update/', update_operation_in_calculation),  # PUT

    # Набор методов пользователей (если требуется)
    path('api/users/register/', register),  # POST
    path('api/users/login/', login),  # POST
    path('api/users/logout/', logout),  # POST
    path('api/users/<int:user_id>/update/', update_user),  # PUT
]

# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('', index),
#     path('operations/<int:operation_id>/', operation_details, name="operation_details"),
#     path('operations/<int:operation_id>/add_to_calculation/', add_operation_to_draft_calculation, name="add_operation_to_draft_calculation"),
#     path('calculations/<int:calculation_id>/delete/', delete_calculation, name="delete_calculation"),
#     path('calculations/<int:calculation_id>/', calculation)
# ]
