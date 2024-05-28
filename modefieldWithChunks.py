import json
import math

def load_data_in_chunks(filepath, chunk_size=10000):
    with open(filepath, 'r') as file:
        data = json.load(file)
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

def process_chunk(chunk):
    losses = []
    total_loss = 0
    discount_rate = 0.05
    years = 1
    
    for building in chunk:
        building_id = building['buildingId']
        floor_area = building['floor_area']
        construction_cost = building['construction_cost']
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']
        exp_term = math.exp(inflation_rate * (floor_area / 1000))
        loss_estimate = (
            (construction_cost * exp_term * hazard_probability) / 
            ((1 + discount_rate) ** years)
        )
        losses.append({'buildingId': building_id, 'loss_estimate': loss_estimate})
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
    
    return losses, total_loss

def main():
    total_projected_loss = 0
    for chunk in load_data_in_chunks('data.json'):
        _, chunk_total_loss = process_chunk(chunk)
        total_projected_loss += chunk_total_loss
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

if __name__ == '__main__':
    main()
