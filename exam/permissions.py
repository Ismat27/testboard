from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsExaminerPermission(BasePermission):
    pass


class CreateExamPermission(BasePermission):

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class ExamOwnerPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        return obj.examiner == user


class ExamResultPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.candidate == user and request.method in SAFE_METHODS:
            return True
        if obj.assessment.examiner == user:
            return True
        return False
