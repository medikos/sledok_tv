from django import template

register = template.Library()


@register.filter(name='status')
def status(value: str) -> str:
    tuple_ = (
        ('unknown', ''),
        ('Running', 'Продолжается'),
        ('Ended', 'Закончился'),
        ('To Be Determined', 'Приостановленный'),
        ('In Development', 'В разработке')

    )
    return {en: ru for en, ru in tuple_}[value]
