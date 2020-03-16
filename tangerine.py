import datetime, csv_helpers
from helpers import *
from transaction import Transaction
from pathlib import Path


def parse_csv_row(i, row):
    """Turn a CSV row from a Tangerine statement into Python objects. Also adds the CSV row number to the end of the row."""
    n_row = []
    for c in row:
        c = c.strip()
        if c == "": c = None

        n_row.append(c)
    n_row.append(i)

    try:
        n_row[0] = datetime.datetime.strptime(n_row[0], "%m/%d/%Y").date()
    except ValueError as e:
        print("Invalid date in row: '{}'".format(n_row[0]))
        print(e)
        return ()

    try:
        n_row[4] = float(n_row[4])
    except ValueError as e:
        print("Invalid amount in row: '{}'".format(n_row[4]))
        print(e)
        return ()

    return tuple(n_row)


def parse_trans(act, row):
    """Turn a CSV row from a Tangerine statement into a Transaction object."""
    return Transaction(csv_row_num=row[-1],
                       act=act,
                       date=row[0],
                       desc="{} | {}".format(row[2], row[3]),
                       amt=row[4])


def read_trans(path):
    """Read a given CSV file into a list of Transaction objects."""
    csv = csv_helpers.read_csv(path, parser=parse_csv_row)
    trans = []
    for i, row in enumerate(csv):
        if len(row) == 5+1:
            trans.append(parse_trans(path.name, row))
        else:
            print("Invalid row,", i)
    return trans


def read_statements(path):
    """Read all CSV files in given path into a single list of Transaction objects."""
    files = list_files(path)
    trans = []

    for f in files:
        trans.extend(read_trans(f))

    return trans


def unique_trans(trans):
    return list(set(trans))


def derive_balances(trans):
    """This will derive and fill in balances for all Transaction objects, given that Tangerine doesn't provide them."""
    for i, t in enumerate(trans):
        if i == 0:
            t.bal_af = t.amt
        else:
            t.bal_af = trans[i-1].bal_af + t.amt


def get_statements(path):
    trans = read_statements(path)
    trans = unique_trans(trans)

    return trans


def load():
    transactions = get_statements(Path("statements/tangerine"))
    # [Transaction]

    accounts = act_wise(transactions)
    # {act: [Transaction]}

    for act, trans in accounts.items():
        derive_balances(trans)

    act_date = date_wise(accounts)
    # {act: {date: [Transaction]}}

    act_bals = daily_balances(act_date)
    # {act: {date: balance}}

    return act_bals
