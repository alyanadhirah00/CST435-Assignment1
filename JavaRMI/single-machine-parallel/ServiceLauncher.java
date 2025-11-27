import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class ServiceLauncher {
    public static void main(String[] args) {
        try {
            // Start the RMI Registry on port 1099
            Registry registry = LocateRegistry.createRegistry(1099);
            System.out.println("--- RMI Registry started on port 1099 ---");

            // Instantiate Services
            CleanService clean = new CleanServiceImpl();
            TokenizeService tokenize = new TokenizeServiceImpl();
            SentimentService sentiment = new SentimentServiceImpl();
            ReportService report = new ReportServiceImpl();

            // Bind them to the registry
            registry.rebind("CleanService", clean);
            registry.rebind("TokenizeService", tokenize);
            registry.rebind("SentimentService", sentiment);
            registry.rebind("ReportService", report);

            System.out.println("Service A (Clean) is ready.");
            System.out.println("Service B (Tokenize) is ready.");
            System.out.println("Service C (Sentiment) is ready.");
            System.out.println("Service D (Report) is ready.");

        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}