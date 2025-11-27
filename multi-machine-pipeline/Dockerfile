FROM eclipse-temurin:8-jdk

WORKDIR /app

# Copy source code
COPY . /app

# Compile common interfaces first.
# The "-d ." flag tells javac to put the compiled files in the root /app folder 
# (preserving the 'common' package structure).
RUN javac -d . common/*.java

# Compile services and client.
# We use "-cp ." to ensure they can find the 'common' classes.
# We use "-d ." to ensure the compiled .class files land in /app, 
# even though the .java files are in subfolders.
RUN javac -cp . -d . service-clean/*.java
RUN javac -cp . -d . service-tokenize/*.java
RUN javac -cp . -d . service-sentiment/*.java
RUN javac -cp . -d . service-report/*.java
RUN javac -cp . -d . client/*.java