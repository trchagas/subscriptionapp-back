from cerberus import Validator, errors
from validator.CustomRules import email


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = 'O campo é obrigatório.'
    messages[errors.BAD_TYPE.code] = 'O campo deve ter um formato válido.'
    messages[errors.EMPTY_NOT_ALLOWED.code] = 'O campo não pode ser vazio.'
    messages[errors.UNALLOWED_VALUE.
             code] = 'O valor preenchido no campo deve ser válido'


def validate_StoreClient(data):
    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'password': {
            'type': 'string',
            'minlength': 6,
            'required': True
        },
        'email': {
            'type': 'string',
            'check_with': email
        },
    }
    v = Validator(schema,
                  error_handler=CustomErrorHandler,
                  ignore_none_values=True)
    v.validate(data)

    return v.errors
