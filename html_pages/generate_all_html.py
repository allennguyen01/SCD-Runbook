from html_pages.generate_html_pages import create_table_pages
from html_pages.generate_html_pages import create_plan_pages
from html_pages.generate_timeline import generate_timeline

if __name__ == "__main__":
    print("Started generating html pages...")

    create_table_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql', 'html_pages\webpages\scheduled.html')
    create_table_pages('html_pages\SQL_queries\IMPORTS.sql', 'html_pages\webpages\imports.html')
    create_table_pages('html_pages\SQL_queries\EXPORTS.sql', 'html_pages\webpages\exports.html')
    create_table_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql', 'html_pages\webpages\inventory.html')

    create_plan_pages('html_pages\SQL_queries\SCHEDULED_PLANS.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')
    create_plan_pages('html_pages\SQL_queries\ABAT_INVENTORY.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')
    create_plan_pages('html_pages\SQL_queries\IMPORTS.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')
    create_plan_pages('html_pages\SQL_queries\EXPORTS.sql', 'html_pages\SQL_queries\SCD_CONFIG.sql')

    generate_timeline('html_pages\SQL_queries\SCHEDULED_PLANS_TIMELINE.sql')

    print("Done generating all html pages!")