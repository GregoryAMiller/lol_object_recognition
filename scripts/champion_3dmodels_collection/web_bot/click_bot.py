import json
import random
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import yaml
from datetime import datetime, timedelta
# Function to generate a random coordinate within a given range
def random_coordinate(x_range, y_range):
    return (random.randint(*x_range), random.randint(*y_range))

def get_skin_urls(champions_data, champion_name=None, skin_name=None):
    # Modified to return URLs along with corresponding champion and skin names
    results = []
    for champion, skins in champions_data.items():
        if champion_name and champion.lower() == champion_name.lower():
            for skin, skin_id in skins.items():
                if skin_name and skin.lower() == skin_name.lower():
                    url = f"https://modelviewer.lol/model-viewer?id={skin_id}"
                    results.append((url, champion, skin))
                elif not skin_name:
                    url = f"https://modelviewer.lol/model-viewer?id={skin_id}"
                    results.append((url, champion, skin))
            break
        elif not champion_name:
            for skin, skin_id in skins.items():
                url = f"https://modelviewer.lol/model-viewer?id={skin_id}"
                results.append((url, champion, skin))
    return results

def perform_clicks_on_page(driver):
    first_click_range = ((822, 847), (619, 640))
    second_click_range = ((584, 856), (342, 376))
    first_click_pos = random_coordinate(*first_click_range)
    second_click_pos = random_coordinate(*second_click_range)
    actions = ActionChains(driver)
    actions.move_by_offset(first_click_pos[0], first_click_pos[1]).click()
    actions.pause(2)
    actions.move_by_offset(-first_click_pos[0], -first_click_pos[1])
    actions.move_by_offset(second_click_pos[0], second_click_pos[1]).click()
    actions.pause(2)
    actions.perform()

def wait_for_download(download_folder, timeout=30):
    start_time = time.time()
    download_folder = Path(download_folder)
    
    while True:
        if all(not file.suffix == '.crdownload' for file in download_folder.iterdir()):
            # No .crdownload file, download completed
            return
        elif time.time() - start_time > timeout:
            raise Exception('Download timed out')
        else:
            # Wait a bit and check again
            time.sleep(2)

def move_downloaded_file(download_folder, target_folder, file_prefix):
    for file in Path(download_folder).glob(file_prefix + '*'):
        target_path = target_folder / file.name
        shutil.move(str(file), str(target_path))
        print(f'Moved downloaded file to {target_path}')

def check_yaml_update(yaml_file_path, json_file_path, last_updated_file_path):
    need_update = False
    if not json_file_path.exists():
        need_update = True
    else:
        try:
            with open(last_updated_file_path, 'r') as file:
                last_run_time_str = file.read().split(': ')[1]
            last_run_time = datetime.strptime(last_run_time_str, '%Y-%m-%d %H:%M:%S')
            if datetime.now() - last_run_time > timedelta(days=30):
                need_update = True
        except FileNotFoundError:
            need_update = True
    
    if need_update:
        convert_yaml_to_json(yaml_file_path, json_file_path)
        with open(last_updated_file_path, 'w') as file:
            file.write(f"Last run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def convert_yaml_to_json(yaml_file_path, json_file_path):
    with open(yaml_file_path, 'r') as file:
        skins_yaml = yaml.safe_load(file)
    champions_json = {}
    for champion in skins_yaml:
        champion_name = champion['name']
        skins_data = champion['skins_data']
        skins_dict = {skin['name']: skin['id'] for skin in skins_data}
        champions_json[champion_name] = skins_dict
    with open(json_file_path, 'w') as json_file:
        json.dump(champions_json, json_file, indent=4)
    print(f"JSON file created at: {json_file_path}")

def main():

    current_dir = Path.cwd()
    yaml_file_path = current_dir.parent / 'champion_skin_mapping.yaml'
    json_file_path = current_dir / 'champion_skin_mapping.json'
    last_updated_file_path = current_dir.parent / 'yaml_file_last_updated.txt'

    check_yaml_update(yaml_file_path, json_file_path, last_updated_file_path)

    with open(json_file_path, 'r') as file:
        champions_data = json.load(file)

    champion_name = "Annie"  # Assuming these might be provided by the user or left empty
    skin_name = "Annie"
    download_folder = current_dir.parent.parent.parent / 'data/3d_glb_files'

    selected_urls_champions_skins = get_skin_urls(champions_data, champion_name, skin_name)

    for url, champ_name, skin_name in selected_urls_champions_skins:
        target_folder = download_folder / champ_name / skin_name
        target_folder.mkdir(parents=True, exist_ok=True)
        
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": str(target_folder)}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        perform_clicks_on_page(driver)

    driver.quit()

if __name__ == "__main__":
    main()
