# Holiday Sales Scraper

Essentially, just provide a CSV formatted file with the names and emails of your customers, and it will send them the holiday deals of the day.

When the program is run, it will scrape certain sites for holiday deals, and then place information about those deals in a (local) SQL server, as well as to a python program that formats emails. These emails are then sent via a flask server to all of the emails in the CSV file. Simple.
