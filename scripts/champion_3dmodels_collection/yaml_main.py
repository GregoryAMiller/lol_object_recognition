import yaml_functions


def main():
    try:
        champions_data = yaml_functions.get_champions_data()  # Get the list of champions

        champions_data_with_skins = yaml_functions.add_skin_data(champions_data)  # Add skin data to each champion

        yaml_functions.save_champion_skin_mapping(champions_data_with_skins)  # Save the data into a YAML file

        print("Champion data with skins saved to YAML file successfully.")

        yaml_functions.record_last_run_time()  # Record the last run time
        
    except Exception as e:  # Catch any exceptions that occur during the process
        print(f"An error occurred: {e}")  # Print the error message

if __name__ == "__main__":
    main()