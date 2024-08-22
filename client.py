BASE_URL = "http://ec2-3-27-212-239.ap-southeast-2.compute.amazonaws.com"

def parse_json(body):
    # Basic JSON parser for this specific example
    data_section = body.split('"data":{')[1].rsplit('}', 1)[0]
    data_items = data_section.split(',')
    data = {}
    for item in data_items:
        key, value = item.split(':', 1)
        key = key.strip().strip('"')
        value = value.strip().strip('"').strip('}')
        if key == "amount":
            value = int(value)  # Convert to float
        data[key] = value
    return data

def main(status_code, conversation_id, body):
    post_url = f"{BASE_URL}/?conversation_id={conversation_id}"

    if status_code == 200:
        body_obj = parse_json(body)
        purpose = str(body_obj.get('purpose', 'None'))

        return {
            "post_url": post_url,
            "chat_history": body_obj.get("chat_history", "Start:"),
            "can_promote": body_obj.get("can_promote", "True"),
            "product_type": body_obj.get("product_type", "None"),
            "purpose": purpose,
            "is_necessary": body_obj.get("is_necessary", "None"),
            "amount": body_obj.get("amount", 0)  # Use parsed amount
        }
    
    else:
        # Define the endpoint for creating customer info
        # Return the URL and the payload
        return {
            "post_url": post_url,
            "chat_history": "Start:",
            "can_promote": "True",  # Default value
            "product_type": "None",    # Default value
            "purpose": "None",         # Default value
            "is_necessary": "None", # Default value
            "amount": 0         # Default value
        }
