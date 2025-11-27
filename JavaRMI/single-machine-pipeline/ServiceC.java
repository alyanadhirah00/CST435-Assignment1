import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ServiceC extends UnicastRemoteObject implements SentimentService {

    private static final Map<String, Integer> LEXICON = new HashMap<>();
    static {
        LEXICON.put("love", 2); LEXICON.put("great", 2); LEXICON.put("good", 1);
        LEXICON.put("awesome", 3); LEXICON.put("excellent", 3); LEXICON.put("nice", 1);
        LEXICON.put("best", 2); 
        LEXICON.put("hate", -2); LEXICON.put("bad", -1); LEXICON.put("terrible", -3);
        LEXICON.put("awful", -3); LEXICON.put("worst", -2); LEXICON.put("poor", -1);
    }

    public ServiceC() throws RemoteException { super(); }

    @Override
    public String analyzeSentiment(List<String> tokens) throws RemoteException {
        int score = 0;
        for (String t : tokens) {
            score += LEXICON.getOrDefault(t.toLowerCase(), 0);
        }
        if (score > 0) return "Positive";
        if (score < 0) return "Negative";
        return "Neutral";
    }

    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            registry.rebind("SentimentService", new ServiceC());
            System.out.println("Service C (Sentiment) is ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}