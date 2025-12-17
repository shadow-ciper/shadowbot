#!/bin/bash
# CipherBot2 MCP Server - Clean startup (NO ECHO STATEMENTS!)

exec docker run -i --rm \
  --cap-add=NET_RAW \
  --cap-add=NET_ADMIN \
  -v "${HOME}:/host:rw" \
  cipherbot2-mcp-server \
  /opt/cipherbot-venv/bin/python3 /app/mcp_server.py
