transaction_schema = {
    'from_account_id': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'to_account_id': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'amount': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'type': {
        'type': 'string',
        'required': True
    },
    'description': {
        'type': 'string',
        'required': True
    }
}