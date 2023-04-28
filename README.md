# Stonks

A simple all-in-one financial dashboard tailored towards israeli banks and institutions.

## Features

- [x] Raw API
- [x] SQLite DB (for easy access from Grafana)
- [x] Multi-tenancy (users & auth)
- [ ] Web UI
  - [ ] Predictions/Projections

## Data sources

- [ ] Bank accounts and transactions (עו"ש) (using [eshaham/israeli-bank-scrapers](https://github.com/eshaham/israeli-bank-scrapers))
- [x] Gemel / Gemel-Le-Hashkaa accounts (from [Swiftness (המסלקה הפנסיונית)](https://www.swiftness.co.il/))
- [x] Pension accounts (from [Swiftness (המסלקה הפנסיונית)](https://www.swiftness.co.il/))
- [x] Insurance plans (from [Swiftness (המסלקה הפנסיונית)](https://www.swiftness.co.il/))
- [ ] Stock prices (from [Yahoo Finance](https://finance.yahoo.com/))

## Usage

- Modify `CREDS_DIR`, `UNPROCESSED_DIR`, and `PROCESSED_DIR` in `stonks/gmail_fetcher/__main__.py`
  - Create `$CREDS_DIR/credentials.json` using [this tutorial](https://developers.google.com/gmail/api/quickstart/python)
- Modify `DATABASES.default.NAME` in `stonks_app/settings.py`
- Install poetry
  - `apt install python3-poetry`
- Install dependencies
  - `poetry install`
- Open a development shell
  - `poetry shell`
  - Create the DB
    - `python manage.py migrate`
  - Create a superuser
    - `python manage.py createsuperuser`
  - Start a dev server
    - `python manage.py runserver`
  - Fetch zips from gmail (run while the dev server is running)
    - `python stonks/gmail_fetcher`
- Try the example [grafana dashboard](grafana_dashboards/example_gemels.json) (accesses the sqlite db directly)
