def calculate_return(starting_capital, final_value):
    return ((final_value - starting_capital) / starting_capital) * 100


def calculate_wfa_efficiency(in_sample_return, out_sample_return):
    if in_sample_return == 0:
        return 0
    return (out_sample_return / in_sample_return) * 100