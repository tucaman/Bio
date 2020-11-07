import numpy as np
import pandas as pd

# Variance of Bernoulli trial: E(X^2) - [E(X)]^2
e_x_2 = 0.05 * 60.5**2 + 0.95 * -1**2
e_x = 0.05 * 60.5 - 0.95 * 1
e_x**2
var_tot = e_x_2 - e_x**2
sd_tot = np.sqrt(var_tot)
(sd_tot + 1)**0.1

# -------------------------------------------------------------------------------------
# Annuity
pv = 500000
r = 0.12

c= pv / (1/r * (1 -  (1+r)**(-5)) )
c

# -------------------------------------------------------------------------------------
# Inflation
r_nominal = 0.055
i = 0.02
N = 10000
W_10 = N * (1+r_nominal)**10
print(' nominal investment balance at the end of year 10', W_10)
W_10_tilde = W_10/(1+i)**10
print('  purchasing power in year 0 dollars', W_10_tilde)

# Suppose CPI increases at a rate of 2% per year, while BRDPI grows at 3% per year.
# How long, in years, does it take for prices to double under

r=0.02
n = np.log(2)/np.log(1+r)
print('...under CPI:', n)

r=0.03
n = np.log(2)/np.log(1+r)
print('...under BRDPI:', n)

# BRDPI
w_insurance = 0.5
g_insurance = 0.04
w_medical_products = w_medical_services = 0.25
g_medical_products = 0.01
g_medical_services = 0.02

i = w_insurance * g_insurance + w_medical_products * g_medical_products + w_medical_services * g_medical_services
print('the annual inflation rate of HCI', i)

# The time value of money
-10 + 0.9 * 5 + 0.8 * 7
# Present and Future Value
1047.62 * 1.05
1100/1.05
# Flu Vaccine Example
npv = -1  +0.5/1.05 +0.4/1.05**2 + 0.3/1.05**3
print('NPV Strategy A:', npv)
npv = -0.2 - 0.2/1.05  +0.3/1.05**2 + 0.3/1.05**3
print('NPV Strategy B:', npv)

# Annuity Example
c = 100
r = 0.1
T = 14
npv = c/r - c/r * 1/(1+r)**T
print('NPV cash flows:', npv)

# Problem 1
# AZ Biotech's after-tax cash flow is $10 million (at the end of) this year and expected to grow at 5% per year forever.
# The appropriate discount rate is 9%. What is the present value of AZ Biotech's after-tax cash flow?
# (Note: Your answer should be expressed in units of millions of dollars.)
c = 10
g = 0.05
r = 0.09
npv = c/(r-g)
print('NPV cash flows:', npv)

# Problem 2
# LifeWorks owns a drug patent that generates $45 million in licensing fees per year starting at the beginning of
# this year (year 0).
# The patent expires in 10 years, after which no licensing fees will be generated (i.e., licensing fee revenues
# for years 10 and beyond will be $0). The discount rate is 12% per year.
# What is the present value of the patent's cash flows?
# (Note: Your answer should be expressed in units of millions of dollars.)
T = 10
r = 0.12
c = 45
npv =c/r * (1 - 1/(1+r) ** (T-1)) + c
print('NPV cash flows:', npv)

# Problem 3
r = 0.06
npv_A = -2000 + 750/(1+r)**1+ 600/(1+r)**2+ 500/(1+r)**3+ 400/(1+r)**4+ 300/(1+r)**5
npv_B = -1000 - 500/(1+r) + 525/(1+r)**2+ 525/(1+r)**3+ 525/(1+r)**4+ 525/(1+r)**5
print('npv_a', npv_A)
print('npv_b', npv_B)

# Problem 4
r=0.1
option_a = 25/r
option_a

r=0.1
g=0.03
option_b = 15/(r-g)
option_b

r=0.1
c=27.5
T=25
option_c = c/r *(1 - 1/(1+r)**25)
option_c

r=0.1
g=0.03
c=22.5
T=25
option_d = c/(r-g) * (1 - (1+g)**T/(1+r)**T)
option_d

# Problem 5
T = 10
r = 0.4167/100
N = 84000
T_months = 10 * 12

#We need to solve for c
# N = c/r * (1 - 1/(1+r)**T_months)
# which gives
c = r * N/(1 - 1/(1+r)**T_months)
print('monthly payment for Sovaldi', c)
# check numbers
total = 0
for i in range(120):
    print(i)
    total += c/(1+r)**(i+1)

# -------------------------------------------------------------------------------------------------------
# Week 2

# Exercise: Expansion Decision
N = 8.5
c = 1
g = 0.025
r = 0.134
-N + c/(r-g)


# Exercise: IRR
cf = [-3, 1.5, 1.3, 1.05, 0.9, 0.75]
np.irr(cf)

# Accounting Variables to Cash Flows
N = 100
depreciation = 100/2
revenue = 80
cost_of_revenue = 25
tax_rate = 0.3
r = 0.06
cf_0 = -N
cf_1 = cf_2 = (revenue - cost_of_revenue) * (1-tax_rate) + depreciation * tax_rate
npv = cf_0 + cf_1/(1+r) + cf_2/(1+r)**2
print('npv:', npv)

# Internal Rate of Return
np.irr([cf_0, cf_1, cf_2])

# Working Capital = Inventory + Accounts_receivable + Accounts_payable
inventory_Q1 = 3 = working_capital_q1

inventory_Q2 = 0
sales_Q2 = 5 = Accounts_receivable_q2
working_capital_q2 = inventory_Q2 + Accounts_receivable_Q2

inventory_Q3 = 0
Accounts_receivable_Q3 = 0
working_capital_q3 = inventory_Q3 + Accounts_receivable_Q3

#  -------------------------------------------------------
# Valuing a Company
shares_out = 2.5
debt = 40
cost_of_capital = 0.15
tax_rate = 0.35
g = 0.03

# calculate the yearly cash flows
sales = [100,108,116.6,126,136,146.9,158.7,171.4]
cogs = [70,75.6,81.6,88.2,95.2,102.9,111.1,120]
depreciation = [3.2,10,10.8,11.2,12,12.4,12.9,13.2]
capex = [12,15.1,16.3,17.5,15.5,16.2,16.8,16.3]
working_capital = [16,17.3,18.7,20.2,21.8,23.5,25.4,27.4]
delta_working_capital = [0] + [working_capital[i] - working_capital[i-1] for i in range(len(working_capital)) if i >0]

# convert to numpy arrays
sales = np.array(sales)
cogs = np.array(cogs)
depreciation = np.array(depreciation)
capex = np.array(capex)
delta_working_capital = np.array(delta_working_capital)

cash_flows = (sales - cogs) * (1-tax_rate) + depreciation * tax_rate - delta_working_capital - capex
pv_cf_1_7 = [cash_flows[i]/(1+cost_of_capital)**i for i in range(len(cash_flows)) if i >0]
pv_cf= np.array(pv_cf_1_7).sum()
print('pv of cash flows years 1-7=', pv_cf)

terminal_value = cash_flows[-1]  *(1+g)/ (cost_of_capital-g) * 1/(1+cost_of_capital)**7
print('terminal value=', terminal_value)

total_pv = pv_cf + terminal_value
print('total_value=',total_pv)

share_price = (total_pv - debt)/shares_out
print('share_price=',share_price)

# Problem 1
N = 300000
depreciation = 300000/10
revenue = 200000
cogs = 50000
tax_rate = 0
r = 0.1

cash_flows = [-N] + [revenue-cogs for i in range(10)]
pv_cf = [cash_flows[i]/ (1+r)**i for i in range(len(cash_flows))]
npv = np.array(pv_cf).sum()
print('npv=', npv)

# Problem 2
# A
salvage_value = +5
cost_savings = [1.5 for i in range(10)]
revenue_loss = [-1 * 1.1**i for i in range(10)]
r = 12/100
cash_flows = np.array([salvage_value] + cost_savings) + np.array([0] + revenue_loss)
pv_cf = [cash_flows[i]/ (1+r)**i for i in range(len(cash_flows))]
npv = np.array(pv_cf).sum()
print('npv=', npv)

# B
salvage_value = +8
cost_savings = [0 for i in range(10)]
revenue_loss = [0 for i in range(5)] + [-3 for i in range(5)]
r = 12/100
cash_flows = np.array([salvage_value] + cost_savings) + np.array([0] + revenue_loss)
pv_cf = [cash_flows[i]/ (1+r)**i for i in range(len(cash_flows))]
npv = np.array(pv_cf).sum()
print('npv=', npv)


# Problem 4

# opportunity A
N = 100
cash_flows_a = [0 for i in range(2)] + [100 for i in range(10)]
pos = 0.5
expected_anual_cash_flows_a = np.append(np.array([-N]), ( pos * np.array(cash_flows_a)))
print('expected_anual_cash_flows_a', expected_anual_cash_flows_a)
r_a = 0.12
pv_cf_A = [expected_anual_cash_flows_a[i]/ (1+r_a)**i for i in range(len(expected_anual_cash_flows_a))]
npv_A = np.array(pv_cf_A).sum()
print('npv A=', npv_A)

# opportunity B
N = 200
cash_flows_b =   [0 for i in range(10)] + [2000 for i in range(10)]
pos = 0.05
expected_anual_cash_flows_b = np.append(np.array([-N]), ( pos * np.array(cash_flows_b)))
print('expected_anual_cash_flows_b', expected_anual_cash_flows_b)
r_b = 0.2
pv_cf_B = [expected_anual_cash_flows_b[i]/ (1+r_b)**i for i in range(len(expected_anual_cash_flows_b))]
npv_B = np.array(pv_cf_B).sum()
print('npv A=', npv_B)


# -------------------------------------------------------------------------------------------------------------------
# Exercise: Discount Bonds

N = 1000
r = 0.03
pv = 1000/1.03**2
price = pv/1000
print(price)

# Exercise: Spot Rates and Forward Rates
f_1_3 = ((1+0.036)**3/(1+0.029))**(1/2) - 1
print('forward rate in 1 year for 2 years', f_1_3 * 100, '%')

# -------------------------------------------------------------------------------------------------------------------
# Zero-Coupon Bonds
N = 100
p = 91.27
T = 5
# p = N/(1+r)**T

def calculate_spot_rate(N, p, T):
    r = (N/p)**(1/T) - 1
    print('spot rate r for', T, 'years:', r * 100, '%')
    return r

N = 100
for e in [(1,99.81),(2,98.98),(5,91.27),(10,73.83),(30,29.38)]:
    # print(e[0], e[1])
    calculate_spot_rate(N=N, p=e[1], T=e[0])


# Coupon Bonds
cf = [50, 50, 1050]
term_structure = [(1,5.04), (2,5.53), (3,5.9)]
p = 0
for i in range(len(cf)):
    p += cf[i] * (1 + term_structure[i][1]/100)**(-term_structure[i][0])
print('Price of coupon bond:', p)

y = np.irr(np.array([-p] + cf))
print('Yield of coupon bond:', y * 100, '%')

# Yield Spread, Risk Premium, and Default Premium

#1) calculate yields for treasury and corporate bond
N = 1000
p=463.19
y_treasury = calculate_spot_rate(N=N, p=p, T=10)
print('Yield of treasury bond:', y_treasury * 100, '%')
N = 1000
p=321.97
y_corporate = calculate_spot_rate(N=N, p=p, T=10)
print('Yield of corporate bond:', y_corporate * 100, '%')
# 2) calculate yield spread
print('Yield spread:', (y_corporate - y_treasury) * 100, '%')

# 3) calculate yield based on expected payoff
N=762.22
p=321.97
y_corporate_expected = calculate_spot_rate(N=N, p=p, T=10)
print('Expected yield of corporate bond:', y_corporate_expected * 100, '%')
#4) Calcuate default premium
print('Default premium of corporate bond:', (y_corporate - y_corporate_expected) * 100, '%')
#5) calculate risk premium
print('Default premium of corporate bond:', (y_corporate_expected - y_treasury) * 100, '%')

# 4) Present Value of Growth Opportunities
RoE = 12/100
b = 50/100 #plow back ratio
g = b * RoE
print(' future growth rate ( g ) under the new program:', g * 100, '%')

# a) Stock price before announcement
d = 1
r = 0.1
p_0 = c/r
print('Stock price before announcement=', p_0)
# b) Stock price after announcement
d = 1 * (1-b)
r = 0.1
p_1 = c/(r-g)
print('Stock price after announcement=', p_1)
# c) Change in stock price
print('Change in stock price:', p_1-p_0)

# Problem 1
# a) calculate spot rates
r = [(1,98.8), (2,97.5), (3,95.6), (4,93.1)]
N=100
spot_rates = [0] + [calculate_spot_rate(N=N, p= e[1], T=e[0]) for e in r]
cf = [-200, -200, 100, 150, 200]
pv = [cf[i]/(1+spot_rates[i])**i for i in range(len(cf))]
print('Total PV:', np.array(pv).sum())

# Problem 2
r_0_3 = 0.03
r_0_2 = 0.02
f_2_1 = (1+r_0_3)**3/(1+r_0_2)**2 - 1
print('f_2_1=', f_2_1 * 100, '%')

# alternative
N_0 = 100/1.02**2 # invest in T0 for 2 years
N_1 = N_0 * 1.03**3 # owe in T=3
f_2_1 = N_1/100 - 1 # divide by 100 (=payback of initial investment in T=0)
print('f_2_1=', f_2_1 * 100, '%')

# Problem 3:
# earnings to interest expense ratios (EBITDA/interest expense coverage ratio)
EBITDA = 23
l_r = [0.04, 0.049, 0.056, 0.07]
for r in l_r:
    interest_expense = 32 * r
    coverage_ratio = EBITDA/interest_expense
    print(coverage_ratio)

# Problem 4:
RoE =15/100
b = 60/100
g = b * RoE
p_0 = 40
earnings = 1
dividend = (1-b) * 1

r = dividend/p_0 + g
print('discount rate=', r * 100, '%')
p_0 = dividend/(r-g)
print('stock price=', p_0)

# calculate stock price w/o growth
b=0
g = b * RoE
earnings = 1
dividend = (1-b) * 1
p_no_growth = dividend/(r-g)
print('stock price w/o growth=', p_no_growth)
print('present value of its growth opportunities (PVGO):', p_0-p_no_growth)


# Problem 5:
dividend = 4
g_init = 0.08
g = 0.03
r = 0.115

# a)
pv_period_1 = dividend/(r-g_init)  - dividend * (1+g_init)**3/(r-g_init) * (1+r)**-3
# dividend/(1+r) + dividend * (1+g_init)/(1+r)**2 + dividend * (1+g_init)**2/(1+r)**3
pv_terminal_1 = dividend * (1+g_init)**2 * (1+g) /(r-g) * (1+r)**-3
print('stock price=', pv_period_1 + pv_terminal_1)
p_0 = pv_period_1 + pv_terminal_1
# b)
pv_period_2 = dividend * (1+g_init)/(1+r) + dividend * (1+g_init)**2/(1+r)**2
pv_terminal_2 = dividend * (1+g_init)**2 * (1+g) /(r-g) * (1+r)**-2
p_1 = pv_period_2 + pv_terminal_2
print('stock price=', p_1)

# The holding period return (HPR)
HPR = (p_1 + dividend - p_0)/p_0
print('The holding period return (HPR):', HPR *100, '%')


#  ---------------------------------------------------------------------------------------------------------------------
# Exercise: Returns
r = np.array([0.1,0.2,0.25,0.17,0.12])

r_net = np.prod(1+r) - 1
print('r_net=', r_net)
r_ann = (1+r_net)**(1/len(r)) - 1
print('r_ann=', r_ann)

# Exercise: Sharpe Ratio
sr = (0.12-0.034) / 0.32
print('Sharpe ratio=', sr)

# Exercise: Mean-Variance Analysis
r_a = 0.15
sigma_a = 0.2
r_b = 0.11
sigma_b = 0.16
rho = 0.4
r_target = 0.12
w   = (r_target - r_b)/ (r_a - r_b)
print('w_a=', w)
print('w_b=', 1-w)
w * r_a + (1-w) * r_b

sigma_p = np.sqrt(w**2 * sigma_a**2 + (1-w)**2 * sigma_b**2 + 2 * w * (1-w) * rho * sigma_a * sigma_b)
print('sigma_p=', sigma_p)


# Portfolio Weights
num_shares = np.array([200,1000,750])
prices = np.array([50,60,40])
values = num_shares * prices
portfolio_value = values.sum()
weights = values/portfolio_value
print('weights:', weights * 100)

# Three Risky Assets
r = np.array([0.1,0.12,0.08])
s = np.array([0.2,0.3,0.25])
corr = np.array([[1,0.2, 0.1], [0.2,1,0.4], [0.1,0.4,1]])
weights = np.array([1/3 for i in range(3)])

expected_return = (r* weights).sum()*100
print('expected return:', expected_return)

variance = 0
for i in range(3):
    for j in range(3):
        variance += weights[i] * weights[j] * corr[i,j] * s[i] * s[j]
standard_deviation = np.sqrt(variance)
print('standard_deviation:', standard_deviation * 100)

# Megafund Example
N = 150
r = np.array([0.1 for i in range(N)])
weights = np.array([1/N for i in range(N)])
sd = np.array([4 for i in range(N)])

expected_return = (r*weights).sum()
print('expected return:', expected_return)

standard_deviation = np.sqrt((weights**2 * sd**2).sum()) #assume ZERO correlation
print('standard_deviation:', standard_deviation * 100)

# CAPM Example
sd = np.array([0.2,0.32])
corr_m = np.array([0.4,0.6])
r_m = 0.09
sd_m = 0.16
rf = 0.03

R = rf + (r_m - rf)  * sd * corr_m/sd_m
weights = [0.5,0.5]
R_P = (weights * R).sum()
print('expected return R_p:', R_P *100)

# Problem 1
rf = 0.02
r_m = 0.08
sd_m = 0.15
R_P = 0.11
sd_P = 0.45

beta_P = (R_P - rf)/(r_m-rf)
print('beta_p:', beta_P)

corr_m = beta_P * sd_m/sd_P
print('Correlation with market return:', corr_m)

# Problem 2
w_A = w_B = 0.4
w_C = 1 - w_A - w_B
beta_A = 0.8
beta_B = 1.4
beta = 1
beta_C = (beta - w_A * beta_A - w_B * beta_B) / w_C
print('beta_C:', beta_C)

rf = 0.06
market_risk_premium = 0.06
R_C =  rf + market_risk_premium * beta_C
print('R_C (Cs opportunity cost of capital):', R_C*100)

# Problem 3


def calc_sd_for_megafund_example(N, corr=0.5):

    weights = np.array([1/N for i in range(N)])

    sd = np.array([4 for i in range(N)])

    variance = (weights**2 * sd**2).sum()
    for i in range(N):
        for j in range(N):
            if i != j:
                variance += weights[i] * weights[j] * corr * sd[i] * sd[j]

    standard_deviation = np.sqrt(variance)

    print(N, 'projects with correlation coefficient =', corr, ':', standard_deviation * 100)

calc_sd_for_megafund_example(N=10, corr=0.5)
calc_sd_for_megafund_example(N=100, corr=0.5)
calc_sd_for_megafund_example(N=1000, corr=0.5)

calc_sd_for_megafund_example(N=10, corr=0)
calc_sd_for_megafund_example(N=100, corr=0)
# calc_sd_for_megafund_example(N=150, corr=0)
calc_sd_for_megafund_example(N=1000, corr=0)

# Problem 4
p = 0.3
R_A = p * 0.5 + (1-p) * (-0.12)
R_B = p * (-0.25) + (1-p) * (0.05)
print('R_A:', R_A*100)
print('R_B:', R_B*100)

VARIANCE_A = p * 0.5**2 + (1-p)*(-0.12)**2 - R_A**2
SD_A = np.sqrt(VARIANCE_A)
print('SD_A:', SD_A * 100)

VARIANCE_B = p * (-0.25)**2 + (1-p)*(0.05)**2 - R_B**2
SD_B = np.sqrt(VARIANCE_B)
print('SD_B:', SD_B * 100)

cov_A_B = p * 0.5*(-0.25) + (1-p) * (-0.12)*(0.05) - R_A * R_B
print('cov_A_B:', cov_A_B)
corr_A_B = cov_A_B/(SD_A * SD_B)
print('corr_A_B:', corr_A_B)

R_P = 0.5*R_A + 0.5*R_B
print('R_P:', R_P*100)

VARIANCE_P = 0.5**2 * SD_A**2 + 0.5**2 * SD_B**2 + 2 * 0.5*0.5 * corr_A_B * SD_A * SD_B
SD_P = np.sqrt(VARIANCE_P)
print('SD_P', SD_P * 100)

# ----------------------------------------------------------------------------------------------------------------------
# Exercise: Valuation of Options
import numpy as np
p = 0.5
u = 1.5
d = 0.5
K = 100
r = 0.04
T = 3
U = 750
D = 250
p_u = ((1+r)**3 - d)/(u-d)
p_d =  (u -(1+r)**3)/(u-d)
option_price = (p_u * (U-K) + p_d * (D-K)) * 1/(1+r)**3
print('option_price:', option_price)

p = 0.6
option_price = p * option_price
print('option_price:', option_price)
#print(df[df.isnull().any(axis=1)].head(20).to_string())

# Exercise: Decision Trees
550/1.12**3*0.6

# Timing Option Example
r = 0.1
c_u = 300
c_d = 100

npv_u = c_u/r
print('NPV in upside scenario:', npv_u)
npv_d = c_d/r
print('NPV in downside scenario:', npv_d)

rNPV_1 = 200 + 0.5 * (c_u/0.1) + 0.5 *(c_d/0.1) - 1500
print('NPV in scenario 1:', rNPV_1)

rNPV_2 = 0.5 * ((c_u/0.1)  - 1650/(1+r))
print('NPV in scenario 2:', rNPV_2)

# Pharmaceutical R&D Example 1
node_2 = 150/1.2**3 * 0.7 - 50
print('node_2:', node_2)
node_1 = node_2/1.2**2 * 0.6 - 5
print('node_1:', node_1)

# Pharmaceutical R&D Example 2
node_2_0 = 350/1.2**3 * 0.7  -50
print('node_2_0:', node_2_0)
node_2_1 = 50/1.2**3 * 0.7  - 50
print('node_2_1:', node_2_1)

# only pursue node_2_0
node_1 = node_2_0/1.2**2 * 0.2 - 5
print('node_1:', node_1)

# ----------------------------------------------------------------------------------------------------------------------
# Week 5
# Overview
# Problem Set Finance due Aug 18, 2020 14:50 CEST
#
# AZ Biotech would receive an initial licensing fee, milestone payments as AZ1024 progressed through the approval
# process, and a royalty on all future sales.
# approval process would take 4 to 7 years in total

# PHASE 1
t_phase_1 = 2
cost_phase_1 = 20
p_phase_1 = 0.7
upfront_phase_1 = -2.5 #paid to AZ in T = 0

# PHASE 2
upfront_phase_2 =  -5 #milestone_phase_1 paid to AZ in T = 2, if successful
t_phase_2 = 2
p_phase_2_strong = 0.05
p_phase_2_moderate = 0.15
p_phase_2_weak = 0.20
p_phase_2_failure = 1 - p_phase_2_strong - p_phase_2_moderate - p_phase_2_weak
cost_phase_2 = 60

# PHASE 3

# Scenario 1: Weak efficiency
t_phase_3_1 = 3
cost_phase_3_1 = 300
p_phase_3_1 = 0.5
upfront_phase_3_1 = -10
milestone_pase_3_1 = -20
fv_phase_3_1 =  1000

# Scenario 2: Moderate efficiency
t_phase_3_2 = 3
cost_phase_3_2 = 200
p_phase_3_2 = 0.8
upfront_phase_3_2 = -20
milestone_pase_3_2 = -20
fv_phase_3_2 =  2000

# Scenario 3: Strong efficiency
t_phase_3_3 = 0
cost_phase_3_3 = 0
p_phase_3_3 = 1
upfront_phase_3_3 = 0
milestone_pase_3_3 = -80
fv_phase_3_3 =  4000

# Problem 1
p_launch_year_4 = p_phase_1 * p_phase_2_strong * p_phase_3_3
print('Probability of launch in year 4:', p_launch_year_4 * 100)

p_launch_year_7_moderate = p_phase_1 * p_phase_2_moderate * p_phase_3_2
print('Probability of launch in year 7, with a commercialization value of $2 billion:', p_launch_year_7_moderate * 100)

p_launch_year_7_weak = p_phase_1 * p_phase_2_weak * p_phase_3_1
print('Probability of launch in year 7, with a commercialization value of $1 billion:', p_launch_year_7_weak * 100)

p_failure = 1 - p_launch_year_4 - p_launch_year_7_weak - p_launch_year_7_moderate
print('Failure to reach market:', p_failure * 100)

# ----------------------------------------------------------------------------------------------------------------------
# Problem 2
# What is AZ1024's rNPV from ABC Pharmaceutical's perspective?
r_abc_0_2 = 0.2
r_abc_2_4 = 0.15
r_abc_4_7 = 0.1

def calculate_node_3(fv, r, T, upfront, milestone, p, cost):
    node_3 = (fv/(1+r)**T  + milestone/(1+r)**T) * p - cost + upfront
    print('Value in node 3:', node_3)
    return node_3

node_3_3 = calculate_node_3(fv_phase_3_3, r_abc_4_7, t_phase_3_3, upfront_phase_3_3,
                            milestone_pase_3_3, p_phase_3_3, cost_phase_3_3)
node_3_2 = calculate_node_3(fv_phase_3_2, r_abc_4_7, t_phase_3_2, upfront_phase_3_2,
                            milestone_pase_3_2, p_phase_3_2, cost_phase_3_2)
node_3_1 = calculate_node_3(fv_phase_3_1, r_abc_4_7, t_phase_3_1, upfront_phase_3_1,
                            milestone_pase_3_1, p_phase_3_1, cost_phase_3_1)

#calculate value of node 2
node_2 = (p_phase_2_strong * node_3_3 + p_phase_2_moderate * node_3_2 + p_phase_2_weak * node_3_1)/ (1+r_abc_2_4)**t_phase_2 \
         - cost_phase_2 + upfront_phase_2

# calculate value of node 1
node_1 = p_phase_1 * node_2/(1+r_abc_0_2)**t_phase_1 - cost_phase_1 + upfront_phase_1

# ----------------------------------------------------------------------------------------------------------------------
# Problem 3
# What is the rNPV of the licensing agreement from AZ Biotech's perspective?
import numpy as np
royality = 0.05
r_az_0_2 = 0.2
r_az_2_4 = 0.15
r_az_4_7 = 0.1

def calculate_node_3(fv, r, T, upfront, milestone, p, royality):
    node_3 = (fv/(1-royality) * royality  + np.abs(milestone)) * p /(1+r)**T \
             + np.abs(upfront)
    print('ROYALITY:', fv/(1-royality) * royality)
    print('Value in node 3:', node_3)
    return node_3

node_3_3 = calculate_node_3(fv_phase_3_3, r_az_4_7, t_phase_3_3, upfront_phase_3_3,
                            milestone_pase_3_3, p_phase_3_3, royality)
node_3_2 = calculate_node_3(fv_phase_3_2, r_az_4_7, t_phase_3_2, upfront_phase_3_2,
                            milestone_pase_3_2, p_phase_3_2, royality)
node_3_1 = calculate_node_3(fv_phase_3_1, r_az_4_7, t_phase_3_1, upfront_phase_3_1,
                            milestone_pase_3_1, p_phase_3_1, royality)

node_2 = (node_3_3 * p_phase_2_strong + node_3_2 * p_phase_2_moderate + node_3_1 * p_phase_2_weak)  \
         * 1/(1+r_az_2_4)**t_phase_2         \
         + np.abs(upfront_phase_2)

node_1 = p_phase_1 * node_2/(1+r_az_0_2)**t_phase_1 + np.abs(upfront_phase_1)

#  ---------------------------------------------------------------------------------------------------------------------
# Problem 4
# For this problem assume a Phase 3 trial under the weak efficacy scenario is projected to cost $400 million instead
# of $300 million. What is AZ1024's rNPV from ABC Pharmaceutical's perspective?
r_abc_0_2 = 0.2
r_abc_2_4 = 0.15
r_abc_4_7 = 0.1

def calculate_node_3(fv, r, T, upfront, milestone, p, cost):
    node_3 = (fv/(1+r)**T  + milestone/(1+r)**T) * p - cost + upfront
    print('Value in node 3:', node_3)
    return node_3

node_3_3 = calculate_node_3(fv_phase_3_3, r_abc_4_7, t_phase_3_3, upfront_phase_3_3,
                            milestone_pase_3_3, p_phase_3_3, cost_phase_3_3)
node_3_2 = calculate_node_3(fv_phase_3_2, r_abc_4_7, t_phase_3_2, upfront_phase_3_2,
                            milestone_pase_3_2, p_phase_3_2, cost_phase_3_2)

cost_phase_3_1 = 400 # assume a Phase 3 trial under the weak efficacy scenario is projected to cost $400 million
node_3_1 = calculate_node_3(fv_phase_3_1, r_abc_4_7, t_phase_3_1, upfront_phase_3_1,
                            milestone_pase_3_1, p_phase_3_1, cost_phase_3_1)

# We would NOT commercialize under this scenario!


#calculate value of node 2
node_2 = (p_phase_2_strong * node_3_3 * (node_3_3>0)
          + p_phase_2_moderate * node_3_2  * (node_3_2>0) +
          p_phase_2_weak * node_3_1 * (node_3_1>0))/ (1+r_abc_2_4)**t_phase_2 \
         - cost_phase_2 + upfront_phase_2

# calculate value of node 1
node_1 = p_phase_1 * node_2/(1+r_abc_0_2)**t_phase_1 - cost_phase_1 + upfront_phase_1


#  ---------------------------------------------------------------------------------------------------------------------
# Week 6
import numpy as np
from scipy.stats import norm

# Problem 1
alpha = 0.025
beta = 0.1
power = 1 -beta
sigma = sigma_t = sigma_x = 25
mu = 5
kappa = mu/sigma
print('kappa = ', kappa)

z_alpha_half = norm.ppf(q=1-alpha)
print('z_alpha_half = ', z_alpha_half)

z_beta  = norm.ppf(q=beta)
print('z_beta = ', z_beta)

n = 2 * ((z_alpha_half - z_beta)/kappa)**2
print('n =', n)


# Problem 2
mu = 10
kappa = mu/sigma
print('kappa = ', kappa)
n = 2 * ((z_alpha_half - z_beta)/kappa)**2
print('n =', n)

#Problem 3 - Overconfidence
mu = 5
kappa = mu/sigma
z_beta_hat = z_alpha_half - kappa/ np.sqrt(2/n)
beta_hat = norm.cdf(x=z_beta_hat)
print('beta_hat = ', beta_hat)
print('power = ', 1-beta_hat)

# ----------------------------------------------------------------------------------------------------------------------
# Week 7
import numpy as np
# Problem 1
equity_investment = 10
equity_interest = 0.4
pre_money_valuation = equity_investment/equity_interest - equity_investment
print('pre_money_valuation =', pre_money_valuation)

# Problem 2
#  build a simple financial model to estimate the value of BLV's offe
pop = 5 * 10**6
cost_of_treatment = 1000
market_share = 0.2
annual_revenue = pop * cost_of_treatment * market_share/ 10**6

T = 13
# No revenue after year 13
r = 0.1
# what would be the present value of revenues at the moment of commercial launch
# --> Use a annuity for 13 years
pv_perpetuity_1 = annual_revenue/r
pv_perpetuity_2 = annual_revenue/r * (1+r)**(-T)
pv_annuity = pv_perpetuity_1 - pv_perpetuity_2
print('PV of revenues = ', pv_annuity)

# Problem 3
COGS = 0.25
SGA = 0.4
profits = annual_revenue *(1 - COGS - SGA)
pv_perpetuity_1 = profits/r
pv_perpetuity_2 = profits/r * (1+r)**(-T)
pv_annuity = pv_perpetuity_1 - pv_perpetuity_2
print('PV of profits = ', pv_annuity)

# Problem 4
r_3 = 0.15
p_3 = 0.7
cf_3 = -150

r_2 = 0.2
p_2 = 0.5
cf_2 = -60

r_1 = 0.3
p_1 = 0.6
cf_1 = -10

pv_T_7 = pv_annuity
pv_T_4 = pv_T_7 * (1+r_3)**-3 * p_3 + cf_3
pv_T_2 = pv_T_4 * (1+r_2)**-2 * p_2 + cf_2
pv_T_0 = pv_T_2 * (1+r_1)**-2 * p_1 + cf_1
print('rNPV =', pv_T_0)

# Problem 5
# Using this financial model, how much of an equity interest would Axon be willing to offer for an investment of
# $10 million? Assume that the equity interest is calculated as a percentage of the total post-money capitalization
# of Axon.
equity_investment = 10
post_money_valuation = pv_T_0 + 10
equity_interest_hat = equity_investment/ post_money_valuation
print('equity_interest_hat =', equity_interest_hat *100, '%')


# Calculating the Variance of an extreme binary payoff
# Assumptions:
investment = 200
T_1 = 10
p = 0.05
# annual_payoff = 2000
# T_2 = 10
pv_payoff = 150/0.1 * (1- 1/(1+0.1)**13) #Unit 4, Slide 25
pv_payoff = 2000/0.1 * (1- 1/(1+0.1)**10)


# Expected return
expected_pv = pv_payoff * p
expected_return  = expected_pv/investment - 1
annualized_expected_return  = (expected_pv/investment)**(1/T_1) - 1
print('annualized_expected_return:', annualized_expected_return)

# Variance
# https://courses.edx.org/courses/course-v1:MITx+15.480x+1T2020/courseware/0733445368ba42dba42163bb6a83e2ca/f543af7bfe2a45e3a83b1f6dc0a57ef8/?child=first
variance_of_return = p * (1-p) * pv_payoff**2/investment**2
sd_of_return = np.sqrt(variance_of_return)

E_a_2_1_plus_R = (1 + annualized_expected_return) ** 2
E_a_1_plus_R_2 = (pv_payoff/investment)**(2/T_1) * (p*(1-p) + p**2)**(1/T_1)
annualized_variance_of_return = E_a_1_plus_R_2 - E_a_2_1_plus_R
#annualized_variance_of_return =  (pv_payoff/investment)**(2/T_1) * (p**(1/T_1) - p**(2/T_1))
annualized_sd = np.sqrt(annualized_variance_of_return)
print('annualized_sd:', annualized_sd)

# ----------------------------------------------------------------------------------------------------------------------
# Exercise: The Role of Financial Engineering & Securitization
import numpy as np
dflt_prob = 0.2
dflt_senior = dflt_prob ** 2
dflt_none = (1-dflt_prob) ** 2
dflt_junior =  1 - dflt_none
print('Price SENIOR tranche = ', (1-dflt_senior) * 1000)
print('Price JUNIOR tranche = ', (1-dflt_junior) * 1000)


# Exercise: Modeling Correlations
import numpy
from scipy.stats import binom
help(binom)
# 1. Assume the probability of success for each project is 10%, and successes are statistically independent.
n = 10
p = 0.1
# calculate probability that no project is successful
P = (1-p)**n
print('probability that NO project is successful:', P)
print('probability that AT LEAST ONE project is successful:', 1 - P)

# 2. If successes are perfectly positively correlated, then what is the probability that at least 1 project is
# successful? (Note: Your answer should be a number in percentage form. Do not enter '%'.)
# NOTE: IF ONE PROJECT FAILS ALL FAIL, if ONE PROJECT SUCCEEDS ALL DO
# P = 10%

# ----------------------------------------------------------------------------------------------------------------------
# Week 8
import numpy as np
# Overview
# Problem Set Finance due Sep 8, 2020 08:37 CEST

# Megafund financing methods for funding early-stage translational research often require billions of dollars in capital
# to diversify idiosyncratic scientific and clinical risk enough to attract private-sector capital. In this problem set
# we apply this financing method to orphan drug development, where development costs, failure rates, and correlations
# are low, and therefore the amount of capital required to de-risk these portfolios is much lower.
#
# Consider a portfolio of 8 preclinical orphan drug compounds each initially acquired and developed using US$25 million
# of capital. Assume this capital is used to first purchase and then develop the compounds, with excess capital not
# currently deployed earning a 0% return in cash.
#
# For simplicity, also assume that compounds are sold once they
# (successfully) complete the preclinical phase. We will perform a statistical analysis to estimate the expected return
# of this investment over the initial preclinical research phase.

# -----------------------------------------------------
# Problem 1
#
# Assuming average annual sales of US$300 million, a 10% cost of capital, a competition-free marketing period of 12 years,
# and profit margin of 25%, estimate the net present value of an orphan drug’s profits over its competition-free lifespan
# at the moment of product launch. Assume the first cash flow occurs 1 year after launch.
# (Note: Your answer should be expressed in units of millions of dollars.)

revenue = 300
margin = 0.25
cf = revenue * margin
r = 0.1
T = 12
pv_annuity = cf/r * (1 - 1/(1+r)**T)
print(' net present value of an orphan drug’s profits over its competition-free lifespan '
      'at the moment of product launch:', pv_annuity)

# -----------------------------------------------------
# Problem 2
# USE pv_annuity from problem 1

def calculate_npv(cost, pos, r, T, profit):
    # estimate the expected value of an orphan drug at the BEGINNING of the following phases.
    # assume clinical trial costs are incurred at the beginning of each phase
    pv = -cost + pos * profit * 1/(1+r)**T
    return pv

# NDA
pos = 0.96
T = 0.8
r = 0.15
cost = 0
profit = pv_annuity

pv = -cost + pos * profit * 1/(1+r)**T
pv = calculate_npv(cost, pos, r, T, profit)
print('NDA PV:', pv)

# PIII
pos = 0.74
T = 2.15
r = 0.25
cost = 43
profit = pv
pv = calculate_npv(cost, pos, r, T, profit)
print('P III PV:', pv)

# P II
pos = 0.53
T = 2.09
r = 0.3
cost = 8
profit = pv
pv = calculate_npv(cost, pos, r, T, profit)
print('P II PV:', pv)

# P I
pos = 0.84
T = 1.66
r = 0.3
cost = 5
profit = pv
pv = calculate_npv(cost, pos, r, T, profit)
print('P I PV:', pv)


# PE
pos = 0.69
T = 1
r = 0.3
cost = 5
profit = pv
pv = calculate_npv(cost, pos, r, T, profit)
print('PRE PV:', pv)

# -----------------------------------------------------
# Problem 3
# At the end of the preclinical research phase, what is the expected value and standard deviation of the return
# on the US$25 million of capital invested in a single preclinical orphan drug compound.
# Assume that capital held in cash earns no interest.
capital = 25
pv # cost for acquiring drug before preclinical
pv_success = capital - cost - pv + profit
pv_fail = capital - cost - pv

expected_return = (pv_success * pos + pv_fail * (1-pos))/capital - 1
print('expected_return:', expected_return * 100, '%')

ret_success = pv_success/capital - 1
ret_fail = pv_fail/capital - 1

variance_of_return = pos * (ret_success - expected_return)**2 + (1-pos) * (ret_fail - expected_return)**2

standard_deviation = np.sqrt(variance_of_return)
print('standard deviation:', standard_deviation * 100, '%.')

# -----------------------------------------------------
# Problem 4
# Assume the success of the preclincal orphan drug compounds within the portfolio are statistically independent, and
# therefore have a fixed correlation of 0%. What is the expected value and standard deviation of the portfolio's return?
# (Note: Your answer should be a number in percentage form. Do not enter '%'.)

expected_return_port = expected_return # assuming expected return is the same for all orphan drugs
standard_deviation_port = np.sqrt(standard_deviation**2 * 1/8**2 * 8)

# # -----------------------------------------------------
# # Problem 5
# Assume that 40% of the total capital required to form the orphan drug portfolio is financed by selling fixed-income
# securities that mature at the end of the preclinical phase, and the residual capital is in the form of equity.
# Furthermore, assume that the yield-to-maturity on these fixed-income securities is 5% per year,
# and their coupon rate is 0% (i.e., they have no coupon payments).
# What is the expected value and standard deviation of the return on equity?
from scipy.stats import binom



n = 8
p = 0.69
s = 0

# calculate the total cost and debt for purchasing the drug portfolio
total_capital = n * capital
total_acq_cost = n * pv
total_trial_cost = n * cost

total_debt = 0.4 * (total_capital)
total_repayment = 1.05 * total_debt
total_equity = total_capital - total_debt

l_p = []
l_ret = []
l_pv = []
l_residual_pv = []
l_roe = []
for i in range(n+1):
    print(i)
    p_scenario = binom(n, p).pmf(i)
    s += p_scenario

    pv_scenario = i* pv_success + (n-i) * pv_fail

    ret_scenario = i/n * ret_success + (n-i)/n * ret_fail



    l_p += [p_scenario]
    l_pv += [pv_scenario]
    l_ret += [ret_scenario]

    l_residual_pv += [pv_scenario - total_repayment]

roe_scenario = [pv/total_equity - 1 for pv in l_residual_pv]

expected_roe = np.sum(np.array(l_p) * np.array(roe_scenario))

std_roe = np.sqrt(np.sum(np.array(l_p) * np.power(np.array(roe_scenario) - expected_roe,2)))

# # ********************************************************************************************************************
# FINAL EXAM
# # ********************************************************************************************************************

# # -----------------------------------------------------
# # Problem 1

net_sales = 1000
r = 0.1 # discount rate

# Calculate PV of actual royalty
actual_royalty_perc = 0.03
T_actual = 9
actual_royalty = actual_royalty_perc * net_sales
npv_annuity = actual_royalty/r # cash_flow/discount_rate
npv_annuity_starting_in_T_years = 1/(1+r)**T_actual * actual_royalty/r
npv_actual_royalty = npv_annuity - npv_annuity_starting_in_T_years
# actual_royalty/r * (1 - 1/(1+r)**T_actual)
print('npv_actual_royalty =', npv_actual_royalty)

# Using the formula
# pv = cf/r * (1 - 1/(1+r)**T)
# for the PV of an annuity with
pv = npv_actual_royalty
T = 3
r = 0.1
# we solve for cf:
cf = r * (pv/(1 - 1/(1+r)**T))
npv_accelerated_royalty = cf
print('npv_accelerated_royalty =', npv_accelerated_royalty)

# # -----------------------------------------------------
# # Problem 2
d1  = 1700
r1 = 0.03

d2 = 1900
r2 = 0.0325

d3 = 600
r3 = 0.035

#  a) What will be Royalty Pharma's interest expense in Year 1 (this upcoming year)?
interest_expense = d1*r1 + d2*r2 + d3*r3
print('interest_expense =', interest_expense)
#  b)  Royalty Pharma finances its acquisitions by an approximately even mixture of debt and equity: $4.2 billion and $4.0 billion.
#      Assume Royalty Pharma operates with a total debt to EBIDTA ratio of 4-to-1.
#      If we use the coverage ratio to estimate the bond rating, approximately what rating would we assign to
#      Royalty Pharma's debt?
total_debt = 4200
ratio_total_debt_ebitda = 4
# We use the relatationship total_debt/ebitda = 4 and the total_debt = 4200 to back out ebitda
ebitda = total_debt/ratio_total_debt_ebitda
print('ebitda =', ebitda)
# Using EBITDA and the interest expense in year 1 we can calulate the interest expense coverage ratio
coverage_ratio = ebitda/interest_expense
print('coverage ratio =', coverage_ratio)

# # -----------------------------------------------------
# # Problem 3

# a) Assume the beta on Royalty Pharma's portfolio of assets is 1, the risk-free rate is 0.5% per year,
# and the market portfolio’s risk premium is 6% per year.
# According to the CAPM, what is Royalty Pharma's expected return?
beta = 1
r_f = 0.5
r_m = 6.5
expected_return = r_f + (r_m - r_f) * beta
print('expected_return =', expected_return)

#  b)   Using your answer to the previous question, and assuming that the expected return on Royalty Pharma's debt is 3%
#       per year, calculate the expected return on Royalty Pharma's equity?
#       Recall that Royalty Pharma finances its acquisitions by an approximatley even mixture of debt and equity:
#       $4.2 billion and $4.0 billion, respectively.
# Hint: How are the expected return on asset, on equity and on debt related? Which one did you compute in Problem 3a?
total_debt = 4200
total_equity = 4000
w_debt = total_debt/(total_debt + total_equity)
w_equity = total_equity/(total_debt + total_equity)
expected_return_debt = 3
# Using the formula for the weighted average cost of capital (WACC)
# expected_return = w_debt * expected_return_debt + w_equity * expected_return_equity
# we back out the expected return on equity
expected_return_equity = 1/w_equity * (expected_return - w_debt * expected_return_debt)
print('expected_return_equity =', expected_return_equity)

# # -----------------------------------------------------
# # Problem 4
# An example of pre-FDA-approval financing is Royalty Pharma's "adaptive financing" for Sunesis Pharmaceuticals
# lead product candidate, Vosaroxin. At the time, Vosaroxin was being evaluated in a Phase-III, randomized, double-blind,
# placebo-controlled trial among patients with first relapsed or refractory acute myeloid leukemia (AML).
#
# Suppose, given a 2.5% significance level threshold for a one-tailed Z-test, the trial was designed to have a
# 90% probability of detecting a 2-month increase in overall survival among patients in the study.
# If the treatment response standard deviation was 6.5 months and there are an equal number of patients in each arm of
# the study, then how many patients would the study require in total?
# Assume that treatment responses are independent and identically distributed given the treatment arm. Therefore,
# by the central limit theorem, the average treatment response in each arm can be estimated by a normal distribution.
import numpy as np
from scipy.stats import norm

# calculate quantile for one-sided test
alpha = 0.05 # for a two-sided test
z_alpha_half = norm.ppf(1-alpha/2)

power = 0.9 # power
beta = 1 - power
# beta = 0.2
z_beta= norm.ppf(beta)

standard_deviation_abs = 6.5
mu = 2
kappa = 2/standard_deviation_abs
# kappa = 0.3

# calculate required sample size n (Week 6, part 2, slide 19)
n = 2 * ((z_alpha_half - z_beta)/ kappa)**2
print('n (number of patients required in each arm) =', n)
print('N (total number of patients required in RCT) =', 2 * n)


# # -----------------------------------------------------
# # Problem 5

# While Sunesis had sufficient capital to fund the original Phase-III design of the trial, the company was seeking an
# additional $25 million to fund a potential expansion of the study based on the results of an interim analysis.
# At that time, an independent data safety monitoring board (DSMB) would decide whether to stop the study early
# for efficacy or futility, continue the study as planned, or implement a one-time increase in sample size with an
# additional 225 patients. By designing the study this way, Sunesis could avoid conducting an unnecessarily large trial
# in certain cases, potentially reducing the overall cost and risk of their study.

# After conducting its due diligence, Royalty Pharma conditionally agreed to pay Sunesis the $25 million to acquire
# a royalty interest on the future net sales of Vosaroxin. However, under the terms of the agreement, Royalty Pharma
# would only invest the $25 million if, following the interim analysis, the study was stopped early for efficacy or if
# the sample-size increase was implemented.
#
# In return, assume Royalty Pharma would get a 3.6% royalty interest on future net sales of the drug if the study was
# stopped early for efficacy, or a 6.75% royalty on future net sales if the sample size was increased.
# Assume these scenarios were estimated to occur with probability 10% and 40%, respectively.
# Furthermore, the probability that the study would be terminated early for futility and abandoned was estimated to be 5%.
#
# If the sample size was increased, Royalty Pharma estimated there was a 10% chance the therapy would show a strong effect,
# a 65% chance that it would show a weak effect, and a 25% chance that it would show no effect and be abandoned.
#
# Finally, if the DSMB decided that the trial should continue as planned, Royalty Pharma would have the option of making
# the $25 million investment upon the un-blinding of the study (i.e., the results were made known) in exchange
# for a 3.6% royalty interest on future net sales. Given this scenario, Royalty Pharma estimated there was a 15% chance
# the therapy would show a strong effect, a 60% chance that it would show a weak effect, and a 25% chance that it would
# show no effect and be abandoned. As such, Royalty Pharma would be able to significantly limit its exposure to the risk
# of an undesirable outcome of the clinical trial and, at the same time, position itself to receive a sizable royalty
# in the event that Vosaroxin was approved.
#
# Vosaroxin was projected to be highly profitable, especially if it the trial was stopped early for efficacy.
# Under this scenario, future net sales were projected to have a present value of $4 billion. If, however, the trial
# required a sample-size increase, then future net sales were projected to have a present value of only $2.5 billion
# under the strong effect scenario, and 0.5 billion under the weak effect scenario.
#
# Finally, if the DSMB decided that the trial should continue as planned, the future net sales would have a present
# value of $3 billion under the strong effect scenario, and $0.5 billion under the weak effect scenario.
#
# Build a decision tree for Royalty Pharma that shows the cash flows and probabilities of each possible scenario.
# Your tree should have 8 outcomes with 3 failures and 5 successes.

# a) What is the probability that the clinical trial fails and the project is abandoned?
# (Note: Your answer should be a number in percentage form. Do not enter '%'.)

p_1 = 0.1

p_continue_as_planned = 0.45
p_2 = p_continue_as_planned * 0.15
p_3 = p_continue_as_planned * 0.6
p_4 = p_continue_as_planned * 0.25 #failure planned

p_increase_n = 0.4
p_5 = p_increase_n * 0.1
p_6 = p_increase_n * 0.65
p_7 = p_increase_n * 0.25 # failure increased sample size

p_8 = 0.05 # outright fail

p_ABANDON = p_4 + p_7 + p_8
print('p_ABANDOM =', p_ABANDON)

# b) What is Vosaroxin's rNPV from Royalty Pharma's perspective? For simplicity, assume the discount rate is 0% so
# the specific timing of the various cash flows can be ignored.
probabilities = np.array([p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8])
cost = 25
cash_flows = np.array([0.036 * 4000 - cost,
              np.max([0.036 * 3000 - cost,0]), #optionality on unblinding - strong efficacy,
              np.max([0.036 * 500 - cost, 0]),  #optionality on unblinding - weak efficacy
              0, #no cost as Royalty Pharma would not invest upon unblinding
              0.0675 * 2500 - cost,
              0.0675 * 500 - cost,
              0 - cost,
              0 #no cost as Royalty Pharma would not invest upon termination of trial
            ])

probabiity_weighted_cash_flows = probabilities * cash_flows

rNPV = probabiity_weighted_cash_flows.sum()
print('rNPV =', rNPV)

# # -----------------------------------------------------
# # Problem 6

# At the end of 2006, Royalty Pharma purchased Cambridge Antibody Technology's (CaT) passive royalty interest in
# Abbott's Humira.
royalty = 0.02688
cost = 0.7
royalty_humira = np.array([3,4.5,5.5,6.5,7.9,9.3,10.7,12.5,14,16.1,18.4]) * royalty
cf = np.concatenate([np.array([-cost]) , royalty_humira])
print('IRR:', np.irr(cf) *100, '%')

# Given the $700 million purchase, and the subsequent royalties, what is the internal rate of return of this deal from
# Royalty Pharma's perspective? Assume all royalties occur at the end of the year so the first payment is received
# exactly 1 year after the $700 million purchase. (Note: Your answer should be a number in percentage form. Do not enter '%'.)


# # -----------------------------------------------------
# # Problem 7
# Suppose Royalty Pharma's portfolio consists of equally-weighted royalty interests in 40 approved and marketed
# biopharmaceutical products. Assume each royalty stream has an annualized expected return of 6.5%,
# and return standard deviation of 20%.
expected_return = 0.065
standard_deviation = 0.20
correlation = 0.4
N = 40

# b) Still assuming that the correlation amongst projects is 10%, what is the return standard deviation of the portfolio.
variance_of_return = standard_deviation**2 * (1/N +  (N-1)/N * correlation)
standard_deviation_of_return = np.sqrt(variance_of_return)
print('standard_deviation_of_return =', standard_deviation_of_return)

# c) If the distribution of portfolio returns is given by a normal distribution, then what is the probability
# that Royalty Pharma's equity holders suffer a loss greater than 10%?
# Assume an approximately even mixture of debt and equity: $4.2 billion and $4.0 billion, respectively.
# In addition, for simplicity, assume the yield on Royalty Pharma's debt is 0%.
total_debt = 4200
total_equity = 4000
w_debt = total_debt/(total_debt+total_equity)
w_equity = total_equity/(total_debt+total_equity)
expected_return_debt = 0
leverage_ratio = total_debt/total_equity
# Using the formula for the weighted average cost of capital (WACC)
# expected_return = w_debt * expected_return_debt + w_equity * expected_return_equity
# we back out the expected return on equity
expected_return_equity = 1/w_equity * (expected_return - w_debt * expected_return_debt)
print('expected_return_equity =', expected_return_equity)
# As the return to debt holders is static, the standard deviation of equity returns is equal to the
# standard deviation of portfolio returns times 1 + leverage ratio. Therefore we can back out the probability of returnds from a
# normal distribution with
mu = expected_return_equity
sigma = standard_deviation_of_return * (1+leverage_ratio)
loss = -0.1
# we need to stanardize the loss to use the standard normal distribution
standardized_loss = (loss-mu)/sigma

p = norm.cdf(x=standardized_loss)
print( 'the probability that Royalty Pharmas equity holders suffer a loss greater than 10%:', p * 100 )