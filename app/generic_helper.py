import re


def extracting_session_id(session_string: str):
    match = re.search(r"\/sessions\/(.*)\/contexts\/", session_string)
    if match:
        session_id = match.group(1)
        return str(session_id)
    return ""


def get_str_from_food_dict(food_dict: dict) -> str:
    return ", ".join(f"{int(value)} {key}" for key, value in food_dict.items())


if __name__ == "__main__":
    print(
        extracting_session_id(
            "projects/ion-xdjr/agent/sessions/037f16a1-8a67-bb1e-30eb-f21aa8553a0f/contexts/ongoing-order"
        )
    )
    print(get_str_from_food_dict({"pizza": 2, "samosa": 1}))
