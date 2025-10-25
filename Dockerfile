# Use the same Python version you run locally (you used 3.13). If not available, fallback to 3.11.
FROM python:3.13-slim

# Non-root user creation for safety (optional but recommended)
ARG USER=appuser
ARG UID=1000
RUN addgroup --system $USER && adduser --system --ingroup $USER --uid $UID $USER

WORKDIR /app

# System deps (adjust if Playwright required). Keep image lean.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency spec first for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

# If you need Playwright in container, uncomment below:
# RUN pip install playwright
# RUN playwright install --with-deps chromium

# Copy code
COPY . /app

# Use non-root user
USER $USER

# Default command for web service (overridden by compose for run types)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
