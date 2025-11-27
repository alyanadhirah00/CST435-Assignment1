package services;

import common.SentimentService;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SentimentServiceImpl extends UnicastRemoteObject implements SentimentService {
    
    // lexicon dictionary
    private static final Map<String, Integer> LEXICON = new HashMap<>();

    static {
        LEXICON.put("love", 2); LEXICON.put("great", 2); LEXICON.put("good", 1);
        LEXICON.put("awesome", 3); LEXICON.put("excellent", 3); LEXICON.put("nice", 1);
        LEXICON.put("best", 2); LEXICON.put("hate", -2); LEXICON.put("bad", -1);
        LEXICON.put("terrible", -3); LEXICON.put("awful", -3); LEXICON.put("worst", -2);
        LEXICON.put("poor", -1);
    }

    public SentimentServiceImpl() throws RemoteException { 
        super(); 
    }

    @Override
    public String analyzeSentiment(List<String> tokens) throws RemoteException {
        System.out.println("Sentiment Service: Analyzing " + tokens.size() + " tokens.");
        int score = 0;
        // Handle potential null list
        if (tokens != null) {
            for (String t : tokens) {
                score += LEXICON.getOrDefault(t.toLowerCase(), 0);
            }
        }
        
        if (score > 0) return "Positive";
        if (score < 0) return "Negative";
        return "Neutral";
    }

    public static void main(String[] args) {
        try {
            System.out.println("--- Starting Sentiment Service ---");
            
            // 1. Set Hostname for Docker
            System.setProperty("java.rmi.server.hostname", "service-sentiment");
            
            // 2. Create Registry
            Registry registry = LocateRegistry.createRegistry(1099);
            
            // 3. Bind Object
            SentimentServiceImpl service = new SentimentServiceImpl();
            registry.rebind("SentimentService", service);
            
            System.out.println("Sentiment Service ready on port 1099");
            
            // 4. Keep server alive (Explicit wait to prevent exit)
            Object lock = new Object();
            synchronized (lock) {
                lock.wait();
            }
            
        } catch (Exception e) {
            System.err.println("Sentiment Service CRASHED:");
            e.printStackTrace();
        }
    }
}