import json

import pytest
from approvaltests import verify
from approval_utilities.utils import get_adjacent_file

from statement import statement


def test_example_statement():
    with open(get_adjacent_file("invoice.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("plays.json")) as f:
        plays = json.loads(f.read())
    verify(statement(invoice, plays))


def test_statement_with_new_play_types():
    with open(get_adjacent_file("invoice_new_plays.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("new_plays.json")) as f:
        plays = json.loads(f.read())
    with pytest.raises(ValueError) as exception_info:
        statement(invoice, plays)
    assert "unknown type" in str(exception_info.value)


def test_tragedy_audience_boundary_at_30():
    plays = {"hamlet": {"name": "Hamlet", "type": "tragedy"}}
    invoice = {
        "customer": "TragedyCo",
        "performances": [
            {"playID": "hamlet", "audience": 30},
            {"playID": "hamlet", "audience": 31},
        ],
    }
    assert statement(invoice, plays) == (
        "Statement for TragedyCo\n"
        " Hamlet: $400.00 (30 seats)\n"
        " Hamlet: $410.00 (31 seats)\n"
        "Amount owed is $810.00\n"
        "You earned 1 credits\n"
    )


def test_comedy_audience_boundary_at_20():
    plays = {"as-like": {"name": "As You Like It", "type": "comedy"}}
    invoice = {
        "customer": "ComedyCo",
        "performances": [
            {"playID": "as-like", "audience": 20},
            {"playID": "as-like", "audience": 21},
        ],
    }
    assert statement(invoice, plays) == (
        "Statement for ComedyCo\n"
        " As You Like It: $360.00 (20 seats)\n"
        " As You Like It: $468.00 (21 seats)\n"
        "Amount owed is $828.00\n"
        "You earned 8 credits\n"
    )
