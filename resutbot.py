from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import logging

# --- NEW IMPORTS ---
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up a logger for this module
logger = logging.getLogger(__name__)

class result_bot:
    
    def __init__(self):
        """Initializes the bot, setting the driver and department lists to None."""
        self.driver = None
        self.departments = {}
        self.valid = []

    def bot_work(self, all_data_collected):
        """
        Starts the driver IN HEADLESS MODE, gets the result link, 
        and scrapes the list of departments.
        all_data_collected[0] = result link
        """
        try:
            # --- START OF MODIFICATIONS ---
            
            # 1. Set up Chrome Options
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080") # Set window size to avoid layout issues
            
            # 2. Set up the Service to auto-install the driver
            service = Service(ChromeDriverManager().install())
            
            # 3. Create the driver with the new service and options
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # --- END OF MODIFICATIONS ---
            
            self.driver.get(all_data_collected[0])
            self.driver.implicitly_wait(30)  # Wait for page to load
            
            select_department = self.driver.find_element(By.ID, "department1")
            select = Select(select_department)
            
            # Populate instance variables so they persist
            self.departments = {opt.text: opt.get_attribute("value") for opt in select.options}
            self.departments.pop('-- Select Department here --', None)  # Remove placeholder
            self.valid = list(self.departments.keys())  # List of department names
            
            logger.info(f"Successfully fetched {len(self.valid)} departments.")
            return self.valid  # Return the list of names
            
        except Exception as e:
            logger.error(f"Error in bot_work: {e}", exc_info=True)
            if self.driver:
                self.driver.quit()
                self.driver = None
            return []  # Return empty list on failure

    #
    # --- NO CHANGES NEEDED to select_department() ---
    #
    def select_department(self, all_data_collected):
        """
        Uses the active driver session to submit the form with all details.
        all_data_collected = [link, department_index, roll, dob]
        """
        
        # Check if the active driver session is active
        if self.driver is None:
            logger.error("No active driver session in select_department.")
            return "Error: Session expired. Please start over with /resultscheck."
        
        try:
            # Use the existing, stored driver
            driver = self.driver 
            
            # Get data from all_data_collected
            department_index = all_data_collected[1]
            roll_number = all_data_collected[2]
            date_of_birth = all_data_collected[3]
            
            # Find the department <select> element
            select_department_element = driver.find_element(By.ID, "department1")
            select = Select(select_department_element)
            
            # Use the stored department list to get the correct value
            choice = self.valid[department_index]  # Get name from index
            value = self.departments[choice]       # Get value from name
            
            logger.info(f"Selecting department: {choice} (value: {value})")
            select.select_by_value(value)
            
            roll_input = driver.find_element(By.ID, "usn")
            roll_input.send_keys(roll_number)
            
            dob_input = driver.find_element(By.ID, "dateofbirth")
            dob_input.send_keys(date_of_birth)
            
            btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Search']")
            btn.click()
            
            driver.implicitly_wait(10)  # Wait for results to load
            
            tables = driver.find_elements(By.TAG_NAME, "table")
            
            result_table = None
            n = 0
            for table in tables:
                n += 1
                if n == 2:  # Assuming the 2nd table is the correct one
                    result_table = table
                    break
            
            if result_table:
                table_png = "result_table.png"
                result_table.screenshot(table_png)
                logger.info(f"Successfully created screenshot: {table_png}")
                return table_png
            else:
                logger.warning("Could not find the result table after submitting form.")
                return "Error: Could not find the result table."

        except Exception as e:
            logger.error(f"Error in select_department: {e}", exc_info=True)
            return f"An error occurred: {e}"
            
        finally:
            # Always quit the driver after this step (success or fail)
            if self.driver:
                self.driver.quit()
                self.driver = None
if __name__ == "__main__":
    pass
