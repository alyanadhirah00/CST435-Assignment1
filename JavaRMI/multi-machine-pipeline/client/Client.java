import common.CleanService;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.io.File;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.*;

public class Client {

    private static final String CLEAN_HOST = "service-clean";
    private static final String TEXTFILE_DIR = "textfile";

    public static void main(String[] args) throws InterruptedException {
        // Wait for services to start
        Thread.sleep(5000); 

        File dir = new File(TEXTFILE_DIR);
        File[] files = dir.listFiles((d, name) -> name.endsWith(".txt"));

        if (files == null || files.length == 0) return;
        Arrays.sort(files, Comparator.comparing(File::getName));

        // Use ExecutorService to manage the parallel requests
        ExecutorService executor = Executors.newFixedThreadPool(5);
        List<Future<String>> futures = new ArrayList<>();

        long totalStartTime = System.nanoTime();

        // Submit all files to the pipeline
        for (File f : files) {
            futures.add(executor.submit(() -> processPipeline(f)));
        }

        // Print results line-by-line as they finish to match the screenshot body
        for (Future<String> future : futures) {
            try {
                System.out.println(future.get());
            } catch (Exception e) { e.printStackTrace(); }
        }

        executor.shutdown();
        long totalEndTime = System.nanoTime();
        
        double totalTimeSec = (totalEndTime - totalStartTime) / 1_000_000_000.0;
        double throughput = files.length / totalTimeSec;

        // --- UPDATED SUMMARY SECTION TO MATCH SCREENSHOT ---
        System.out.println("----Summary for Multi Container Parallel----");
        System.out.printf("Total execution time: %.3f seconds\n", totalTimeSec);
        System.out.printf("Throughput: %.2f files/sec\n", throughput);
        System.out.println("Results stored in 'reports/results.csv'");
        System.out.println("--------------------------------------------");
    }

    private static String processPipeline(File file) {
        String filename = file.getName();
        long start = System.nanoTime();

        try {
            String content = new String(Files.readAllBytes(file.toPath()), StandardCharsets.UTF_8);

            // Connect to the first service (Clean)
            // It will propagate the data to B -> C -> D and return the sentiment string
            Registry registry = LocateRegistry.getRegistry(CLEAN_HOST, 1099);
            CleanService stub = (CleanService) registry.lookup("CleanService");
            
            String sentiment = stub.processPipeline(content, filename);

            long end = System.nanoTime();
            double duration = (end - start) / 1_000_000_000.0;

            // Output format: "File: review1.txt -> Neutral | Processing time: 0.257 seconds"
            return String.format("File: %s -> %-7s | Processing time: %.3f seconds", filename, sentiment, duration);

        } catch (Exception e) {
            long end = System.nanoTime();
            return String.format("File: %s -> Error   | Processing time: %.3f seconds", filename, (end - start)/1e9);
        }
    }
}