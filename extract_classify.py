def main(input_str: str) -> dict:
    try:
        # Remove any unnecessary characters
        cleaned_input = input_str.replace("'", "").strip()
        
        # Split the cleaned input string into class and amount
        class_name, amount = cleaned_input.split('=')
        
        # Strip any extra spaces
        class_name = class_name.strip()
        amount = int(amount.strip())

        return {
            "class": class_name,
            "amount": amount
        }
    except ValueError:
        # Handle the case where input_str doesn't contain '='
        return {
            "class": "v_0",
            "amount": 0
        }

input_str = "'v_1 = 10' \n"

print(main(input_str))
