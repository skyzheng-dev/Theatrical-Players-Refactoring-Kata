from statement import statement


PLAYS = {"henry-v": {"name": "Henry V", "type": "historical"}}


def test_historical_example_from_spec():
    invoice = {
        "customer": "HistoryCo",
        "performances": [{"playID": "henry-v", "audience": 35}],
    }
    assert statement(invoice, PLAYS) == (
        "Statement for HistoryCo\n"
        " Henry V: $725.00 (35 seats)\n"
        "Amount owed is $725.00\n"
        "You earned 7 credits\n"
    )


def test_historical_audience_boundary_at_20():
    invoice = {
        "customer": "HistoryCo",
        "performances": [
            {"playID": "henry-v", "audience": 20},
            {"playID": "henry-v", "audience": 21},
        ],
    }
    assert statement(invoice, PLAYS) == (
        "Statement for HistoryCo\n"
        " Henry V: $500.00 (20 seats)\n"
        " Henry V: $515.00 (21 seats)\n"
        "Amount owed is $1,015.00\n"
        "You earned 8 credits\n"
    )


def test_historical_with_original_play_types():
    plays = {
        "hamlet": {"name": "Hamlet", "type": "tragedy"},
        "as-like": {"name": "As You Like It", "type": "comedy"},
        "henry-v": {"name": "Henry V", "type": "historical"},
    }
    invoice = {
        "customer": "MixedCo",
        "performances": [
            {"playID": "hamlet", "audience": 55},
            {"playID": "as-like", "audience": 35},
            {"playID": "henry-v", "audience": 35},
        ],
    }
    assert statement(invoice, plays) == (
        "Statement for MixedCo\n"
        " Hamlet: $650.00 (55 seats)\n"
        " As You Like It: $580.00 (35 seats)\n"
        " Henry V: $725.00 (35 seats)\n"
        "Amount owed is $1,955.00\n"
        "You earned 44 credits\n"
    )
