const { Builder, Browser, By } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const path = require('path');

// Directories
const htmlDir = 'digikala_pages';
const outputDir = 'output';
if (!fs.existsSync(htmlDir)) fs.mkdirSync(htmlDir);
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

// CSV writer
const csvWriter = createCsvWriter({
  path: path.join(outputDir, 'digikala_data.csv'),
  header: [
    { id: 'Category', title: 'Category' },
    { id: 'Title', title: 'Title' },
    { id: 'Price', title: 'Price' },
    {id:'color' , title: 'color'},
    { id: 'URL', title: 'URL' },
    { id: 'HTML_File', title: 'HTML_File' },
  ],
  encoding: 'utf8'
});

// Categories to crawl
const categories = [
  { name: 'Books', url: 'https://www.digikala.com/search/category-book/' },
  { name: 'Clothes', url: 'https://www.digikala.com/search/category-women-clothing/' },
  { name: 'Laptops', url: 'https://www.digikala.com/search/notebook-netbook-ultrabook/?attributes%5B2316%5D%5B0%5D=21388&sort=7&camCode=2174' },
  { name :'Phone' , url: 'https://www.digikala.com/search/category-mobile-phone/'},
  {name :'cooking',  url: 'https://www.digikala.com/search/category-cooking/'},
]


async function crawlCategory(driver, categoryName, categoryUrl, startIndex = 0) {
  const data = [];

  console.log(`Navigating to ${categoryUrl} (${categoryName})`);
  await driver.get(categoryUrl);
  await driver.sleep(10000);

  for (let i = 0; i < 5; i++) {
    await driver.executeScript('window.scrollTo(0, document.body.scrollHeight);');
    await driver.sleep(4000);
  }

  const categoryHtml = await driver.getPageSource();
  fs.writeFileSync(`debug_category_${categoryName}.html`, categoryHtml, 'utf8');

  const productLinks = await driver.findElements(By.css('a[href*="/product/dkp-"]'));
  const productUrls = [];

  for (let i = 0; i < Math.min(productLinks.length, 10); i++) {
    try {
      const href = await productLinks[i].getAttribute('href');
      if (href && href.includes('/product/dkp-')) productUrls.push(href);
    } catch (e) {
      console.log(`Error getting href for ${categoryName} item ${i}: ${e}`);
    }
  }

  for (const [i, url] of productUrls.entries()) {
    try {
      console.log(`Visiting product: ${url}`);
      await driver.get(url);
      await driver.sleep(5000);

      let title = 'N/A';
      try {
        const titleElement = await driver.findElement(By.css('p.ellipsis-2, h1.text-h4'));
        title = await titleElement.getText();
      } catch (e) {
        console.log(`Error getting title for ${url}: ${e}`);
      }

      let price = 'N/A';
      try {
        const priceElement = await driver.findElement(By.css('span[data-testid="price-no-discount"]'));
        price = await priceElement.getText();
        price = price.replace(/[, تومان]/g, '').trim();
      } catch (e) {
        console.log(`Error getting price for ${url}: ${e}`);
      }
      let color = 'N/A';
        try {
          const colorElement = await driver.findElement(By.xpath("//span[contains(text(),'رنگ')]"));
          const colorText = await colorElement.getText(); 
          color = colorText.split(':')[1]?.trim() || 'N/A';
        } catch (e) {
          console.log(`Error getting color for ${url}: ${e}`);
        }


      const html = await driver.getPageSource();
      const htmlFile = path.join(htmlDir, `${categoryName}_${startIndex + i + 1}.html`);
      fs.writeFileSync(htmlFile, html, 'utf8');

      data.push({
        Category: categoryName,
        Title: title,
        Price: price,
        color:color,
        URL: url,
        HTML_File: htmlFile
      });

      console.log(`Crawled: ${title} (${categoryName})`);
      await driver.sleep(2500);
    } catch (e) {
      console.log(`Error crawling ${url}: ${e}`);
    }
  }

  return data;
}

async function crawlDigikala() {
  const options = new chrome.Options()
    .addArguments('--headless=new')
    .addArguments('--disable-gpu')
    .addArguments('--window-size=1920,1080')
    .addArguments('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');

  const driver = await new Builder()
    .forBrowser(Browser.CHROME)
    .setChromeOptions(options)
    .setChromeService(new chrome.ServiceBuilder('E:/Files/wikipeadia/chromedriver/chromedriver.exe'))
    .build();

  let allData = [];

  try {
    let counter = 0;
    for (const category of categories) {
      const catData = await crawlCategory(driver, category.name, category.url, counter);
      allData = allData.concat(catData);
      counter += catData.length;
    }

    await csvWriter.writeRecords(allData);
    console.log(`✅ Total ${allData.length} records saved to CSV.`);
  } catch (e) {
    console.log(`❌ General error: ${e}`);
  } finally {
    await driver.quit();
  }
}

crawlDigikala().catch(console.error);
