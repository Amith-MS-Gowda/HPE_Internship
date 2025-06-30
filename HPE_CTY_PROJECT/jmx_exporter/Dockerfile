FROM openjdk:8-jre-alpine

# Set environment variables
ENV JMX_EXPORTER_VERSION=0.16.1
ENV JMX_EXPORTER_HOME=/opt/jmx_exporter

# Create the directory for the JMX exporter
RUN mkdir -p $JMX_EXPORTER_HOME

# Install curl
RUN apk --no-cache add curl

# Download the JMX Exporter JAR file with retry mechanism
RUN curl -L --retry 5 https://github.com/prometheus/jmx_exporter/releases/download/v${JMX_EXPORTER_VERSION}/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar -o ${JMX_EXPORTER_HOME}/jmx_prometheus_javaagent.jar

# Expose the JMX Exporter port
EXPOSE 5556

# Run the JMX Exporter with Java
CMD ["java", "-jar", "/opt/jmx_exporter/jmx_prometheus_javaagent.jar", "5556", "/etc/jmx_exporter/config.yml"]
