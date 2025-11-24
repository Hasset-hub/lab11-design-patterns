import pytest
from presidio_anonymizer.operators import Initial

def test_correct_name():
    assert Initial().operator_name() == "initial"

@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("John Smith", "J. S."),
        ("     Eastern    Michigan   University ", "E. M. U."),  # extra whitespace
        #("@abc", "@A."),  # leading non-alphanumeric
        #("--**abc", "--**A."),  # leading symbols
    ]
)
def test_given_value_for_initial(input_text, expected):
    text = Initial().operate(input_text)
    assert text == expected
