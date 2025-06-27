import weekly_sleep_duration_calculator
import time
import website_screenshotter
import email_packager

# The date and time when the program will start running
# Day of the week: Monday is 0, Sunday is 6
SCHEDULED_DATE = {"Day": 4, "Hour": 12, "Minute": 0, "Second": 0}

# Browser options
WINDOW_SIZE = {"x" : 1920, "y" : 1080}
RUN_IN_BACKGROUND = True

# Website and screenshot options
# The first element in each 'screenshot' and 'elements' list is used for scrolling and cropping
websites = [
    {
        "link": "https://www.lme.com/Metals/Non-ferrous/LME-Copper#Price+graphs", 
        "scroll_adjustment": 215, 

        # Crop Details
        "x_position_adjustment" : 0, # If ignore_elements is true, 0 is the furthest left pixel 
        "x_size_adjustment" : 70, #If ignore_elements is true, this dictates the size of the crop
        "y_size_adjustment" : 250, 
        
        # If True, disables the search and interaction with elements, MUST be off if there are no elements provided
        "ignore_elements" : False,

        # The program emails the full photo without cropping it
        "no_crop" : False,

        # Each item in screenshot will signal the creation of a photo
        "screenshot" : [
            {
                "file_name" : "1_month_copper_price_graph",
                "elements" : [
                    {
                        "tag" : None, 
                        "class" : "chart__canvas", 
                        "aria" : "LME Copper Official Prices ", 
                        "xpath" : None,
                        "interaction" : None,
                        "wait_time" : 0 # The time waiting after this element's interaction is done
                    }
                ] 
            },
            {
                "file_name" : "4_year_copper_price_graph", 
                "elements" : [
                    {
                        "tag" : None, 
                        "class" : None, 
                        "aria" : None, 
                        "xpath" : "//input[@type='date' and @name='start-date']",
                        "interaction" : "input_text",
                        "wait_time" : 0
                    },
                    {
                        "tag" : None, 
                        "class" : "button-primary.chart-controls__element", 
                        "aria" : None, 
                        "xpath" : None,
                        "interaction" : "click",
                        "wait_time" : 3
                    }
                ] 
            }
        ]
    }, 
    {
        "link": "https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium#Price+graphs", 
        "scroll_adjustment": 215, 
        "x_position_adjustment" : 0, 
        "x_size_adjustment" : 70, 
        "y_size_adjustment" : 250, 
        "ignore_elements" : False,
        "no_crop" : False,
        "screenshot" : [
            {
                "file_name" : "1_month_aluminium_price_graph", 
                "elements" : [
                    {
                        "tag" : "canvas", 
                        "class" : "chart__canvas", 
                        "aria" : None,
                        "xpath" : None,
                        "interaction" : None,
                        "wait_time" : 0
                    }
                ] 
            },
            {
                "file_name" : "4_year_aluminium_price_graph", 
                "elements" : [
                    {
                        "tag" : None, 
                        "class" : None, 
                        "aria" : None, 
                        "xpath" : "//input[@type='date' and @name='start-date']",
                        "interaction" : "input_text",
                        "wait_time" : 0
                    },
                    {
                        "tag" : None, 
                        "class" : "button-primary.chart-controls__element", 
                        "aria" : None, 
                        "xpath" : None,
                        "interaction" : "click",
                        "wait_time" : 3
                    }
                ] 
            }
        ]
    }, 
    {
        "link": "https://www.lme.com/Metals/Ferrous/LME-Steel-HRC-FOB-China-Argus#Price+graph", 
        "scroll_adjustment": 215, 
        "x_position_adjustment" : 0, 
        "x_size_adjustment" : 70, 
        "y_size_adjustment" : 250, 
        "ignore_elements" : False,
        "no_crop" : False,
        "screenshot" : [
            {
                "file_name" : "1_month_steel_price_graph", 
                "elements" : [
                    {
                        "tag" : "canvas", 
                        "class" : "chart__canvas", 
                        "aria" : "LME Steel Scrap HRC FOB China (Argus)  Closing prices graph", 
                        "xpath" : None,
                        "interaction" : None,
                        "wait_time" : 0
                    }
                ] 
            },
            {
                "file_name" : "4_year_steel_price_graph", 
                "elements" : [
                    {
                        "tag" : None, 
                        "class" : None, 
                        "aria" : None, 
                        "xpath" : "//input[@type='date' and @name='start-date']",
                        "interaction" : "input_text",
                        "wait_time" : 0
                    },
                    {
                        "tag" : None, 
                        "class" : "button-primary.chart-controls__element", 
                        "aria" : None, 
                        "xpath" : None,
                        "interaction" : "click",
                        "wait_time" : 3
                    }
                ] 
            }
        ]
    }, 
    {
        "link": "https://www.lme.com/en/Metals/Non-ferrous/LME-Nickel#Price+graphs", 
        "scroll_adjustment": 215, 
        "x_position_adjustment" : 0, 
        "x_size_adjustment" : 70, 
        "y_size_adjustment" : 250, 
        "ignore_elements" : False,
        "no_crop" : False,
        "screenshot" : [
            {
                "file_name" : "1_month_nickel_price_graph", 
                "elements" : [
                    {
                        "tag" : "canvas", 
                        "class" : "chart__canvas", 
                        "aria" : "LME Nickel Official Prices graph", 
                        "xpath" : None,
                        "interaction" : None,
                        "wait_time" : 0
                    }
                ] 
            },
            {
                "file_name" : "4_year_nickel_price_graph", 
                "elements" : [
                    {
                        "tag" : None, 
                        "class" : None, 
                        "aria" : None, 
                        "xpath" : "//input[@type='date' and @name='start-date']",
                        "interaction" : "input_text",
                        "wait_time" : 0
                    },
                    {
                        "tag" : None, 
                        "class" : "button-primary.chart-controls__element", 
                        "aria" : None, 
                        "xpath" : None,
                        "interaction" : "click",
                        "wait_time" : 3
                    }
                ] 
            }
        ]
    }, 
    {
        "link": "https://www.xe.com/currencycharts/?from=USD&to=TWD&view=1M", 
        "scroll_adjustment": -75, 
        "x_position_adjustment" : 0, 
        "x_size_adjustment" : 70, 
        "y_size_adjustment" : 560, 
        "ignore_elements" : False,
        "no_crop" : False,
        "screenshot" : [
            {
                "file_name" : "1_month_USD_to_TWD_conversion_graph", 
                "elements" : [
                    {
                        "tag" : "g", 
                        "class" : "recharts-layer", 
                        "aria" : None, 
                        "xpath" : None,
                        "interaction" : None,
                        "wait_time" : 0
                    }
                ] 
            },
            {
                "file_name" : "5_year_USD_to_TWD_conversion_graph", 
                "elements" : [
                    {
                        "tag" : None, 
                        "class" : None, 
                        "aria": None, 
                        "xpath" : "//button[text()='5Y']",
                        "interaction": "click",
                        "wait_time" : 3
                    }
                ] 
            }
        ]
    }
]

SCREENSHOT_FOLDER = "Your Screenshot Folder" # Example:"C:/Users/YourUsername/Desktop/screenshots" 

# Email details
SENDER_EMAIL = "Your Email"       
RECEIVER_EMAIL = "Reciever Email"        
PASSWORD = "google app password" #Put your google app password      
SUBJECT = "Weekly Metal and TWD Value Update"      
BODY = """The financial graphs are attached below.   

Links
Copper: https://www.lme.com/Metals/Non-ferrous/LME-Copper#Price+graphs
Aluminium: https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium#Price+graphs
Steel: https://www.lme.com/Metals/Ferrous/LME-Steel-HRC-FOB-China-Argus#Price+graph
Nickel: https://www.lme.com/en/Metals/Non-ferrous/LME-Nickel#Price+graphs
USD to TWD Conversion: https://www.xe.com/currencycharts/?from=USD&to=TWD&view=1M
"""


def main():
    while True:
        time.sleep(weekly_sleep_duration_calculator.get_sleep_duration(SCHEDULED_DATE))
        print("\nAwoken")
        photo_locations = website_screenshotter.screenshot_website_element(websites, WINDOW_SIZE, RUN_IN_BACKGROUND, SCREENSHOT_FOLDER)
        email_packager.email_files(SENDER_EMAIL, RECEIVER_EMAIL, PASSWORD, SUBJECT, BODY, photo_locations)


if __name__ == "__main__":
    main()
