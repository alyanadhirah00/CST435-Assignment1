package services;
import common.TokenizeService;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TokenizeServiceImpl extends UnicastRemoteObject implements TokenizeService {

    public TokenizeServiceImpl() throws RemoteException { super(); }

    @Override
    public List<String> tokenize(String cleanText) throws RemoteException {
        System.out.println("Tokenize Service: Received text.");
        List<String> tokens = new ArrayList<>();
        Pattern p = Pattern.compile("[\\w']+");
        Matcher m = p.matcher(cleanText);
        while (m.find()) {
            tokens.add(m.group());
        }
        System.out.println("Tokenize Service: Split into " + tokens.size() + " tokens.");
        return tokens;
    }

    public static void main(String[] args) {
        try {
            System.setProperty("java.rmi.server.hostname", "service-tokenize");
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("TokenizeService", new TokenizeServiceImpl());
            System.out.println("Tokenize Service ready on port 1099");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}