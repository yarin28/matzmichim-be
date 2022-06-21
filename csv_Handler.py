
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

    def reduce_phone_number(value: str) -> str:
        return ''.join(value.split('-'))

    def validate_phone_number(value: str) -> bool:
        value = Validator.reduce_phone_number(value)
        if len(value) != 10:
            return False
        prefix = value[0:3]
        return prefix in ('05' + str(digit) for digit in range(0, 10))


    def validate_email(value: str) -> bool:
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value) is not None
    
    def validate_full_name(value: str) -> bool:
        # return re.match(r'^[\w\s]+$', value) is not None
        if len(value.split()) <2:
            return False
        for name in value.split(" "):
            if len(name) ==0:
                return False
            for letter in name:
                if letter.isalpha():
                    continue
                else:
                    return False

class CsvHandler:
    #TODO: add more description to error messages
    def __init__(self):
        pass

    def validate_row(row:dict)->dict:
        #the result key should be added in the parent function not here
        row["RESULT"] = []
        if Validator.validate_israeli_id(row["ID"]) is False:
            row["RESULT"].append({"ERROR_PLACE":"ID","ERROR_MESSAGE": "ID is not valid"}) 
        if Validator.validate_email(row["Email"]) is False:
            row["RESULT"].append({"ERROR_PLACE":"Email","ERROR_MESSAGE": "EMAIL is not valid"})
        if Validator.validate_full_name(row["Full_name"]) is False:
            row["RESULT"].append({"ERROR_PLACE":"Full_name","ERROR_MESSAGE": "Full Name is not valid"})
        if Validator.validate_phone_number(row["Phone"]) is False:
            row["RESULT"].append({"ERROR_PLACE":"Phone","ERROR_MESSAGE": "Phone Number is not valid"})
        return row