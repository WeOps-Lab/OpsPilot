#!/bin/bash
# Set default password if SALTAPI_PASSWORD not provided
DEFAULT_SALTAPI_PASSWORD="saltapi"
SALTAPI_PASSWORD=${SALTAPI_PASSWORD:-$DEFAULT_SALTAPI_PASSWORD}

# Change password for saltapi user
echo "saltapi:$SALTAPI_PASSWORD" | chpasswd

# Run command passed into docker run
exec "$@"