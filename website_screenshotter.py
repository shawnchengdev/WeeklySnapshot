from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from PIL import Image
import time
from typing import Optional
import datetime


# Sets up and returns a Chrome browser instance
def setup_browser(window_size: dict, run_in_background: bool):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--window-size={window_size['x']},{window_size['y']}")
    if run_in_background:
        options.add_argument("--headless=new")  # Sets the browser invisible
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36") # User agent, helps the program look more like a real browser
    return webdriver.Chrome(options = options)


# Loops through each element_detail and tries to locate each element. If any elements are not found the website will be refreshed up to 2 times
def locate_all_elements(the_browser: webdriver.Chrome, element_details: list[dict], website_link: str):
    element_list = []

    count_repeated = 0
    while count_repeated < 2:
        for screenshot_info in element_details:
            for website_elements in screenshot_info["elements"]:
                element_list.append(locate_element(the_browser, website_elements["tag"], website_elements["class"], website_elements["aria"], website_elements["xpath"]))
                
        if not all(element_list):
            count_repeated += 1
            print("\nREPEATING SEARCH ON", website_link, f", Repeat: {count_repeated}")
            the_browser.refresh()
            time.sleep(4)
            continue

        print("Elements found...")
        return element_list
    print("\nCOULD NOT FIND ELEMENTS FROM", website_link, "\n")
    return None


# Finds the element that matches with at least one of the provided identifiers
# If xpath is being used, the rest of the css_selector parameters must be empty or xpath will be overidden
def locate_element(the_browser: webdriver.Chrome, tag_name: Optional[str], class_name: Optional[str], aria_label: Optional[str], xpath: Optional[str]):
    element_list = []
    css_selector = ""

    try:
        if xpath:
            element_list = the_browser.find_elements(By.XPATH, xpath)

        if tag_name:
            css_selector += tag_name
        
        if class_name:
            css_selector += "." + class_name

        if aria_label:
            css_selector += f"[aria-label='{aria_label}']"

        if css_selector:    
            element_list = the_browser.find_elements(By.CSS_SELECTOR, css_selector)

    except NoSuchElementException:
        print("ELEMENT NOT FOUND\nXPATH:", xpath, "\ncss_selector:", css_selector, "\n")
        return None
    
    for element in element_list:
        if element.is_displayed(): 
            return element
    return None


# Scrolls to a vertical position so that the target is centered on the screen
def browser_scroll(the_browser:webdriver.Chrome, y_location:int, browser_vertical_size:int):
    the_browser.execute_script(f"window.scrollTo(0, {y_location - browser_vertical_size/2})") # window.scrollTo() scrolls the number of pixels provided
    time.sleep(2)


# Returns a date string offset by months, days or years away from the current date
def delta_date_formatter(month_delta:int, day_delta:int, year_delta:int):
    date = ""
    if datetime.datetime.now().month + month_delta < 10:
        date += "0" + str(datetime.datetime.now().month + month_delta) + "-"
    else:
        date += str(datetime.datetime.now().month + month_delta) + "-"

    if datetime.datetime.now().day + day_delta < 10:
        date += "0" + str(datetime.datetime.now().day + day_delta) + "-"
    else:
        date += str(datetime.datetime.now().day + day_delta) + "-"

    date += str(datetime.datetime.now().year + year_delta)
    return date


# Interacts with the given element based off the specified interaction type
def interact_with_element(interactable_element: WebElement, interaction: str, values_to_send: Optional[str], wait_time: Optional[float]):
    match interaction:
        case "click":
            interactable_element.click()

        case "input_text":
            interactable_element.clear()
            interactable_element.send_keys(values_to_send)

        case _:
            pass
    
    if wait_time:
        time.sleep(wait_time)


# Crops the image around a specified element, assuming the element is centered on screen
def crop_image_element(element_position_x: int, element_size_x: int, element_size_y: int, x_size_adjusment: int, y_size_adjustment: int, original_file_path: str):
    im = Image.open(original_file_path)
    image_height = im.size[1]

    # Calculates the crop box (top-left and bottom-right corners) for cropping the image
    left = element_position_x - x_size_adjusment/2
    upper = image_height/2 - element_size_y/2 - y_size_adjustment/2
    right = element_position_x + element_size_x + x_size_adjusment/2
    lower = image_height/2 + element_size_y/2 + y_size_adjustment/2

    im = im.crop((left, upper, right, lower))
    return im
   
# Opens each website, locates target elements, scrolls to center them, takes screenshots, optionally interacts with elements, and crops images.
def screenshot_website_element(website_list: list[dict], window_size: dict, run_in_background: bool, screenshot_folder: str):
    print("Booting up browser...")
    browser = setup_browser(window_size, run_in_background)
    file_locations = []

    try:
        # Loops through all the websites
        for website in website_list:
            save_path_list = []

            print(f"\nOpening website {website['link']}...")
            browser.get(website["link"])  

            # Creates a save locations for the screenshots
            for screenshot in website["screenshot"]:
                save_path_list.append(screenshot_folder + screenshot["file_name"] + ".png")

            # Waits for a set period of time for the website to load in
            time.sleep(4)
        
            if not website["ignore_elements"]:
                # If the elements aren't found locate_all_elements will return none, and the rest of this iteration will be skipped
                elements = locate_all_elements(browser, website["screenshot"], website["link"])
                if elements is None:
                    continue

              # Stores position and size of the first element to use for scrolling and cropping
                element_position = elements[0].location
                element_size = elements[0].size

                # Scrolls to the element's position
                browser_scroll(browser, element_position["y"] + website["scroll_adjustment"], window_size["y"])
            else:
                browser_scroll(browser, website["scroll_adjustment"], window_size["y"])

            # Loops and interacts with elements before taking a screenshot, cropping an element and appending the cropped photo to file_locations  
            for i, save_path in enumerate(save_path_list):
                if not website["ignore_elements"]:
                    element_interacted = 0
                    for j in range(len(website["screenshot"][i]["elements"])):
                        interact_with_element(elements[j], website["screenshot"][i]["elements"][j]["interaction"], delta_date_formatter(0, 0, -4), website["screenshot"][i]["elements"][j]["wait_time"])
                        element_interacted += 1

                    # Removes interacted elements from element_list 
                    for _ in range(element_interacted):
                        elements.pop(0)
                
                browser.save_screenshot(save_path)

                if not website["no_crop"]:
                    if not website["ignore_elements"]:
                        crop_image_element(element_position["x"] + website["x_position_adjustment"], element_size["width"], element_size["height"], website["x_size_adjustment"], website["y_size_adjustment"], save_path).save(save_path[:-4] + "_cut" + save_path[-4:])
                    else:
                        crop_image_element(website["x_position_adjustment"], 0, 0, website["x_size_adjustment"], website["y_size_adjustment"], save_path).save(save_path[:-4] + "_cut" + save_path[-4:])
                    
                    # Appends the cropped photos to file_locations
                    file_locations.append(save_path[:-4] + "_cut" + save_path[-4:])
                else:
                    # Appends the full photos to file_locations
                    file_locations.append(save_path)
                print("Images saved...")
    # Ensures the browser always quits
    finally:
        browser.quit()
        print("Browser has exited...")

    return file_locations
