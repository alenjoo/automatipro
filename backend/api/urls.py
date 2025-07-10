from django.urls import path
from .views import RegisterView, CustomLoginView, LeaveRequestCreateView, LeaveRequestListView, LeaveRequestUpdateView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', CustomLoginView.as_view()),
    path('leave-request/', LeaveRequestCreateView.as_view(), name='leave-request-create'),
    path('leave-requests/', LeaveRequestListView.as_view(), name='leave-requests-list'),
    path('leave-request/<int:pk>/', LeaveRequestUpdateView.as_view(), name='leave-request-update'),
]
