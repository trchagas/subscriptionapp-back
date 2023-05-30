from cerberus import Validator, errors


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = 'O campo é obrigatório.'
    messages[errors.BAD_TYPE.code] = 'O campo deve ter um formato válido.'
    messages[errors.EMPTY_NOT_ALLOWED.code] = 'O campo não pode ser vazio.'
    messages[errors.UNALLOWED_VALUE.
             code] = 'O valor preenchido no campo deve ser válido'


def validate_UpdateSubscription(data):
    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'description': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'price': {
            'type': 'number',
            'required': True,
            'empty': False
        },
        'next_bill': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'billing_cycle': {
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'remind': {
            'type': 'boolean',
            'required': True,
            'empty': False
        },
        'is_continuous': {
            'type': 'boolean',
            'required': True,
            'empty': False
        },
        'is_active': {
            'type': 'boolean',
            'required': True,
            'empty': False
        },
        'background': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'category': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
    v = Validator(schema,
                  error_handler=CustomErrorHandler,
                  ignore_none_values=True)
    v.validate(data)

    return v.errors
