"""Authored train/calibration labels. Test labels live separately in evaluation/.
No financial amounts, household identities or test examples train the classifier.
"""
TRAIN = {
    'owner_id': ['Owner reference', 'Holder ID', 'Customer identity', 'Depositor identifier', 'Investor reference', 'Registered owner ID', 'Customer reference number', 'Account holder identity'],
    'account_id': ['Deposit reference', 'FD number', 'Certificate ID', 'Deposit account number', 'Fixed deposit identifier', 'Account reference', 'Term deposit receipt number', 'Certificate reference number'],
    'institution': ['Bank identifier', 'Institution', 'Bank code', 'Issuer institution', 'Issuing bank', 'Financial institution code', 'Bank reference', 'Institution ID'],
    'as_of': ['As of', 'Valuation date', 'Statement date', 'Balance date', 'Position date', 'Value as at', 'Date of observation', 'Reporting date'],
    'principal': ['Principal', 'Principal amount', 'Amount deposited', 'Deposit principal', 'Original invested amount', 'Initial deposit sum', 'Capital deposited', 'Principal balance'],
    'maturity_value': ['Maturity amount', 'Value at maturity', 'Maturity proceeds', 'Amount repayable on maturity', 'Maturity payout', 'Redemption value at maturity', 'Amount payable at expiry', 'Projected maturity amount'],
    'maturity_date': ['Maturity date', 'Date of maturity', 'Deposit expiry date', 'Matures on', 'Redemption date', 'Term end date', 'Date deposit matures', 'Expiry date'],
    'currency': ['Currency', 'Denomination', 'Currency code', 'Monetary unit', 'Amount currency', 'Deposit currency', 'Currency of account', 'Unit of account'],
    'ignore': ['Interest rate', 'Customer name', 'Address', 'Nominee', 'Bank balance', 'Total assets', 'Contact number', 'Branch address', 'Available balance', 'Total wealth', 'Instructions', 'Loan balance', 'Tax deducted', 'Interest accrued', 'Opening date', 'Issue date', 'Transaction amount', 'Current value', 'Balance', 'Value', 'Amount'],
}
CALIBRATION = {
    'owner_id': ['Depositor identity reference', 'Registered holder ID', 'Owner identifier'],
    'account_id': ['Deposit certificate reference', 'FD account reference', 'Certificate number'],
    'institution': ['Bank institution ID', 'Issuing institution code', 'Financial institution'],
    'as_of': ['Statement as of date', 'Reported position date', 'Balance as at date'],
    'principal': ['Original principal deposited', 'Invested principal amount', 'Initial capital deposited'],
    'maturity_value': ['Proceeds payable at maturity', 'Final maturity payout', 'Deposit maturity value'],
    'maturity_date': ['Scheduled maturity date', 'Deposit matures on', 'Certificate expiry date'],
    'currency': ['Principal currency', 'Reporting currency code', 'Monetary denomination'],
    'ignore': ['Annual yield', 'Total account value', 'Last login', 'Nominee reference', 'Tax reference', 'Available amount', 'Amount due', 'Future value'],
}
