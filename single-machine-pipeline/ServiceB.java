import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ServiceB extends UnicastRemoteObject implements TokenizeService {

    public ServiceB() throws RemoteException { super(); }

    @Override
    public List<String> tokenize(String cleanText) throws RemoteException {
        List<String> tokens = new ArrayList<>();
        Matcher m = Pattern.compile("[\\w']+").matcher(cleanText);
        while (m.find()) {
            tokens.add(m.group());
        }
        return tokens;
    }

    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            registry.rebind("TokenizeService", new ServiceB());
            System.out.println("Service B (Tokenize) is ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}