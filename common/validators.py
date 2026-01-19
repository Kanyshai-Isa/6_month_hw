from datetime import date, datetime
from rest_framework.exceptions import ValidationError

def validate_age(request):
    token = request.auth

    if not token:
        raise ValidationError("Срок сессии истек")

    birthdate_str = token.get("birthdate")

    if not birthdate_str:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    try:
        birthdate = datetime.fromisoformat(birthdate_str).date()
    except ValueError:
        raise ValidationError("Некорректная дата рождения в токене")

    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
