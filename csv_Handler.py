
import re

class Validator:

    def validate_israeli_id(value: str) -> bool:
        check_digit = 0
        weight_sum = 0
        temp = 0

        for i in range(len(value) - 1):
            if i % 2 == 0:
                temp = int(value[i])
            else:
                temp = int(value[i]) * 2

            if temp > 10:
                weight_sum += (temp % 10) + int(temp / 10)
            else:
                weight_sum += temp

        while (weight_sum + check_digit) % 10 != 0:
            check_digit += 1

        return str(check_digit) == value[-1]


    def validate_email(value: str) -> bool:
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value) is not None
    
