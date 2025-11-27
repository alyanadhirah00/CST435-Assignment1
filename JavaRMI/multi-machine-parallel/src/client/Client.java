package client;

import common.*;
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

    private static final String CLEAN_HOST = "service-clean";
    private static final String TOKENIZE_HOST = "service-tokenize";
    private static final String SENTIMENT_HOST = "service-sentiment";
    private static final String REPORT_HOST = "service-report";
    private static final String TEXTFILE_DIR = "textfile";

    // --- OPTIMIZATION: Cache the Stubs so we don't reconnect every time ---
    private static CleanService stubClean;
    private static TokenizeService stubToken;
    private static SentimentService stubSent;
    private static ReportService stubRep;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Client started. Waiting 5s for services...");
        Thread.sleep(5000); 

        // --- OPTIMIZATION: Initialize connections ONCE before processing ---
        try {
            System.out.println("--- Connecting to Services... ---");
            Registry regClean = LocateRegistry.getRegistry(CLEAN_HOST, 1099);
            stubClean = (CleanService) regClean.lookup("CleanService");

            Registry regToken = LocateRegistry.getRegistry(TOKENIZE_HOST, 1099);
            stubToken = (TokenizeService) regToken.lookup("TokenizeService");

            Registry regSent = LocateRegistry.getRegistry(SENTIMENT_HOST, 1099);
            stubSent = (SentimentService) regSent.lookup("SentimentService");

            Registry regRep = LocateRegistry.getRegistry(REPORT_HOST, 1099);
            stubRep = (ReportService) regRep.lookup("ReportService");
            System.out.println("--- Connected to all services successfully ---");
        } catch (Exception e) {
            System.err.println("CRITICAL ERROR: Could not connect to services.");
            e.printStackTrace();
            return;
        }

        File dir = new File(TEXTFILE_DIR);
        File[] files = dir.listFiles((d, name) -> name.endsWith(".txt"));

        if (files == null || files.length == 0) {
            System.out.println("Error: No .txt files found in '" + TEXTFILE_DIR + "'.");
            return;
        }

        Arrays.sort(files, Comparator.comparing(File::getName));

        System.out.println("--- Client: Processing " + files.length + " files in parallel... ---");

        // --- Start Total Timer ---
        long totalStartTime = System.nanoTime();

        // Increase thread pool slightly to ensure CPU saturation if needed
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

        // --- Stop Total Timer ---
        long totalEndTime = System.nanoTime();
        
        double totalTimeSec = (totalEndTime - totalStartTime) / 1_000_000_000.0;
        double throughput = files.length / totalTimeSec;

        // --- Summary Output ---
        System.out.println("----Summary for Multi Container Parallel----");
        System.out.printf("Total execution time: %.3f seconds\n", totalTimeSec);
        System.out.printf("Throughput: %.2f files/sec\n", throughput);
        System.out.println("Results stored in 'reports/results.csv'");
        System.out.println("---------------------------------");
        System.out.println();
        System.out.println("=================================");
        System.out.println("All servers and client finished!");
        System.out.println("Check results in 'reports/results.csv'");
    }

    private static String processPipeline(File file) {
        String filename = file.getName();
        long fileStartTime = System.nanoTime();
        String sentiment = "Error";

        System.out.println("[Client] Processing '" + filename + "'...");

        try {
            String content = new String(Files.readAllBytes(file.toPath()));

            // --- Step 1: Clean (Using Cached Stub) ---
            String cleanText = stubClean.cleanText(content);
            System.out.println(" > '" + filename + "': Step 1 Clean OK");

            // --- Step 2: Tokenize (Using Cached Stub) ---
            List<String> tokens = stubToken.tokenize(cleanText);
            System.out.println(" > '" + filename + "': Step 2 Tokenize OK (" + tokens.size() + " tokens)");

            // --- Step 3: Sentiment (Using Cached Stub) ---
            sentiment = stubSent.analyzeSentiment(tokens);
            System.out.println(" > '" + filename + "': Step 3 Sentiment OK (" + sentiment + ")");

            // --- Step 4: Report (Using Cached Stub) ---
            String responseMsg = stubRep.logReport(filename, sentiment);
            System.out.println(" > '" + filename + "': Step 4 Report OK (" + responseMsg + ")");

        } catch (Exception e) {
            long failTime = System.nanoTime();
            double failDuration = (failTime - fileStartTime) / 1_000_000_000.0;
            System.out.println("[Client] ERROR processing '" + filename + "': " + e.getMessage());
            return String.format("File: %s -> Error | Processing time: %.3f seconds", filename, failDuration);
        }

        long fileEndTime = System.nanoTime();
        double durationSec = (fileEndTime - fileStartTime) / 1_000_000_000.0;

        return String.format("File: %s -> %-8s | Processing time: %.3f seconds", filename, sentiment, durationSec);
    }
}