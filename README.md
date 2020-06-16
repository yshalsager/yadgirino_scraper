# Yadgirino Scraper

## What's this?

Yadgirino is a persian website that hosts educational courses videos from various providers. This script is a scraper based on [Scrapy](https://scrapy.org) famous library that extracts any course download links from Yadgirino.

## Usage

- After cloning the project, you need to install the dependencies first using pip (19 or newer).

```
pip install .
```

- Then, get the url of the course you'd like to download from [Yadgirino](https://yadgirino.com).

- Also, you need an Iranian http proxy as the website won't show courses content if the IP address of the request is from outside for some reason I don't know.

- Finally run the scraper using the following command:

```
scrapy crawl courses -a url="[course url]" -a proxy="[proxy url]"

```

*Note:* The extracted links can be accessed from any IP adress.

### Example output

Example JSON output files are available [here](https://github.com/yshalsager/yadgirino_scraper/tree/master/example_output).

### Disclaimer
This script was written for educational purposes, I'm not responsible for misuse.
