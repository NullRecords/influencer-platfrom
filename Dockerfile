FROM python:3.8.1-slim-buster

# Add user that will be used in the container.
RUN useradd wagtail

# Ports used by the container.
EXPOSE 8000 8443 10000/udp 3000

# Set environment variables.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail, Django, and other components.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    python3-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    curl \
    openjdk-11-jre-headless \
 && rm -rf /var/lib/apt/lists/*

# Install the application server and project dependencies.
RUN pip install "gunicorn==20.0.4"
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install Metabase.
RUN curl -o /metabase.jar https://downloads.metabase.com/v0.46.6/metabase.jar

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Install Jitsi dependencies.
RUN apt-get update && apt-get install -y \
    nginx \
    prosody \
    jicofo \
    jitsi-videobridge2 \
 && rm -rf /var/lib/apt/lists/*

# Configure Jitsi Meet.
RUN mkdir -p /etc/jitsi && \
    echo "Configuring Jitsi..." > /etc/jitsi/README

# Use user "wagtail" to run the Django server.
USER wagtail

# Start services in a single container.
CMD set -xe; \
    python manage.py migrate --noinput; \
    gunicorn mysite.wsgi:application & \
    java -jar /metabase.jar & \
    service nginx start && \
    service prosody start && \
    service jicofo start && \
    service jitsi-videobridge2 start && \
    tail -f /dev/null
