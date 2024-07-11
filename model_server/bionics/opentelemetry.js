/*opentelemetry.js*/
// Require dependencies
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { ConsoleSpanExporter } = require('@opentelemetry/sdk-trace-node');
const { Resource } = require('@opentelemetry/resources');
const {
  OTLPTraceExporter,
} = require('@opentelemetry/exporter-trace-otlp-proto');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { diag, DiagConsoleLogger, DiagLogLevel } = require('@opentelemetry/api');
diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.DEBUG);
const {
  getNodeAutoInstrumentations,
} = require('@opentelemetry/auto-instrumentations-node');
const {
  PeriodicExportingMetricReader,
  ConsoleMetricExporter,
} = require('@opentelemetry/sdk-metrics');

// Use environment variables for the URL and service name
const otlpUrl = process.env.OTLP_URL;
const serviceName = process.env.SERVICE_NAME;

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: otlpUrl,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'bionics',
  }),
});

sdk.start();
