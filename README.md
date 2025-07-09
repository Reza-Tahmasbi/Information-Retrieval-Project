# Wikipedia and Digikala Web Scraper & Analysis

This project is a comprehensive web scraping and data analysis toolset designed to extract and process data from Wikipedia and Digikala. It includes web scrapers for collecting data, preprocessing scripts, and machine learning (ML) pipelines for classification and clustering. The Wikipedia scraper extracts book-related data, while the Digikala scraper gathers product information across multiple categories. The project also features ML analysis using Python, saving results as CSVs, HTML files, and visualizations.

## Features

### Digikala Scraper
- **Target Categories and URLs**:
  - Books: [https://www.digikala.com/search/category-book/](https://www.digikala.com/search/category-book/)
  - Women's Clothing: [https://www.digikala.com/search/category-women-clothing/](https://www.digikala.com/search/category-women-clothing/)
  - Cooking: [https://www.digikala.com/search/category-cooking/](https://www.digikala.com/search/category-cooking/)
  - Laptops: [https://www.digikala.com/search/notebook-netbook-ultrabook/?attributes%5B2316%5D%5B0%5D=21388&sort=7&camCode=2174](https://www.digikala.com/search/notebook-netbook-ultrabook/?attributes%5B2316%5D%5B0%5D=21388&sort=7&camCode=2174)
  - Phones: [https://www.digikala.com/search/category-mobile-phone/](https://www.digikala.com/search/category-mobile-phone/)
- **Data Extracted**: Product titles, prices, colors, URLs, and associated HTML content.
- **Output**:
  - CSV: `digikala_data.csv` (columns: `Category`, `Title`, `Price`, `color`, `URL`, `HTML_File`).
  - HTML: Stored in category-specific subdirectories (e.g., `digikala_pages/books/`, `digikala_pages/clothes/`).
- **Technology**: Uses Node.js with Selenium WebDriver and headless Chrome.

### Wikipedia Scraper
- **Target Data**: Book-related content from Wikipedia pages.
- **Data Extracted**: Text content, categories, and titles (details in `wiki_crawler.py`).
- **Output**:
  - CSV: `wiki_data.csv`.
  - HTML: Stored in `wiki_pages/` for debugging.
- **Technology**: Uses Python with Selenium and headless Chrome.

### Machine Learning Analysis
- **Preprocessing**: Adapts to both datasets (Wikipedia and Digikala) with project-specific text processing (e.g., Persian support for Digikala).
- **Features**:
  - Classification: Implements Naive Bayes, Linear SVM, and Random Forest.
  - Clustering: Uses K-means clustering.
  - Visualization: Generates word clouds, confusion matrices, and saves metrics.
- **Output**: Saved in `output/wiki/` or `output/digi/` (e.g., `wordcloud_*.png`, `confusion_matrix_*.png`, `classification_report_*.txt`, `clustering_metrics.txt`).
- **Technology**: Python with scikit-learn, NLTK, hazm (for Persian), and matplotlib.

## Prerequisites

- **Node.js**: Version 14 or higher (for Digikala scraper).
- **Python**: Version 3.6 or higher (for Wikipedia scraper and ML).
- **Chrome Browser**: Compatible with ChromeDriver (e.g., Chrome 138 or later).
- **ChromeDriver**: Download from [ChromeDriver downloads](https://chromedriver.chromium.org/downloads) and place at `E:/Files/wikipeadia/chromedriver/chromedriver.exe` or update the path in the scraper scripts.
- **Python Dependencies**: Install via `pip install selenium pandas numpy scikit-learn nltk matplotlib wordcloud hazm`.
- **NLTK Data**: Download required data by running `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"`.
- **Node.js Dependencies**: Install via `npm install selenium-webdriver csv-writer` in the Digikala directory.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Reza-Tahmasbi/Information-Retrieval-Project.git
   cd Information-Retrieval-Project
   ```

   0. install chrome driver in case you want to crawl
   ```bash
   1. pip install -r requirements.txt
   ```

   2. cd digikala
   ```bash
    npm install selenium-webdriver csv-writer
   ```
   3. python nltk_packages.py
   4. python main.py (adjust the project variable, whether 'wiki' or 'digi')

