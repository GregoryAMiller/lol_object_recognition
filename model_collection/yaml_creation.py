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