import pandas as pd
import numpy as np
import math

def calculate_loss(row, discount_rate=0.05, years=1):
    exp_term = math.exp(row['inflation_rate'] * (row['floor_area'] / 1000))
    loss_estimate = (
        (row['construction_cost'] * exp_term * row['hazard_probability']) / 
        ((1 + discount_rate) ** years)
    )
    return loss_estimate

def main():
    chunk_size = 10000
    total_projected_loss = 0
    
    # Read the entire JSON file
    data = pd.read_json('data.json')
    
    # Split data into chunks
    num_chunks = int(np.ceil(len(data) / chunk_size))
    
    for i in range(num_chunks):
        chunk = data.iloc[i * chunk_size:(i + 1) * chunk_size].copy()
        print("chunk",chunk)
        chunk.loc[:, 'loss_estimate'] = chunk.apply(calculate_loss, axis=1)
        total_projected_loss += chunk['loss_estimate'].sum()
    
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

if __name__ == '__main__':
    main()
