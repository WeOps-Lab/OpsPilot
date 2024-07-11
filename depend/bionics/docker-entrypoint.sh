#!/bin/bash
# Check if the ENABLE_OTLP is set to true
if [ "${ENABLE_OTEL}" = "true" ]
then
    echo "Starting with OpenTelemetry instrumentation..."
    yarn start-ot
else
    yarn start
fi