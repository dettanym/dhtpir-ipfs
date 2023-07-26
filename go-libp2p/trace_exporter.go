package main

import (
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/jaeger"
	"go.opentelemetry.io/otel/sdk/resource"
	"go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
	"log"
	"os"
)

// newResource returns a resource describing this application.
func newResource() *resource.Resource {
	r, _ := resource.Merge(
		resource.Default(),
		resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName("go-libp2p-kad-dht"),
			semconv.ServiceVersion("v0.1.0")),
	)
	return r
}

func InitTracing(url string) {
	l := log.New(os.Stdout, "", 0)

	// Create the Jaeger exporter
	exp, err := jaeger.New(jaeger.WithCollectorEndpoint(jaeger.WithEndpoint(url)))
	if err != nil {
		println("failed to initialize jaeger exporter: %w", err)
		l.Fatal(err)
	}
	bsp := trace.NewBatchSpanProcessor(exp)
	tp := trace.NewTracerProvider(
		trace.WithSpanProcessor(bsp),
		// trace.WithBatcher(exp),
		trace.WithResource(newResource()),
		trace.WithSampler(trace.AlwaysSample()),
	)

	otel.SetTracerProvider(tp)
	tp.Tracer("go-libp2p-kad-dht")
}
