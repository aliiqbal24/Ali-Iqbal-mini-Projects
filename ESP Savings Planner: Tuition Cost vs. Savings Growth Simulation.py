import matplotlib.pyplot as plt
import numpy as np

print('Version 1')
counter = []
for i in range(0, 216):
    counter += [i]

# Constants
initial_deposit = 2000
current_amount = initial_deposit
monthly_contribution = 200
monthy_interest_rate = 6.25
annual_increase_rate = 7

# Saving Calculation - calculates amount of saving for each month
amount = []
for i in range(1,19):
    if i==18:
        month = 11
    else:
        month = 12
    for j in range(month):
        current_amount += current_amount* monthy_interest_rate/1200 + monthly_contribution
    amount.append(current_amount)

# Tuition Calculation -  calculates cost of tuition required for 4 year degree
tuition_rates = [[5550],[6150],[6550]]
current_fees = tuition_rates[:]


for i in range(21):
    for j in range(3):
        current_fees[j].append(current_fees[j][-1]+current_fees[j][-1]*annual_increase_rate/100)

cost_arts = sum(current_fees[0][-4:])
cost_science = sum(current_fees[1][-4:])
cost_engg = sum(current_fees[2][-4:])

# Display the final savings amount and tuition cost
print(f"The savings amount is ${round(amount[-1],2)}")
print(f"The cost of the arts program is ${round(cost_arts,2)}")
print(f"The cost of the science program is ${round(cost_science,2)}")
print(f"The cost of the engg program is ${round(cost_engg,2)}")

# Plotting the graph
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(amount,label="Saving Balance")
ax.plot([cost_engg for i in range(19)],label="Engineering")
ax.plot([cost_science for i in range(19)],label="Science")
ax.plot([cost_arts for i in range(19)],label="Arts")
ax.legend()
ax.set_xlabel("'Number of Years")
ax.set_ylabel("Amount in Dollars') $")
ax.set_title("RESP Savings vs. Predicted Tuition Costs")
ax.set_xticks([i for i in range(19)])
plt.show()

program = int(input("Enter a program 1.Arts, 2.Science, 3.Engineering :"))

if program==1:
    goal = cost_arts
    if goal<=amount[-1]:
        print("Congratulations!!! You have saved enough for the arts program")
    else:
        print("Unfortunately!!! You do not have enough saved for the arts program")
elif program==2:
    goal = cost_science
    if goal<=amount[-1]:
        print("Congratulations!!! You have saved enough for the science program")
    else:
        print("Unfortunately!!! You do not have enough saved for the science program")
else:
    goal  = cost_engg
    if goal<=amount[-1]:
        print("Congratulations!!! You have saved enough for the engineering program")
    else:
        print("Unfortunately!!! You do not have enough saved for the engineering program")

monthly_contribution = 1
# implemetning while loop to get optimal answer
while True:
    current_amount = 2000
    for i in range(1,19):
        if i==18:
            month = 11
        else:
            month = 12
        for j in range(month):
            current_amount += current_amount* monthy_interest_rate/1200 + monthly_contribution
    if current_amount>=goal:
        break
    monthly_contribution+=1

print(f"The optimal monthly contribution is ${monthly_contribution}")

