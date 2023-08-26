from rest_framework.permissions import BasePermission


class IsExaminerOption(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsCandidate(BasePermission):
    """
    Return True if the requesting user is a candidate of the exam 
    which the question belongs
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsExaminer(BasePermission):
    """
    Return True if the requesting user is the owner of the exam 
    which the question belongs
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
