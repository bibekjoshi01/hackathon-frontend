import django_filters
from django.db.models import Q
from django_filters.rest_framework import (
    DateFromToRangeFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView

from src.libs.pagination import CustomLimitOffsetPagination
from src.user.models import MainModule, PermissionCategory, UserGroup, UserPermission
from src.user.permissions import UserGroupSetupPermission, UserSetupPermission

from .serializers import (
    MainModuleSerializer,
    UserGroupForUserSerializer,
    UserPermissionCategorySerializer,
    UserPermissionSerializer,
)


class FilterForMainModule(FilterSet):
    date = DateFromToRangeFilter(field_name="created_at")
    name = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = MainModule
        fields = ["id", "date", "name"]


class MainModuleForUserGroupsView(ListAPIView):
    """Main Module List API View"""

    permission_classes = [UserGroupSetupPermission]
    queryset = MainModule.objects.filter(is_active=True, is_archived=False)
    serializer_class = MainModuleSerializer
    filterset_class = FilterForMainModule
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    http_method_names = ["get", "head", "options"]


class FilterForUserPermission(FilterSet):
    date = DateFromToRangeFilter(field_name="created_at")
    name = django_filters.CharFilter(lookup_expr="iexact")
    codename = django_filters.CharFilter()
    permission_category = django_filters.NumberFilter(field_name="permission_category")
    main_module = django_filters.NumberFilter(
        field_name="permission_category__main_module",
        label="Main Module",
    )

    class Meta:
        model = UserPermission
        fields = [
            "id",
            "date",
            "name",
            "codename",
            "permission_category",
            "main_module",
        ]


class UserPermissionForUserGroupsView(ListAPIView):
    """User Permissions List View"""

    pagination_class = CustomLimitOffsetPagination
    permission_classes = [UserGroupSetupPermission]
    queryset = UserPermission.objects.filter(is_active=True, is_archived=False)
    serializer_class = UserPermissionSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = FilterForUserPermission
    http_method_names = ["get", "head", "options"]
    search_fields = ["name", "codename", "codename"]
    ordering_fields = ["id", "name", "codename"]
    ordering = ["id"]


class FilterForUserPermissionCategory(FilterSet):
    date = DateFromToRangeFilter(field_name="created_at")
    name = django_filters.CharFilter(lookup_expr="iexact")
    codename = django_filters.CharFilter()
    main_module = django_filters.NumberFilter(field_name="main_module")

    class Meta:
        model = PermissionCategory
        fields = ["id", "date", "name", "main_module"]


class UserPermissionCategoryForUserGroupsView(ListAPIView):
    """User Permission Category List View"""

    pagination_class = CustomLimitOffsetPagination
    permission_classes = [UserGroupSetupPermission]
    queryset = PermissionCategory.objects.filter(is_active=True, is_archived=False)
    serializer_class = UserPermissionCategorySerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = FilterForUserPermissionCategory
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    http_method_names = ["get", "head", "options"]


class UserGroupsForUserView(ListAPIView):
    permission_classes = [UserSetupPermission]
    queryset = UserGroup.objects.filter(
        Q(is_active=True) | ~Q(is_archived=True) | ~Q(is_system_managed=True),
    )
    serializer_class = UserGroupForUserSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ["id", "name", "codename", "is_active"]
    search_fields = ["id", "name", "codename", "is_active"]
    ordering_fields = ["id", "name"]
    ordering = ["name"]
