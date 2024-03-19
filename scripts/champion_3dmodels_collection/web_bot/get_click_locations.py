from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime

# Set up the WebDriver (this example uses Chrome)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment if you don't want the browser to open visibly
driver = webdriver.Chrome(options=options)

# Navigate to the website
driver.get('https://modelviewer.lol/model-viewer?id=1011')

# Wait for a specific element to ensure the page is fully loaded; adjust the selector as necessary
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

click_listener_script = """
var clickCount = 0;
var clickPositions = [];
// Use capturing by setting the third argument of addEventListener to true
document.addEventListener('click', function(event) {
    clickCount++;
    if(clickCount <= 2) {
        clickPositions.push({x: event.pageX, y: event.pageY});
        if(clickCount === 2) {
            document.body.setAttribute('data-clicks-recorded', JSON.stringify(clickPositions));
        }
    }
}, true);  // True here sets the listener to capture mode
"""

# Inject the JavaScript into the webpage
driver.execute_script(click_listener_script)

# Manual interaction: User performs two clicks on the webpage
# Wait for the custom attribute to appear on the body element
WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.body.hasAttribute('data-clicks-recorded');"))

# Retrieve the stored click positions
click_positions = driver.execute_script("return JSON.parse(document.body.getAttribute('data-clicks-recorded'));")

# Output the click positions
print(f"The recorded click positions are: {click_positions}")

# Append the click positions to a text file with a timestamp
with open('click_coordinates.txt', 'a') as file:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"{timestamp}: {click_positions}\n")

# Close the browser
driver.quit()
