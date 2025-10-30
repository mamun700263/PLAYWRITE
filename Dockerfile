# ---------- Base layer ----------
FROM python:3.13-slim

# Disable Python output buffering (so logs show instantly)
ENV PYTHONUNBUFFERED=1

# ---------- Install system dependencies ----------
# RUN apt-get update && apt-get install -y \
#     curl \
#     wget \
#     git \
#     libnss3 \
#     libatk1.0-0 \
#     libatk-bridge2.0-0 \
#     libcups2 \
#     libdrm2 \
#     libxkbcommon0 \
#     libxcomposite1 \
#     libxrandr2 \
#     libxdamage1 \
#     libgbm1 \
#     libpango-1.0-0 \
#     libasound2 \
#     fonts-liberation \
#     && rm -rf /var/lib/apt/lists/*

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Copy dependency list ----------
COPY requirements.txt .

# ---------- Install Python dependencies ----------
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Copy source code ----------
COPY . .

# ---------- Install browsers inside container ----------
# Install Chromium dependencies manually (Debian 13-compatible)
RUN apt-get update && apt-get install -y \
    fonts-unifont \
    fonts-ubuntu \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libdrm2 \
    libgbm1 \
    libxshmfence1 \
    xvfb \
    && playwright install chromium \
    && rm -rf /var/lib/apt/lists/*


# ---------- Command to start scraper ----------
CMD ["python3", "app/runner.py"]
