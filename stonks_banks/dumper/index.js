import { createScraper } from "israeli-bank-scrapers";

import { readFileSync } from "fs";

(async function () {
  try {
    // parse parameters from stdin
    const params = JSON.parse(readFileSync(process.stdin.fd, "utf-8"));

    const date_1_month_back = new Date();
    date_1_month_back.setMonth(date_1_month_back.getMonth() - 1);
    date_1_month_back.setHours(0, 0, 0, 0);

    // read documentation below for available options
    const options = {
      companyId: params["bank"],
      startDate: date_6_months_back,
      combineInstallments: false,
      showBrowser: false,
      verbose: true,
      futureMonthsToScrape: 2,
      additionalTransactionInformation: true,
      args: ["--no-sandbox"],
    };

    const scraper = createScraper(options);
    const scrapeResult = await scraper.scrape(params["credentials"]);
    scrapeResult["queryTime"] = new Date().toISOString();

    console.log(JSON.stringify(scrapeResult));
  } catch (e) {
    console.error(`scraping failed for the following reason: ${e.message}`);
  }
})();
