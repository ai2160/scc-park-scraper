# Santa Clara County Campground Scraper

Notifies you when campsites at a santa clara county park is available for reservation.

**Note**: Start date must be at least 3 days from scraping date. This is a requirement by county.

## Requirements

    - A server with python 3.4 or greater
    - Free account with mailgun.com for email notification

## Usage

Fill in secrets.py with your mailgun account info. You will only need the private API key and domain.

Fill in config.json with your choice of start date, length and park id. When park id is set to '0' it means, look for all parks in santa clara.

```bash
cp example.secrets.py secrets.py    # Make a real secrets.py file with mailgun credentials
vim secrets.py                      # Fill in the mailgun secrets
cp example.config.json config.json  # Make a real config.json with desired camping dates
vim config.json                     # Fill in camping details
virtualenv .                        # Create a virtualenv
source bin/activate                 # Enter it
pip install -r requirements.txt     # Install python dependencies 
python scraper.py                   # Run the scraper
```
