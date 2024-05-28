import json
import math

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(building_data):
    total_loss = 0
    years = 1  # Assuming calculations are based on a single year
    losses=[]
    discount_rate = 0.05
    for building in building_data:
        floor_area = building['floor_area']
        building_id = building['buildingId']
        construction_cost = building['construction_cost']
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']

        # Calculate the exponential term
        exponential_part = math.exp(inflation_rate * (floor_area / 1000))
        le=((construction_cost * exponential_part * hazard_probability) / ((1 + discount_rate) ** years))

        # Add to losses list and total loss
        losses.append({'buildingId': building_id, 'loss_estimate': le})

        # Calculate future cost is modefiled. Equation reffred from https://www.fe.training/free-resources/project-finance/modelling-inflation/
        future_cost = construction_cost * ((1 + inflation_rate) ** years) 

        # Calculate risk-adjusted loss. its mentioned in given task like this "for each building, multiply its future construction cost by its hazard probability to assess the potential financial impact if the hazard were to occur". So i modefiled below equation
        
        risk_adjusted_loss = future_cost * hazard_probability

        # Calculate present value of the risk-adjusted loss
          # Assuming a 5% discount rate. This line move to top
        present_value_loss = risk_adjusted_loss / (1 + discount_rate)

        # Calculate maintenance and total maintenance cost
        maintenance_cost = floor_area * 50  # assuming a flat rate per square meter
        total_maintenance_cost = maintenance_cost / (1 + discount_rate)  

        # Total loss calculation. I changed the below formula also. The task description explicitly focuses on financial losses due to potential hazards, adjusted for inflation and discounted to present value. It does not mention ongoing maintenance costs. Including maintenance costs introduces additional complexity not required by the task. Thus, focusing on the essential components makes the solution more aligned with the requirements.
        total_loss += present_value_loss 

    return total_loss,losses

# Main execution function
def main():
    data = load_data('data.json')
    total_projected_loss,loss = calculate_projected_losses(data)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")
    for losses in loss:
         print(f"Building {losses['buildingId']} Estimated Loss: ${losses['loss_estimate']:.2f}")
    

if __name__ == '__main__':
    main()
