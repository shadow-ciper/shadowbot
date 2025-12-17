FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Update + essential tools
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    whatweb \
    nikto \
    ffuf \
    gobuster \
    dirb \
    wfuzz \
    sqlmap \
    nuclei \
    sudo \
    && apt clean

# Python venv
RUN python3 -m venv /opt/cipherbot-venv
COPY requirements.txt /opt/requirements.txt
RUN /opt/cipherbot-venv/bin/pip install --upgrade pip && \
    /opt/cipherbot-venv/bin/pip install -r /opt/requirements.txt

# Copy server
WORKDIR /app
COPY mcp_server.py /app/
RUN chmod +x /app/mcp_server.py

# Create mount point for host filesystem access
RUN mkdir -p /host

# RUNNING AS ROOT - No user restrictions, full privileges
# This eliminates ALL permission issues

CMD ["/opt/cipherbot-venv/bin/python3", "/app/mcp_server.py"]
