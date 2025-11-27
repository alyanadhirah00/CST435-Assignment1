import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;

public class ServiceA extends UnicastRemoteObject implements CleanService {

    public ServiceA() throws RemoteException { super(); }

    @Override
    public String cleanText(String rawText) throws RemoteException {
        // Logic: Lowercase and remove non-alphanumeric chars
        if (rawText == null) return "";
        String cleaned = rawText.toLowerCase().replaceAll("[^a-z0-9\\s']+", "");
        cleaned = cleaned.replaceAll("\\s+", " ").trim();
        return cleaned;
    }

    public static void main(String[] args) {
        try {
            // Service A starts the Registry
            try { LocateRegistry.createRegistry(1099); } catch (Exception e) {}
            
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            registry.rebind("CleanService", new ServiceA());
            System.out.println("Service A (Clean) is ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}