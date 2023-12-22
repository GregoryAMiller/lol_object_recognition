import requests
import yaml

# Function to fetch a list of champions from the modelviewer.lol API
def get_champions_data():
    api_url = "https://www.modelviewer.lol/api/champions?language=default"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # Return the JSON response if the request is successful
    else:
        raise Exception(f"Error fetching champions data: {response.status_code}")  # Raise an exception if the request fails

# Function to add skin data to each champion
def add_skin_data(champions_data):
    for champion in champions_data:  # Iterate over each champion in the list
        # Construct API URL to get skins for each champion
        api_url = f"https://www.modelviewer.lol/api/skins?id={champion['id']}&language=default"
        response = requests.get(api_url)
        if response.status_code == 200:
            champion['skins_data'] = response.json()  # Add skin data to the champion's dictionary
        else:
            # Print an error message if fetching skin data fails
            print(f"Error fetching skin data for champion {champion['id']}")

    return champions_data  # Return the updated list of champions with skin data

# Function to save the champions data with skins into a YAML file
def save_champion_skin_mapping(champions_data, file_path='champion_skin_mapping.yaml'):
    with open(file_path, 'w') as yaml_file:  # Open a file in write mode
        yaml.dump(champions_data, yaml_file)  # Write the champions data to the file in YAML format

# Main function to orchestrate the fetching and saving of champions data
def main():
    try:
        champions_data = get_champions_data()  # Get the list of champions
        champions_data_with_skins = add_skin_data(champions_data)  # Add skin data to each champion
        save_champion_skin_mapping(champions_data_with_skins)  # Save the data into a YAML file
        print("Champion data with skins saved to YAML file successfully.")
    except Exception as e:  # Catch any exceptions that occur during the process
        print(f"An error occurred: {e}")  # Print the error message


if __name__ == "__main__":
    main()