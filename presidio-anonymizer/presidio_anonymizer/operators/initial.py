# presidio_anonymizer/operators/initial.py
from presidio_anonymizer.operators import Operator, OperatorType

class Initial(Operator):
    """An operator that converts names to initials."""

    def operator_name(self) -> str:
        return "initial"

    def operator_type(self) -> OperatorType:
        # This operator anonymizes text
        return OperatorType.Anonymize

    def validate(self, text: str, params: dict = None) -> bool:
        # Minimal validation: always returns True
        return True

    def operate(self, text: str, params: dict = None) -> str:
        import re

        result = []
        # Split words by whitespace
        for word in text.strip().split():
            # Find first alphanumeric character
            match = re.search(r'\w', word)
            if match:
                initial = match.group(0).upper() + "."
                prefix = word[:match.start()]  # preserve leading chars
                result.append(prefix + initial)
        return " ".join(result)
