from cerberus import Validator, errors


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[
        errors.MIN_LENGTH.code] = 'A senha precisa ter ao menos 6 dígitos.'
    messages[errors.REQUIRED_FIELD.code] = 'O campo é obrigatório.'
    messages[errors.REGEX_MISMATCH.code] = 'O e-mail informado é inválido.'
    messages[errors.BAD_TYPE.code] = 'O campo deve ter um formato válido.'


def validate_SessionUser(data):
    schema = {
        'email': {
            'type': 'string',
            'required': True,
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        },
        'password': {
            'type': 'string',
            'minlength': 6,
            'required': True
        }
    }
    v = Validator(schema,
                  error_handler=CustomErrorHandler,
                  ignore_none_values=True,
                  allow_unknown=True)
    v.validate(data)

    return v.errors
