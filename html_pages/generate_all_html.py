from generate_html_pages import create_main_pages
from generate_plan_pages import create_plan_pages
from generate_timeline import generate_timeline
import os

if __name__ == "__main__":
    print("Started generating html pages...")

    create_main_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql', 'html_pages\webpages\scheduled.html')
    create_main_pages('html_pages\SQL_queries\IMPORTS.sql', 'html_pages\webpages\imports.html')
    create_main_pages('html_pages\SQL_queries\EXPORTS.sql', 'html_pages\webpages\exports.html')
    create_main_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql', 'html_pages\webpages\inventory.html')
    print("Table pages generated successfully.")

    # try:
    #     os.mkdir("html_pages\webpages\plan_pages")
    # except FileExistsError:
    #     print("'plan_pages' folder already exists.")
    # create_plan_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql')
    # create_plan_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql')
    # create_plan_pages('html_pages\SQL_queries\IMPORTS.sql')
    # create_plan_pages('html_pages\SQL_queries\EXPORTS.sql')
    # print("SCD config pages for Batch Job Groups generated successfully.")

    # generate_timeline('html_pages\SQL_queries\SCHEDULED_PLANS_TIMELINE.sql')
    # print("Timeline page generated successfully.")

    print("Done generating all html pages!")