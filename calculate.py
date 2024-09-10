def calculate_guest_rating(guest_rating: int) -> str:
    if guest_rating >= 8:
        return "Highly Satisfied"
    elif guest_rating >= 6:
        return "Satisfied"
    elif guest_rating >= 4:
        return "Neutral"
    else:
        return "Unsatisfied"