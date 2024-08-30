# SECTION ENUMS
# Used in models.py: Model - Account, Security, Crypto, Transactions

SOURCE_CHOICES = [
    ('MANUAL', 'Manual'),
    ('SNAPTRADE', 'SnapTrade'),
    ('PLAID', 'Plaid'),
]

TRANSACTION_TYPE_CHOICES = [
    ('BUY', 'Buy'),
    ('SELL', 'Sell'),
    ('BUY_TO_OPEN', 'Buy to Open'),
    ('BUY_TO_CLOSE', 'Buy to Close'),
    ('SELL_TO_OPEN', 'Sell to Open'),
    ('SELL_TO_CLOSE', 'Sell to Close'),
    ('DIVIDEND', 'Dividend'),
    ('INTEREST', 'Interest'),
    ('RENTAL_INCOME', 'Rental Income'),
    ('DEPOSIT', 'Deposit'),
    ('WITHDRAWAL', 'Withdrawal'),
    ('CONTRIBUTION', 'Contribution'),
    ('TRANSFER', 'Transfer'),
    ('FEE', 'Fee'),
    ('EXPENSE', 'Expense'),
    ('PAYMENT', 'Payment'),
    ('APPRECIATION', 'Appreciation'),
    ('DEPRECIATION', 'Depreciation'),
    ('OTHER', 'Other'),
]


# SECTION Default Asset Groups
#These are the constant variables used by signals.py and models.py
#The purpose of this module is to prevent repeated objects.

PORTFOLIO_GROUP_CONFIG = {
    "name": "My Portfolio",
    "description": "Top level overview of your net worth",
    "parent_group_id": None,
    "target_weighting": None,
    "sort": 0
}

UNGROUPED_GROUP_CONFIG = {
    "name": "Ungrouped",
    "description": "Ungrouped assets and liabilities are kept here",
    "parent_group_id": None,  # This will be set dynamically to the actual portfolio group
    "target_weighting": None,
    "sort": 1
}
