import common.SentimentService;
import common.ReportService;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SentimentServiceImpl extends UnicastRemoteObject implements SentimentService {
    
    private static final Map<String, Integer> LEXICON = new HashMap<>();
    static {
        LEXICON.put("love", 2); LEXICON.put("great", 2); LEXICON.put("good", 1);
        LEXICON.put("awesome", 3); LEXICON.put("excellent", 3); LEXICON.put("nice", 1);
        LEXICON.put("best", 2); 
        LEXICON.put("hate", -2); LEXICON.put("bad", -1); LEXICON.put("terrible", -3);
        LEXICON.put("awful", -3); LEXICON.put("worst", -2); LEXICON.put("poor", -1);
    }

    public SentimentServiceImpl() throws java.rmi.RemoteException { super(); }

    @Override
    public String processSentiment(List<String> tokens, String filename) throws java.rmi.RemoteException {
        System.out.println("Sentiment Service: Processing '" + filename + "'");
        
        // 1. Do the work
        int score = 0;
        for (String t : tokens) score += LEXICON.getOrDefault(t.toLowerCase(), 0);
        String sentiment = (score > 0) ? "Positive" : (score < 0 ? "Negative" : "Neutral");

        // 2. Call the NEXT service (Report)
        try {
            Registry registry = LocateRegistry.getRegistry("service-report", 1099);
            ReportService stub = (ReportService) registry.lookup("ReportService");
            
            return stub.logReport(filename, sentiment); // This returns the final string
            
        } catch (Exception e) {
            System.err.println("Sentiment Service Failed to call Report: " + e.getMessage());
            throw new java.rmi.RemoteException("Pipeline broken at Sentiment Service", e);
        }
    }

    public static void main(String[] args) {
        try {
            System.setProperty("java.rmi.server.hostname", "service-sentiment");
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("SentimentService", new SentimentServiceImpl());
            System.out.println("Sentiment Service (Pipeline Mode) ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}