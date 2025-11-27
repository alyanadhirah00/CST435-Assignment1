import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SentimentServiceImpl extends UnicastRemoteObject implements SentimentService {

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
        System.out.println("Sentiment Service: Received " + tokens.size() + " tokens.");
        
        int score = 0;
        for (String token : tokens) {
            score += LEXICON.getOrDefault(token.toLowerCase(), 0);
        }

        String sentiment = "Neutral";
        if (score > 0) sentiment = "Positive";
        else if (score < 0) sentiment = "Negative";

        System.out.println("Sentiment Service: Score: " + score + " -> " + sentiment);
        return sentiment;
    }
}