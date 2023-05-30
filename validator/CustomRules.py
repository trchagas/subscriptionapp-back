from validate_docbr import CPF, CNPJ
import validators, datetime
import re
from models.User import User

cpf_aux = CPF()
cnpj_aux = CNPJ()


def day(field, value, error):
    if value < 1 or value > 31:
        error(field, 'O dia informado é inválido.')


def month(field, value, error):
    if value < 1 or value > 12:
        error(field, 'O mês informado é inválido.')


def year(field, value, error):
    date = datetime.datetime.now()
    if value < 1900 or value > date.year:
        error(field, 'O ano informado é inválido.')


def state(field, value, error):
    states = [
        'AC',
        'AL',
        'AP',
        'AM',
        'BA',
        'CE',
        'DF',
        'ES',
        'GO',
        'MA',
        'MT',
        'MS',
        'MG',
        'PA',
        'PB',
        'PR',
        'PE',
        'PI',
        'RJ',
        'RN',
        'RS',
        'RO',
        'RR',
        'SC',
        'SP',
        'SE',
        'TO',
    ]
    if value not in states:
        error(field, 'O estado informado é inválido.')


def cep(field, value, error):
    if not value:
        return
    pattern = re.compile("\d{5}-?\d{3}")

    if not pattern.match(value):
        error(field, 'O CEP informado é inválido.')


def url(field, value, error):
    if not value:
        return

    pattern = re.compile(
        "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    )
    if not pattern.match(value):
        error(field, 'O endereço URL informado é inválido.')


def phone(field, value, error):
    pattern = re.compile(
        "^\\(?[1-9]{2}\\)? ?(?:[2-8]|9[1-9])[0-9]{3}\\-?[0-9]{4}$")
    if not pattern.match(value):
        error(field, 'O número de telefone informado é inválido.')


def clientEmail(field, value, error):
    if not validators.email(value):
        error(field, 'O e-mail informado é inválido.')


def email(field, value, error):
    if not validators.email(value):
        error(field, 'O e-mail informado é inválido.')

    emailAlreadyRegistered = User.query.filter_by(email=value).first()
    if emailAlreadyRegistered:
        error(field, 'O e-mail informado já está cadastrado no sistema.')


def cpf(field, value, error):
    if not cpf_aux.validate(value):
        error(field, 'O CPF informado é inválido.')


def cnpj(field, value, error):
    if not cnpj_aux.validate(value):
        error(field, 'O CNPJ informado é inválido.')