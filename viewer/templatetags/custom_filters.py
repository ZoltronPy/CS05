from django import template

register = template.Library()


@register.filter
def generate_range(value):
    """
    Vytvoří range objekt pro iteraci v šabloně.
    Pokud je hodnota neplatná nebo není číslo, vrací prázdný range.
    """
    try:
        value = int(value)
        if value >= 0:
            return range(value)
    except (ValueError, TypeError):
        return range(0)


@register.filter
def sub(value, arg):
    """
    Odečte hodnotu `arg` od hodnoty `value`.
    """
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
