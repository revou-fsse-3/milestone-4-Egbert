account_schema = {
    'user_id': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'account_type': {
        'type': 'string',
        'required': True
    },
    'account_number': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'balance': {
        'type': 'integer',
        'min': 1,
        'required': True
    }
}