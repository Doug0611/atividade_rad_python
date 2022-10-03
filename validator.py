from dataclasses import dataclass


@dataclass
class Validator:
    @staticmethod
    def validate_field_name(field: str) -> bool:
        data = field.split()
        is_valid = True
        if len(data) <= 1:
            is_valid = False
        for char in field:
            if char.isdigit():
                is_valid = False
        return is_valid

    @staticmethod
    def validate_field_gender(field) -> bool:
        is_valid = True
        if len(field) > 1 or len(field) < 1:
            is_valid = False
        if field not in ["M", "m", "F", "f"]:
            is_valid = False
        return is_valid

    @staticmethod
    def validade_field_scores(*field) -> bool:
        is_valid = True
        for score in field:
            if len(str(score)) < 3 or len(str(score)) > 4:
                is_valid = False
        return is_valid
