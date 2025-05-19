import pandas as pd
import random 

#df.loc[row_label, column_label]

# Create the table with percentages as integers (e.g., 37 means 37%)
data = {
    "Criteria": ["Endurance", "Complexity", "Quality", "Cost", "Safety", "Noise", "Sustainability"],
    "Weight (%)": [0.10, 0.15, 0.15, 0.20, 0.10, 0.10, 0.20],
    "Helicopter": [0.10, 0.22, 0.65, 0.37, 0.34, 0.10, 0.22],
    "Quadcopter": [0.10, 1, 1, 0.37, 0.70, 0.75, 0.37],
    "Osprey": [0.50, 0.38, 0.52, 0.83, 0.75, 1, 0.38],
    "Yangda": [0.75, 0.75, 0.65, 1, 0.90, 1, 0.58],
}

# Create the DataFrame
df = pd.DataFrame(data).set_index("Criteria")
print(df)



def Compare():
    #resetting the table
    data = {
        "Criteria": ["Endurance", "Complexity", "Quality", "Cost", "Safety", "Noise", "Sustainability"],
        "Weight (%)": [0.10, 0.15, 0.15, 0.20, 0.10, 0.10, 0.20],
        "Helicopter": [0.10, 0.22, 0.65, 0.37, 0.34, 0.10, 0.22],
        "Quadcopter": [0.10, 1, 1, 0.37, 0.70, 0.75, 0.37],
        "Osprey": [0.50, 0.38, 0.52, 0.83, 0.75, 1, 0.38],
        "Yangda": [0.75, 0.75, 0.65, 1, 0.90, 1, 0.58],
    }
    #global df
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

    # Compute weighted total score 
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
    Amount = round(random.uniform(0.01, 0.1), 2)
    #print(f"\nChanging weights: +{Amount:.2f} to '{Cat1}', -{Amount:.2f} from '{Cat2}'")

    # Modify the "Weight (%)" values
    df.loc[Cat1, "Weight (%)"] += Amount
    df.loc[Cat2, "Weight (%)"] -= Amount

    # Optional: ensure weights stay in bounds [0, 1] CHECK IF THIS IS NEEDED
    #df["Weight (%)"] = df["Weight (%)"].clip(lower=0, upper=1)

    # print("\nNew table")
    # print(df)


    # Compute weighted total score 
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

    print(PRE_Totals)
    return PRE_Totals, POST_Totals


#MAIN - I guess
for i in range(1000):
    Pre,Post = Compare()
    if max(Pre) >= 1:
        print("pAST 100% eRROR")
        print(max(Post))

