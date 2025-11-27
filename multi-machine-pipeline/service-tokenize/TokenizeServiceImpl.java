import common.TokenizeService;
import common.SentimentService;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TokenizeServiceImpl extends UnicastRemoteObject implements TokenizeService {

    public TokenizeServiceImpl() throws java.rmi.RemoteException { super(); }

    @Override
    public String processTokenize(String cleanText, String filename) throws java.rmi.RemoteException {
        System.out.println("Tokenize Service: Processing '" + filename + "'");

        // 1. Do the work
        List<String> tokens = new ArrayList<>();
        Matcher m = Pattern.compile("[\\w']+").matcher(cleanText);
        while (m.find()) tokens.add(m.group());

        // 2. Call the NEXT service (Sentiment)
        try {
            Registry registry = LocateRegistry.getRegistry("service-sentiment", 1099);
            SentimentService stub = (SentimentService) registry.lookup("SentimentService");
            
            return stub.processSentiment(tokens, filename);
            
        } catch (Exception e) {
            System.err.println("Tokenize Service Failed to call Sentiment: " + e.getMessage());
            throw new java.rmi.RemoteException("Pipeline broken at Tokenize Service", e);
        }
    }

    public static void main(String[] args) {
        try {
            System.setProperty("java.rmi.server.hostname", "service-tokenize");
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("TokenizeService", new TokenizeServiceImpl());
            System.out.println("Tokenize Service (Pipeline Mode) ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}