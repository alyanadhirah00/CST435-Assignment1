import xmlrpc.client
import time

class ForceCloseTransport(xmlrpc.client.Transport):
    def send_host(self, connection, host):
        connection.putheader("Connection", "close")
        super().send_host(connection, host)

proxy_clean = xmlrpc.client.ServerProxy("http://service-clean:50051/RPC2", transport=ForceCloseTransport())
proxy_tokenize = xmlrpc.client.ServerProxy("http://service-tokenize:50052/RPC2", transport=ForceCloseTransport())
proxy_sentiment = xmlrpc.client.ServerProxy("http://service-sentiment:50053/RPC2", transport=ForceCloseTransport())
proxy_report = xmlrpc.client.ServerProxy("http://service-report:50054/RPC2", transport=ForceCloseTransport())

textfiles = [
    "textfile/review1.txt",
    "textfile/review2.txt",
    "textfile/review3.txt"
]

def process_file(filepath):
    start = time.time()
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_text = proxy_clean.Process(raw_text, filepath)
    print(f"✅ Clean Service completed for {filepath}")

    tokens = proxy_tokenize.Process(cleaned_text, filepath)
    print(f"✅ Tokenize Service completed for {filepath}: {len(tokens)} tokens")

    sentiment = proxy_sentiment.Process(tokens, filepath)
    print(f"✅ Sentiment Service completed for {filepath}: {sentiment}")

    proxy_report.Process(filepath, sentiment)
    print(f"✅ Report Service completed for {filepath}")

    end = time.time()
    return filepath, end - start

if __name__ == "__main__":
    file_times = []
    total_start = time.time()

    print("=" * 60)
    print("🚀 RPC Container Sequential Demo")
    print("=" * 60)

    for filepath in textfiles:
        result = process_file(filepath)
        file_times.append(result)

    total_end = time.time()

    print("\n" + "=" * 60)
    print("📊 Sequential Processing Summary")
    print("=" * 60)
    for f, t in file_times:
        print(f"{f:<20} Time: {t:.4f}s Throughput: {1/t:.2f} files/sec")

    total_time = total_end - total_start
    avg_throughput = len(textfiles) / total_time
    print(f"Total execution time: {total_time:.4f}s, Average throughput: {avg_throughput:.2f} files/sec")
    print("=" * 60)
    print("🎉 Demo completed! Check reports/results.csv for detailed results.")
