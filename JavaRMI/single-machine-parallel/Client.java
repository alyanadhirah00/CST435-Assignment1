import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.File;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.*;

public class Client {

    private static final String HOST = "localhost";
    private static final String TEXTFILE_DIR = "textfile";

    // --- OPTIMIZATION: Define Stubs as Static Variables ---
    // This allows us to look them up ONCE and reuse them 1000 times.
    private static CleanService cleanStub;
    private static TokenizeService tokenizeStub;
    private static SentimentService sentimentStub;
    private static ReportService reportStub;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("--- Client: Waiting 5s for services to start... ---");
        Thread.sleep(5000); 

        // --- OPTIMIZATION STEP 1: Connect to Services BEFORE the loop ---
        try {
            System.out.println("--- Client: Connecting to RMI Registry and caching stubs... ---");
            Registry registry = LocateRegistry.getRegistry(HOST, 1099);
            
            // Perform the lookup strictly ONCE
            cleanStub = (CleanService) registry.lookup("CleanService");
            tokenizeStub = (TokenizeService) registry.lookup("TokenizeService");
            sentimentStub = (SentimentService) registry.lookup("SentimentService");
            reportStub = (ReportService) registry.lookup("ReportService");
            
            System.out.println("--- Client: Connection Successful. Stubs cached. ---");
        } catch (Exception e) {
            System.err.println("CRITICAL ERROR: Could not connect to RMI Services.");
            e.printStackTrace();
            return;
        }

        File dir = new File(TEXTFILE_DIR);
        if (!dir.exists()) { System.out.println("Error: No directory."); return; }
        File[] files = dir.listFiles((d, name) -> name.endsWith(".txt"));
        if (files == null || files.length == 0) { System.out.println("Error: No files."); return; }

        Arrays.sort(files, Comparator.comparing(File::getName));

        System.out.println("--- Client: Processing " + files.length + " files in parallel... ---");
        System.out.println();

        long totalStartTime = System.nanoTime();

        // Increase threads slightly if your CPU handles it, but 5 is fine
        ExecutorService executor = Executors.newFixedThreadPool(5);
        List<Future<String>> futures = new ArrayList<>();

        for (File f : files) {
            futures.add(executor.submit(() -> processPipeline(f)));
        }

        for (Future<String> future : futures) {
            try {
                System.out.println(future.get());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        executor.shutdown();

        long totalEndTime = System.nanoTime();
        double totalTimeSec = (totalEndTime - totalStartTime) / 1_000_000_000.0;
        double throughput = (totalTimeSec > 0) ? files.length / totalTimeSec : 0;

        System.out.println("--------Summary for Local Machine Parallel-------");
        System.out.printf("Total execution time: %.3f seconds\n", totalTimeSec);
        System.out.printf("Throughput: %.2f files/sec\n", throughput);
        System.out.println("Results stored in 'reports/results.csv'");
        System.out.println("----------------------------------------------------------------------");
        System.out.println();
        System.out.println("======================================================================");
        System.out.println("All servers and client finished!");
        System.out.println("Check results in 'reports/results.csv'");
    }

    private static String processPipeline(File file) {
        String filename = file.getName();
        long fileStartTime = System.nanoTime();
        String sentiment = "Error";

        try {
            String content = new String(Files.readAllBytes(file.toPath()));

            // --- OPTIMIZATION STEP 2: Use the pre-loaded stubs ---
            // Direct method calls. No networking lookup overhead here.
            
            // Step 1
            String cleanText = cleanStub.cleanText(content);

            // Step 2
            List<String> tokens = tokenizeStub.tokenize(cleanText);

            // Step 3
            sentiment = sentimentStub.analyzeSentiment(tokens);

            // Step 4
            reportStub.logReport(filename, sentiment);

        } catch (Exception e) {
            long failTime = System.nanoTime();
            double failDuration = (failTime - fileStartTime) / 1_000_000_000.0;
            return String.format("File: %s -> Error    | Processing time: %.3f seconds", filename, failDuration);
        }

        long fileEndTime = System.nanoTime();
        double durationSec = (fileEndTime - fileStartTime) / 1_000_000_000.0;

        return String.format("File: %s -> %-8s | Processing time: %.3f seconds", filename, sentiment, durationSec);
    }
}