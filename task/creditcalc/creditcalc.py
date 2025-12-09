import math
import argparse


############################################################################################################
# Examples:
#
# > python creditcalc.py --type=diff --principal=1000000 --periods=10 --interest=10
# Month 1: payment is 108334
# Month 2: payment is 107500
# Month 3: payment is 106667
# Month 4: payment is 105834
# Month 5: payment is 105000
# Month 6: payment is 104167
# Month 7: payment is 103334
# Month 8: payment is 102500
# Month 9: payment is 101667
# Month 10: payment is 100834
#
# Overpayment = 45837
# ----------------------------------------------------------------------------------------------------------
# > python creditcalc.py --type=annuity --principal=1000000 --periods=60 --interest=10
# Your annuity payment = 21248!
# Overpayment = 274880
# ----------------------------------------------------------------------------------------------------------
# > python creditcalc.py --type=diff --principal=1000000 --payment=104000
# Incorrect parameters.
# ----------------------------------------------------------------------------------------------------------
# > python creditcalc.py --type=diff --principal=500000 --periods=8 --interest=7.8
# Month 1: payment is 65750
# Month 2: payment is 65344
# Month 3: payment is 64938
# Month 4: payment is 64532
# Month 5: payment is 64125
# Month 6: payment is 63719
# Month 7: payment is 63313
# Month 8: payment is 62907
#
# Overpayment = 14628
# ----------------------------------------------------------------------------------------------------------
# > python creditcalc.py --type=annuity --payment=8722 --periods=120 --interest=5.6
# Your loan principal = 800018!
# Overpayment = 246622
# ----------------------------------------------------------------------------------------------------------
# > python creditcalc.py --type=annuity --principal=500000 --payment=23000 --interest=7.8
# It will take 2 years to repay this loan!
# Overpayment = 52000
############################################################################################################


# write your code here

def print_return_input():
    print("> ", end="")
    return input()


def nominal_interest(i_rate):
    return i_rate / (12 * 100)


parser = argparse.ArgumentParser(prog="Loan Calculator",
                                 description="Personal finance can be tricky, but it doesn't have to be! "
                                             "This project helps you understand loans and mortgages with a handy "
                                             "calculator.")

parser.add_argument("--payment", nargs='?', type=float, help='The payment amount. '
                                                             'It can be calculated using the provided principal, '
                                                             'interest, and number of months')
parser.add_argument("--principal", nargs='?', type=float, help='You can get its value if you know the '
                                                               'interest, annuity payment, and number of months.')
parser.add_argument("--periods", nargs='?', type=int, help='denotes the number of months needed to '
                                                           'repay the loan. It\'s calculated based on the interest, '
                                                           'annuity payment, and principal.')
parser.add_argument("--interest", nargs='?', type=float, help='is specified without a percent sign. Note '
                                                              'that it can accept a floating-point value. Our loan '
                                                              'calculator can\'t calculate the interest, so it must '
                                                              'always be provided.')
parser.add_argument("--type", help='The --type argument is indicating the type of payment: '
                                   '"annuity" or "diff" (differentiated). '
                                   'It must always be provided in any run.')

args = parser.parse_args()

## assign passed arguments
payment = args.payment
principal = args.principal
periods = args.periods
interest = args.interest
type_parameter = args.type

## class member
calc_sum = 0
ANNUITY = "annuity"
DIFF = "diff"

# calculate nominal interest
if interest:
    interest = nominal_interest(interest)

param_list = {payment, principal, periods, interest, type_parameter}


## logical selection of functions
def program_run_conditions():
    if not type_parameter:
        print_incorrect_params_and_exit()
    elif type_parameter != ANNUITY and type_parameter != DIFF:
        print_incorrect_params_and_exit()
    elif type_parameter == DIFF and payment:
        print_incorrect_params_and_exit()
    elif type_parameter == ANNUITY and not interest:
        print_incorrect_params_and_exit()
    elif check_if_values_negative():
        print_incorrect_params_and_exit()
    elif count_num_of_parameters() < 4:
        print_incorrect_params_and_exit()
    else:
        pass


def check_if_values_negative():
    for i in param_list:
        if isinstance(i, (int, float)) and i < 0:
            return True
    else:
        return False


def count_num_of_parameters():
    num_of_parameter = 0
    for i in param_list:
        if i is not None:
            num_of_parameter += 1
    return num_of_parameter


def print_incorrect_params_and_exit():
    print("Incorrect parameters")
    exit()


# p = payment, i = monthly interest in 12% = 0.01 , n = number of payments
def annuity_payment(p, i, n):
    counter = i * (1 + i) ** n
    denominator = ((1 + i) ** n) - 1
    temp = counter / denominator
    return p * temp


def calculate_loan_principal(a, i, n):
    below_fraction = i * (1 + i) ** n
    below_denominator = ((1 + i) ** n) - 1
    below_result = below_fraction / below_denominator
    return a / below_result


def calculate_number_of_payments(credit, rate, i_rate):
    fraction_denominator = rate - (i_rate * credit)
    fraction = rate / fraction_denominator
    base = 1 + i_rate
    return math.log(fraction, base)


def calculate_years(months):
    return months // 12


def calculate_months(months, years):
    remainder = months % 12
    return remainder


def get_duration_text(years, months):
    if years > 0 and months > 0:
        return f'It will take {years} years and {months} months to repay this loan!'
    elif years > 0 and months == 0:
        return f'It will take {years} years to repay this loan!'
    elif years == 0 and months > 0:
        return f'It will take {months} months to repay this loan!'
    else:
        return 'There is neither a year nor a month, and that should not happen.'


def build_and_print_duration_text(months):
    years = calculate_years(months)
    months = calculate_months(months, years)
    text = get_duration_text(years, months)
    print(text)


def calc_print_differentiate_payments(p_loan, n_periods, i):
    dp_sum = 0
    for n in range(1, n_periods + 1):
        result = calc_differentiate_payments_steps(n, p_loan, n_periods, i)
        result = math.ceil(result)
        dp_sum += result
        print(f'Month {n}: payment is {result}')
    overpayment = int(dp_sum - p_loan)
    print(f'Overpayment = {overpayment}')


def calc_differentiate_payments_steps(step, p_loan, n_periods, i):
    return (p_loan / n_periods) + i * (p_loan - (p_loan * (step - 1) / n_periods))


## check user input
program_run_conditions()

## calculation decision
# ---> calculate number of months
if type_parameter == ANNUITY and principal and interest and payment and not periods:
    value = calculate_number_of_payments(principal, payment, interest)
    value = math.ceil(value)
    build_and_print_duration_text(value)
    overpayment = int((payment * value) - principal)
    print(f'Overpayment = {overpayment}')
# ---> calculate monthly payment (ordinary annuit)
elif type_parameter == ANNUITY and principal and periods and interest and not payment:
    print("You should calculate the monthly payment.")
    pay_per_month = annuity_payment(principal, interest, periods)
    pay_per_month = math.ceil(pay_per_month)
    print(f'Your annuity payment = {pay_per_month}!')
    overpayment = int((pay_per_month * periods) - principal)
    print(f'Overpayment = {overpayment}')
# ---> calculate loan principal
elif type_parameter == ANNUITY and periods and interest and payment and not principal:
    value = calculate_loan_principal(payment, interest, periods)
    value = int(value)
    print(f'Your loan principal = {value}!')
    overpayment = int((payment * periods) - value)
    print(f'Overpayment = {overpayment}')
elif type_parameter == DIFF:
    calc_print_differentiate_payments(principal, periods, interest)
else:
    print("Something went wrong. Please check your input. ")
