from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'Patient'

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'Doctor'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.account_type == 'Admin'