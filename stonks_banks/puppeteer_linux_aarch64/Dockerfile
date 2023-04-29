FROM debian:stable-slim

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends chromium-driver curl ca-certificates &&  \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash &&  \
    apt-get install -y nodejs &&  \
    apt clean &&  \
    rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
