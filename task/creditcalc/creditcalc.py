import math
import argparse


# write your code here

def print_return_input():
    print("> ", end="")
    return input()


# print("Enter the loan principal:")
# loan_principal = int(print_return_input())
#
# def number_of_month_payments():
#     print("Enter the monthly payment:")
#     monthly_amount = int(print_return_input())
#     monthly_amount = math.ceil(loan_principal / monthly_amount)
#     return monthly_amount
#
# def amount_per_month():
#     print('Enter the number of months:')
#     num_of_months = int(print_return_input())
#     regular_amount = math.ceil(loan_principal / num_of_months)
#     last_payment = loan_principal - (num_of_months - 1) * regular_amount
#     print(f'Your monthly payment = {regular_amount} and the last payment = {last_payment}.')
#
# print("What do you want to calculate?")
# print('type "m" - for number of monthly payments,')
# print('type "p" - for the monthly payment:')
#
# # input selection of process
# selection = print_return_input()
# if selection == "m":
#     monthly_payment = number_of_month_payments()
#     print(f"It will take {monthly_payment} months to repay the loan")
# elif selection == "p":
#     amount_per_month()
#     exit()

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
parser.add_argument("--periods", nargs='?', type=float, help='denotes the number of months needed to '
                                                             'repay the loan. It\'s calculated based on the interest, '
                                                             'annuity payment, and principal.')
parser.add_argument("--interest", nargs='?', type=float, help='is specified without a percent sign. Note '
                                                              'that it can accept a floating-point value. Our loan '
                                                              'calculator can\'t calculate the interest, so it must '
                                                              'always be provided.')
parser.add_argument("--type", required=True, help='The --type argument is indicating the type of payment: '
                                                  '"annuity" or "diff" (differentiated). '
                                                  'It must always be provided in any run.')

args = parser.parse_args()

## assign passed arguments
payment = args.payment
principal = args.principal
periods = args.periods
interest = args.interest

# calculate nominal interest
if interest:
    interest = nominal_interest(interest)
    # print('nominal interest set to:', interest)


## logical selection of functions

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


## calculation decision
# ---> calculate number of months
if principal and interest and payment and not periods:
    value = calculate_number_of_payments(principal, payment, interest)
    value = math.ceil(value)
    build_and_print_duration_text(value)
# ---> calculate monthly payment (ordinary annuit)
elif principal and periods and interest and not payment:
    print("You should calculate the monthly payment.")
    pay_per_month = annuity_payment(principal, interest, periods)
    pay_per_month = math.ceil(pay_per_month)
    print(f'Your monthly payment = {pay_per_month}!')
# ---> calculate loan principal
elif periods and interest and payment and not principal:
    value = calculate_loan_principal(payment, interest, periods)
    value = int(value)
    print(f'Your loan principal = {value}!')
else:
    print("Something went wrong. Please check your input. ")
