def calculate_match_percentage(customer_measurements, product_measurements):

    total_score = 0.0
    count = 0
    threshold = 0.95

    for key,product_value in product_measurements.items():
            customer_value = customer_measurements[key]
            product_value = product_measurements[key]
            score  = (product_value - customer_value) / customer_value
            if score < 0:
                score = abs(score)
            else:
                score = threshold - score

            count += 1
            total_score += score


    if count == 0:
        return 0.0

    match_percentage = (total_score / count) * 100
    return match_percentage

