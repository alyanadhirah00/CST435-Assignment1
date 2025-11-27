FROM eclipse-temurin:8-jdk


WORKDIR /app

# Copy source code
COPY src /app/src
COPY textfile /app/textfile

# Create output directory for classes
RUN mkdir -p /app/bin

# Compile all Java files
RUN javac -d /app/bin src/common/*.java src/services/*.java src/client/*.java

# Create report directory
RUN mkdir -p /app/reports

# Set classpath
ENV CLASSPATH=/app/bin

# Entrypoint script to run the correct class based on ENV variable
CMD ["sh", "-c", "java $SERVICE_CLASS"]