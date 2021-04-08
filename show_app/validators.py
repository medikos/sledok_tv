from django.core.exceptions import ValidationError
import string



def password_form_validator(password):
    list_errors = [] 

    if len(password) < 8:
        list_errors.append("Не менее восьми символов")   

    if len(set(string.digits) - set(password)) == 10:
        list_errors.append('Нет ни одной цифры')
    
    if list_errors:
        raise ValidationError(list_errors)
    

    
