Run instructions:


1. Build and start everything (from project root):


```bash
docker compose up --build
```


2. To follow logs (live):


```bash
docker compose logs -f
```


3. If you change Python code and your Dockerfile uses COPY (not volume), rebuild:


```bash
docker compose down
docker compose up --build
```


4. To run client locally (WSL/host machine):


```bash
python3 client.py
```


Notes:
- The services are synchronous (they return results to client). The client calls Clean -> Tokenize -> Sentiment -> Report for each file, and the client runs multiple files in parallel using ThreadPoolExecutor.
- The reports folder is mounted so results.csv will appear on host in ./reports/results.csv


---