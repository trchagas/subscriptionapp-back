from cerberus import Validator, errors


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = 'O campo é obrigatório.'
    messages[errors.BAD_TYPE.code] = 'O campo deve ter um formato válido.'
    messages[errors.EMPTY_NOT_ALLOWED.code] = 'O campo não pode ser vazio.'
    messages[errors.UNALLOWED_VALUE.
             code] = 'O valor preenchido no campo deve ser válido'


def validate_StoreSubscription(data):
    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'description': {
            'type': 'string',
        },
        'price': {
            'type': 'number',
            'required': True,
        },
        'next_bill': {
            'type': 'string',
        },
        'billing_cycle': {
            'type': 'integer',
        },
        'remind': {
            'type': 'boolean',
        },
        'is_continuous': {
            'type': 'boolean',
        },
        'is_active': {
            'type': 'boolean',
        },
        'background': {
            'type': 'string',
        },
        'category': {
            'type': 'string',
            'required': True,
        }
    }
    v = Validator(schema,
                  error_handler=CustomErrorHandler,
                  ignore_none_values=True)
    v.validate(data)

    return v.errors
