import xmlrpc.client
import time

# Service addresses
CLEAN_SERVICE_ADDR = 'http://service-clean:50051'
TOKENIZE_SERVICE_ADDR = 'http://service-tokenize:50052'
SENTIMENT_SERVICE_ADDR = 'http://service-sentiment:50053'
REPORT_SERVICE_ADDR = 'http://service-report:50054'

textfiles = ["textfile/review1.txt", "textfile/review2.txt", "textfile/review3.txt"]

file_times = []
total_start = time.time()

print("=" * 60)
print("🚀 RPC Container Pipeline Demo: Text Processing Workflow")
print("=" * 60)
print("Processing text files through a multi-service pipeline:")
print("1. Clean Service: Text cleaning and preprocessing")
print("2. Tokenize Service: Token extraction")
print("3. Sentiment Service: Sentiment analysis")
print("4. Report Service: Results logging")
print("-" * 60)

# Create proxies with allow_none=True
proxy_clean = xmlrpc.client.ServerProxy(CLEAN_SERVICE_ADDR, allow_none=True)
proxy_tokenize = xmlrpc.client.ServerProxy(TOKENIZE_SERVICE_ADDR, allow_none=True)
proxy_sentiment = xmlrpc.client.ServerProxy(SENTIMENT_SERVICE_ADDR, allow_none=True)
proxy_report = xmlrpc.client.ServerProxy(REPORT_SERVICE_ADDR, allow_none=True)

for i, filepath in enumerate(textfiles, 1):
    print(f"\n📄 Processing File {i}/{len(textfiles)}: {filepath}")
    print("-" * 40)
    start = time.time()

    # Read raw text
    with open(filepath, 'r') as f:
        raw_text = f.read()

    # Step 1: Clean
    print("📤 Sending to Clean Service...")
    cleaned_text = proxy_clean.Process(raw_text, filepath)
    if cleaned_text is None:
        cleaned_text = ""
    print("✅ Clean Service completed")

    # Step 2: Tokenize
    print("🔹 Sending to Tokenize Service...")
    tokens = proxy_tokenize.Process(cleaned_text, filepath)
    if tokens is None:
        tokens = []
    print(f"✅ Tokenize Service completed: {tokens[:5]}{'...' if len(tokens)>5 else ''}")

    # Step 3: Sentiment
    print("🔹 Sending to Sentiment Service...")
    sentiment = proxy_sentiment.Process(cleaned_text, filepath)
    if sentiment is None:
        sentiment = "Neutral"
    print(f"✅ Sentiment Service completed: {sentiment}")

    # Step 4: Report
    print("🔹 Sending to Report Service...")
    proxy_report.Process(filepath, sentiment)
    print("✅ Report Service completed")

    end = time.time()
    processing_time = end - start
    print(f"🕒 Completed processing for {filepath} (Time: {processing_time:.4f}s)")
    file_times.append(processing_time)

total_end = time.time()

# Summary
print("\n" + "=" * 60)
print("📊 Detailed Processing Summary (Multi-Container Pipeline)")
print("=" * 60)
print(f"{'File':<20} {'Time (s)':<10} {'Throughput (files/sec)':<20}")
print("-" * 50)
for f, t in zip(textfiles, file_times):
    throughput = 1/t if t>0 else 0
    print(f"{f:<20} {t:<10.4f} {throughput:<20.2f}")

total_time = total_end - total_start
avg_throughput = len(textfiles)/total_time
print("-" * 50)
print(f"{'Total files processed:':<30} {len(textfiles)}")
print(f"{'Total execution time:':<30} {total_time:.4f}s")
print(f"{'Average throughput:':<30} {avg_throughput:.2f} files/sec")
print("=" * 60)
print("🎉 Demo completed! Check reports/results.csv for detailed results.")
print("=" * 60)
