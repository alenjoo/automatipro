from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LeaveRequestCreateView(generics.CreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LeaveRequestListView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['hr', 'admin']:
            return LeaveRequest.objects.all()
        else:
         
            return LeaveRequest.objects.none()
class LeaveRequestUpdateView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        user = self.request.user
        if user.role not in ['hr', 'admin']:
            raise PermissionDenied("You do not have permission to update leave requests.")

        return super().get_object()
    def perform_update(self, serializer):
        print("Saving status update:", serializer.validated_data.get("status"))
        serializer.save()