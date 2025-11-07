from django import template

register = template.Library()


@register.filter
def has_role(user, role_name: str) -> bool:
    if not hasattr(user, "is_authenticated") or not user.is_authenticated:
        return False
    if getattr(user, "is_superuser", False):
        return True
    return getattr(user, "role", None) == role_name


@register.simple_tag(takes_context=True)
def user_role(context):
    user = context.get("user")
    return getattr(user, "role", None)

