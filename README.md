Wikipedia and Digikala Web Scraper

This project contains two web scrapers for extracting data from Wikipedia and Digikala. The Wikipedia scraper (wiki_crawler.py) extracts data from book-related Wikipedia pages. The Digikala scraper (digikala/digikala_crawler.js) extracts product data (title, price, color, URL, HTML) from Books, Women's Clothing, Cooking, Laptop, and Phone categories. Data is saved to CSV files, and HTML pages are stored for debugging.
Features


Digikala Scraper (digikala/digikala_crawler.js):
Scrapes products from:
Books: https://www.digikala.com/search/category-book/
Women's Clothing: https://www.digikala.com/search/category-women-clothing/
Cooking: https://www.digikala.com/search/category-cooking/
Laptop: https://www.digikala.com/search/notebook-netbook-ultrabook/?attributes%5B2316%5D%5B0%5D=21388&sort=7&camCode=2174
Phone: https://www.digikala.com/search/category-mobile-phone/


Extracts product titles, prices, colors, URLs, and saves HTML.
Saves data to digikala/output/digikala_data.csv (columns: Category, Title, Price, color, URL, HTML_File).
Saves HTML in digikala/digikala_pages/[books|clothes|cooking|laptop|phone]/.


Wikipedia Scraper (wiki_crawler.py):
Scrapes book-related data from Wikipedia pages.
Saves data to output/wiki_data.csv.
Saves HTML pages in wiki_pages/ for various books.


Uses headless Chrome for efficient scraping.

Prerequisites

Node.js: Version 14 or higher (for Digikala).
Python: Version 3.6 or higher (for Wikipedia).
Chrome Browser: Compatible with ChromeDriver (e.g., Chrome 138).
ChromeDriver: Place at E:/Files/wikipeadia/chromedriver/chromedriver.exe or update path in digikala/digikala_crawler.js.

Installation

Clone the repository:git clone :https://github.com/Reza-Tahmasbi/Information-Retrieval-Project.git
cd wikipedia


Install Digikala dependencies:cd digikala
npm install selenium-webdriver csv-writer


Install Wikipedia dependencies:pip install selenium


Download ChromeDriver:
Get the version matching your Chrome browser from ChromeDriver downloads.
Place at E:/Files/wikipeadia/chromedriver/chromedriver.exe or update path.



Usage

Run Digikala scraper:cd digikala
node digikala_crawler.js


Output: CSV (digikala/output/digikala_data.csv); HTML (digikala/digikala_pages/[books|clothes|cooking|laptop|phone]/).


Run Wikipedia scraper:python wiki_crawler.py


Output: CSV (output/wiki_data.csv); HTML (wiki_pages/).



Project Structure


wikipedia/
├── digikala/
│   ├── digikala_crawler.js       # Digikala scraper for Books, Clothes, Cooking, Laptop, Phone
│   ├── digikala_pages/           # Digikala HTML files
│   │   ├── books/                # Books HTML files
│   │   ├── clothes/              # Clothes HTML files
│   │   ├── cooking/              # Cooking HTML files
│   │   ├── laptop/               # Laptop HTML files
│   │   ├── phone/                # Phone HTML files
│   ├── output/
│   │   └── digikala_data.csv     # Digikala data
│   └── package.json              # Node.js dependencies
├── wiki_crawler.py               # Wikipedia scraper for books
├── wiki_pages/                   # Wikipedia HTML files for books
├── output/
│   └── wiki_data.csv             # Wikipedia data
└── README.md                     # This file




Notes

The Digikala scraper targets up to 10 products per category to avoid rate-limiting.
For Clothes, verify selectors h3.ellipsis-2.text-body2-strong.text-neutral-700.styles_VerticalProductCard__productTitle__6zjjN (title) and span[data-testid="price-final"] (price) in digikala/digikala_pages/clothes/. The current script uses incorrect selectors for Clothes.
The color field may not apply to all categories (e.g., Books, Laptops); expect N/A for some products.
Update Wikipedia section with wiki_crawler.py details (e.g., URLs, data extracted).
For CAPTCHAs, reduce maxProducts or add a proxy in digikala_crawler.js:options.addArguments('--proxy-server=http://your-proxy:port');



Troubleshooting

No links scraped: Inspect category pages in Chrome DevTools:document.querySelectorAll('a[href*="/product/dkp-"]').forEach(el => console.log(el.href));

Try div.products-grid a[href*="/product/dkp-"] if needed.
Selector errors: Check HTML files in digikala/digikala_pages/[category]/ or wiki_pages/. For Clothes, update title/price selectors in digikala_crawler.js.
GCM/TensorFlow errors: Unrelated; ignore unless critical.

License
MIT License. See LICENSE file.
Contributing
Open issues or pull requests to improve the scrapers!
