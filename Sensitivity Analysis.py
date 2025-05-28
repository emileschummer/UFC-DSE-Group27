import pandas as pd
import random 
import numpy as np
import matplotlib.pyplot as plt


# Create the DataFrame
data = {
    "Criteria": ["Endurance", "Complexity", "Quality", "Cost", "Safety", "Noise", "Sustainability"],
    "Weight (%)": [0.10, 0.15, 0.15, 0.20, 0.10, 0.10, 0.20],
    "Helicopter": [0.10, 0.22, 0.75, 0.30, 0.34, 0.10, 0.22],
    "Quadcopter": [0.10, 1, 1, 0.65, 0.70, 0.75, 0.65],
    "Osprey": [0.50, 0.38, 0.52, 0.68, 0.75, 1, 0.61],
    "Yangda": [0.75, 0.75, 0.65, 0.68, 0.90, 1, 0.80],
}

df = pd.DataFrame(data).set_index("Criteria")
print("Initial table:")
print(df)



def Compare(): #2 category method
        #resetting the table each time
    data = {
        "Criteria": ["Endurance", "Complexity", "Quality", "Cost", "Safety", "Noise", "Sustainability"],
        "Weight (%)": [0.10, 0.15, 0.15, 0.20, 0.10, 0.10, 0.20],
        "Helicopter": [0.10, 0.22, 0.75, 0.30, 0.34, 0.10, 0.22],
        "Quadcopter": [0.10, 1, 1, 0.65, 0.70, 0.75, 0.65],
        "Osprey": [0.50, 0.38, 0.52, 0.68, 0.75, 1, 0.61],
        "Yangda": [0.75, 0.75, 0.65, 0.68, 0.90, 1, 0.80],
    }

    df = pd.DataFrame(data)
    df.set_index("Criteria", inplace=True)

    # print("\n Original Table:")
    # print(df)

    #Seperating
    Pre_weights = df["Weight (%)"].copy()
    Heli = df["Helicopter"].copy()
    Quad = df["Quadcopter"].copy()
    Tiltrotor = df["Osprey"].copy()
    Yangda = df["Yangda"].copy()


    # Compute old weighted total score for verification/validation
    PRE_Heli_total = (Heli*Pre_weights).sum()
    PRE_Quad_total = (Quad * Pre_weights).sum()
    PRE_Tilt_total = (Tiltrotor*Pre_weights).sum()
    PRE_Yangda_total = (Yangda*Pre_weights).sum()
    PRE_Totals = [PRE_Heli_total,PRE_Quad_total,PRE_Tilt_total,PRE_Yangda_total]

    # print("\n The pre Totals are:")
    # print(PRE_Quad_total,PRE_Heli_total,PRE_Tilt_total,PRE_Yangda_total)


    # Randomly pick two different row Categories
    Row1, Row2 = random.sample(range(len(df)), 2)

    # Get the actual row labels 
    Cat1 = df.index[Row1]
    Cat2 = df.index[Row2]

    # Choose a random amount to vary
    Amount = random.choice([round(i * 0.01, 2) for i in range(1, 11)])
    #Amount = round(random.uniform(0.01, 0.1), 2) - OLD CODE, BIAS ON EDGES FROM ROUNDING


    #print(f"\nChanging weights: +{Amount:.2f} to '{Cat1}', -{Amount:.2f} from '{Cat2}'")

    # Modify the 2 "Weight (%)" values
    df.loc[Cat1, "Weight (%)"] += Amount
    df.loc[Cat2, "Weight (%)"] -= Amount

    # print("\nNew table")
    # print(df)


    # Compute new weighted total score 
    Post_weights = df["Weight (%)"]
    POST_Heli_total = (Heli*Post_weights).sum()
    POST_Quad_total = (Quad *Post_weights ).sum()
    POST_Tilt_total = (Tiltrotor*Post_weights).sum()
    POST_Yangda_total = (Yangda*Post_weights).sum()
    POST_Totals = [POST_Heli_total,POST_Quad_total,POST_Tilt_total,POST_Yangda_total]


    # print("\n The new post weights are:")
    # print(POST_Quad_total,POST_Heli_total,POST_Tilt_total,POST_Yangda_total)

    # print("\nWeight COmparison:")
    # print(Pre_weights, Post_weights)

    #print("\n The sum of the weights is:",sum(df["Weight (%)"]))
    print(df)
    return POST_Totals, Amount, Row1, Row2



def Compare_Equal():#proportional decrease method
    #resetting the table
    data = {
        "Criteria": ["Endurance", "Complexity", "Quality", "Cost", "Safety", "Noise", "Sustainability"],
        "Weight (%)": [0.10, 0.15, 0.15, 0.20, 0.10, 0.10, 0.20],
        "Helicopter": [0.10, 0.22, 0.65, 0.30, 0.34, 0.10, 0.22],
        "Quadcopter": [0.10, 1, 1, 0.65, 0.70, 0.75, 0.37],
        "Osprey": [0.50, 0.38, 0.68, 0.83, 0.75, 1, 0.38],
        "Yangda": [0.75, 0.75, 0.68, 1, 0.90, 1, 0.58],
    }

    df = pd.DataFrame(data)
    df.set_index("Criteria", inplace=True)


    #Seperating
    Pre_weights = df["Weight (%)"].copy()
    Heli = df["Helicopter"].copy()
    Quad = df["Quadcopter"].copy()
    Tiltrotor = df["Osprey"].copy()
    Yangda = df["Yangda"].copy()


    # Compute old weighted total score for verification/validation
    PRE_Heli_total = (Heli*Pre_weights).sum()
    PRE_Quad_total = (Quad * Pre_weights).sum()
    PRE_Tilt_total = (Tiltrotor*Pre_weights).sum()
    PRE_Yangda_total = (Yangda*Pre_weights).sum()
    PRE_Totals = [PRE_Heli_total,PRE_Quad_total,PRE_Tilt_total,PRE_Yangda_total]


    # Setting Up
    Amount = random.choice([round(i * 0.01, 2) for i in range(1, 11)])
    Row = random.sample(range(len(df)), 1)[0]

    #increasing the chosen one 
    Cat_Main = df.index[Row]
    df.loc[Cat_Main, "Weight (%)"] += Amount

    Ratios = [0.1, 0.15, 0.15, 0.2, 0.1, 0.1, 0.2]
    sum_others = 1 - Ratios[Row]

    # Decrease other categories proportionally
    for i in range(len(df)):
        if i != Row:
            Cat_Other = df.index[i]
            decrease = Amount * (Ratios[i] / sum_others)
            df.loc[Cat_Other, "Weight (%)"] -= decrease



    # Compute weighted total score 
    Post_weights = df["Weight (%)"]
    POST_Heli_total = (Heli*Post_weights).sum()
    POST_Quad_total = (Quad *Post_weights ).sum()
    POST_Tilt_total = (Tiltrotor*Post_weights).sum()
    POST_Yangda_total = (Yangda*Post_weights).sum()
    POST_Totals = [POST_Heli_total,POST_Quad_total,POST_Tilt_total,POST_Yangda_total]


    print(df)
    return POST_Totals, Amount, Row





#MAIN - I guess
Runs = 2 #Recommend 10k
Equal = True  #Change for 2 category or equal Method
if Equal:
    print("\nEqual Variation method used")
else:
    print("\n2 Category method used")


Amount_Array = []
Row_Array = []
Difference_Winnings = []
Wins = [0,0,0,0]

for i in range(Runs):

    if Equal:
        Post, Amount, Row = Compare_Equal()
        Amount_Array.append(Amount)
        Row_Array.append(Row)
    else:
        Post, Amount, Row1, Row2 = Compare()
        Amount_Array.append(Amount)
        Row_Array.append(Row1)
        Row_Array.append(Row2)



    max_index = int(Post.index(max(Post)))
    Wins[max_index] = Wins[max_index] +1 


    # Sort in descending order and take the top two for difference 
    top_two = sorted(Post, reverse=True)[:2]
    difference = top_two[0] - top_two[1]
    Difference_Winnings.append(difference)



print("-----------------------------------------")
print(Wins)
print("-----------------------------------------")


#Plotting for bias
Vals_Amounts, Counts_Amount = np.unique(Amount_Array, return_counts=True)

plt.bar(Vals_Amounts, Counts_Amount, width=0.005)
plt.xlabel('Weighting change ')
plt.ylabel('Frequency of Occurance')
plt.title('Distribution of Random Changed Weight Values (0.01 to 0.1)')
plt.grid(axis='y')
plt.show()



Rows_Vals, counts_Rows = np.unique(Row_Array, return_counts=True)

plt.bar(Rows_Vals, counts_Rows)
plt.xticks(Rows_Vals) 
plt.xlabel('Categories Changed')
plt.ylabel('Frequency of Occurance')
plt.title('Distribution of Changed Weight Categories')
plt.grid(axis='y')
plt.show()


#Plotting the data we want for the report
Vals_Dif, Counts_Dif = np.unique(Difference_Winnings, return_counts=True)
#Counts_Dif = Counts_Dif/Runs
plt.bar(Vals_Dif, Counts_Dif, width=0.005)
plt.xlabel('Difference Value')
plt.ylabel('Frequency of Occurance')
plt.title('Difference Between First and Second Designs')
plt.grid(axis='y')
plt.show()