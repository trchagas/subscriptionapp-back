from cerberus import Validator, errors


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[
        errors.MIN_LENGTH.code] = 'A senha precisa ter ao menos 6 dígitos.'
    messages[errors.REQUIRED_FIELD.code] = 'O campo é obrigatório.'
    messages[errors.BAD_TYPE.code] = 'O campo deve ter um formato válido.'
    messages[errors.EMPTY_NOT_ALLOWED.code] = 'O campo não pode ser vazio.'


def validate_UpdateAdmin(data):
    schema = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
    }
    v = Validator(schema,
                  error_handler=CustomErrorHandler,
                  ignore_none_values=True,
                  allow_unknown=True)
    v.validate(data)

    return v.errors
