FROM python:3.11

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
    fonts-liberation xdg-utils ffmpeg\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download the tiny Whisper model (one single RUN command)
RUN python -c "import whisper; print('Downloading Whisper tiny model...'); model = whisper.load_model('tiny'); print('Whisper tiny model downloaded successfully.')"

# Install browsers
RUN playwright install chromium

COPY . .

CMD ["python", "main.py"]