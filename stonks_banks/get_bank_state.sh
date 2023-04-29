#!/usr/bin/env bash
export TZ='Asia/Jerusalem'
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# shellcheck disable=SC2002
cat /srv/stonks/bank_creds.json | docker run -i --rm -v /srv/stonks/dumper:/code puppeteer-aarch64:latest node /code/index.js > /srv/stonks/dumps/"BankDump_${DATE}".json.tmp
mv /srv/stonks/dumps/"BankDump_${DATE}".json.tmp /srv/stonks/dumps/"BankDump_${DATE}".json
