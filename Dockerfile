FROM python:3.11

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
    fonts-liberation xdg-utils ffmpeg\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Keep the Whisper/Playwright caches under /app (owned by the non-root
# user created below) instead of root's home directory.
ENV HOME=/app \
    PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download the tiny Whisper model (one single RUN command)
RUN python -c "import whisper; print('Downloading Whisper tiny model...'); model = whisper.load_model('tiny'); print('Whisper tiny model downloaded successfully.')"

# Install browsers
RUN playwright install chromium

COPY . .

# Run as a non-root user. This image bundles Playwright/Chromium and
# PyTorch/Whisper -- both large, frequently-patched native dependency
# chains -- and docker-compose.yml bind-mounts host directories into the
# container, so root here would give a future RCE in either stack more
# than a disposable container filesystem to work with.
RUN groupadd --gid 1000 scraper && \
    useradd --uid 1000 --gid scraper --create-home scraper && \
    chown -R scraper:scraper /app
USER scraper

CMD ["python", "main.py"]