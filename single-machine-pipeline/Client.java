import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.File;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class Client {

    private static final String CLEAN_HOST = "localhost";
    private static final String TOKENIZE_HOST = "localhost";
    private static final String SENTIMENT_HOST = "localhost";
    private static final String REPORT_HOST = "localhost";
    
    private static final String TEXTFILE_DIR = "textfile";

    public static void main(String[] args) throws InterruptedException {
        // Optional: Keep this if you need startup time, or remove to match screenshot exactly
        // System.out.println("--- Client: Waiting 5s for services to start... ---");
        Thread.sleep(5000); 

        File dir = new File(TEXTFILE_DIR);
        if (!dir.exists() || dir.listFiles() == null) {
            System.out.println("Error: No files found in " + TEXTFILE_DIR);
            return;
        }

        File[] files = dir.listFiles((d, name) -> name.endsWith(".txt"));
        Arrays.sort(files, Comparator.comparing(File::getName));

        // --- Start Total Timer ---
        long totalStartTime = System.nanoTime();

        // --- SEQUENTIAL LOOP ---
        for (File f : files) {
            String result = processPipeline(f);
            System.out.println(result);
        }

        // --- Stop Total Timer ---
        long totalEndTime = System.nanoTime();
        
        double totalTimeSec = (totalEndTime - totalStartTime) / 1_000_000_000.0;
        double throughput = files.length / totalTimeSec;

        // --- Print Summary (Exact Screenshot Format) ---
        System.out.println("-------Summary for Local Machine Pipeline-------");
        System.out.printf("Total execution time: %.3f seconds\n", totalTimeSec);
        System.out.printf("Throughput: %.2f files/sec\n", throughput);
        System.out.println("Results stored in 'reports/results.csv'");
        System.out.println("------------------------------------------------------------");
        System.out.println();
        System.out.println("============================================================");
        System.out.println("All servers and client finished!");
        System.out.println("Check results in 'reports/results.csv'");
    }

    private static String processPipeline(File file) {
        String filename = file.getName();
        long fileStartTime = System.nanoTime();
        String sentiment = "Error";

        // Note: Intermediate "Processing..." logs removed to match screenshot
        try {
            String content = new String(Files.readAllBytes(file.toPath()));

            // Step 1: Clean
            Registry regClean = LocateRegistry.getRegistry(CLEAN_HOST, 1099);
            CleanService stubClean = (CleanService) regClean.lookup("CleanService");
            String cleanText = stubClean.cleanText(content);

            // Step 2: Tokenize
            Registry regToken = LocateRegistry.getRegistry(TOKENIZE_HOST, 1099);
            TokenizeService stubToken = (TokenizeService) regToken.lookup("TokenizeService");
            List<String> tokens = stubToken.tokenize(cleanText);

            // Step 3: Sentiment
            Registry regSent = LocateRegistry.getRegistry(SENTIMENT_HOST, 1099);
            SentimentService stubSent = (SentimentService) regSent.lookup("SentimentService");
            sentiment = stubSent.analyzeSentiment(tokens);

            // Step 4: Report
            Registry regRep = LocateRegistry.getRegistry(REPORT_HOST, 1099);
            ReportService stubRep = (ReportService) regRep.lookup("ReportService");
            stubRep.logReport(filename, sentiment);

        } catch (Exception e) {
            // In case of error, formatting matches the success line roughly
            long failTime = System.nanoTime();
            double failDuration = (failTime - fileStartTime) / 1_000_000_000.0;
            return String.format("File: %s -> Error | Processing time: %.3f seconds", filename, failDuration);
        }

        long fileEndTime = System.nanoTime();
        double durationSec = (fileEndTime - fileStartTime) / 1_000_000_000.0;

        // Exact Format: "File: review1.txt -> Neutral | Processing time: 0.475 seconds"
        return String.format("File: %s -> %-8s | Processing time: %.3f seconds", filename, sentiment, durationSec);
    }
}