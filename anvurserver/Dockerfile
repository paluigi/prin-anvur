FROM python:3.12.6-bookworm

# Install necessary software
RUN apt-get update && \
    apt-get -y install ghostscript python3-tk curl

# Install supercronic
# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.32/supercronic-linux-arm64 \
    SUPERCRONIC=supercronic-linux-arm64 \
    SUPERCRONIC_SHA1SUM=7f89438e7810669d3e0ea488a202aaf422cc2fdf

RUN curl -fsSLO "$SUPERCRONIC_URL" \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "$SUPERCRONIC" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add crontab file
COPY crontab .

# Copy scripts and placeholders
COPY scraping_anvur.py .
COPY api.py .
COPY start.sh .
COPY data/info.md data/info.md

# Make scripts executable
RUN chmod +x scraping_anvur.py
RUN chmod +x api.py
RUN chmod +x start.sh

# Copy initial DB
COPY db.json .

# Start the startup script
CMD ["/app/start.sh"]
