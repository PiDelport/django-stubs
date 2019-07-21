from typing import Any, Collection, Optional, Set, Tuple, Type, Union

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser, BaseUserManager as BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.db.models.manager import EmptyManager

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

def update_last_login(sender: Type[AbstractBaseUser], user: AbstractBaseUser, **kwargs: Any) -> None: ...

class PermissionManager(models.Manager):
    def get_by_natural_key(self, codename: str, app_label: str, model: str) -> Permission: ...

class Permission(models.Model):
    content_type_id: int
    name: models.CharField = ...
    content_type: models.ForeignKey = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    codename: models.CharField = ...
    def natural_key(self) -> Tuple[str, str, str]: ...

class GroupManager(models.Manager):
    def get_by_natural_key(self, name: str) -> Group: ...

class Group(models.Model):
    name: models.CharField = ...
    permissions: models.ManyToManyField = models.ManyToManyField(Permission)
    def natural_key(self): ...

class UserManager(BaseUserManager):
    def create_user(
        self, username: str, email: Optional[str] = ..., password: Optional[str] = ..., **extra_fields: Any
    ) -> AbstractUser: ...
    def create_superuser(
        self, username: str, email: Optional[str], password: Optional[str], **extra_fields: Any
    ) -> AbstractBaseUser: ...

class PermissionsMixin(models.Model):
    is_superuser: models.BooleanField = ...
    groups: models.ManyToManyField = models.ManyToManyField(Group)
    user_permissions: models.ManyToManyField = models.ManyToManyField(Permission)
    def get_group_permissions(self, obj: None = ...) -> Set[str]: ...
    def get_all_permissions(self, obj: Optional[str] = ...) -> Set[str]: ...
    def has_perm(self, perm: str, obj: Optional[str] = ...) -> bool: ...
    def has_perms(self, perm_list: Collection[str], obj: None = ...) -> bool: ...
    def has_module_perms(self, app_label: str) -> bool: ...

class AbstractUser(AbstractBaseUser, PermissionsMixin):  # type: ignore
    username_validator: UnicodeUsernameValidator = ...
    username: models.CharField = ...
    first_name: models.CharField = ...
    last_name: models.CharField = ...
    email: models.EmailField = ...
    is_staff: models.BooleanField = ...
    date_joined: models.DateTimeField = ...
    EMAIL_FIELD: str = ...
    USERNAME_FIELD: str = ...
    def clean(self) -> None: ...
    def get_full_name(self) -> str: ...
    def get_short_name(self) -> str: ...
    def email_user(self, subject: str, message: str, from_email: str = ..., **kwargs: Any) -> None: ...

class User(AbstractUser): ...

class AnonymousUser:
    id: Any = ...
    pk: Any = ...
    username: str = ...
    is_staff: bool = ...
    is_active: bool = ...
    is_superuser: bool = ...
    def save(self) -> Any: ...
    def delete(self) -> Any: ...
    def set_password(self, raw_password: str) -> Any: ...
    def check_password(self, raw_password: str) -> Any: ...
    @property
    def groups(self) -> EmptyManager: ...
    @property
    def user_permissions(self) -> EmptyManager: ...
    def get_group_permissions(self, obj: None = ...) -> Set[Any]: ...
    def get_all_permissions(self, obj: Any = ...) -> Set[str]: ...
    def has_perm(self, perm: str, obj: None = ...) -> bool: ...
    def has_perms(self, perm_list: Collection[str], obj: None = ...) -> bool: ...
    def has_module_perms(self, module: str) -> bool: ...
    @property
    def is_anonymous(self) -> bool: ...
    @property
    def is_authenticated(self) -> bool: ...
    def get_username(self) -> str: ...
