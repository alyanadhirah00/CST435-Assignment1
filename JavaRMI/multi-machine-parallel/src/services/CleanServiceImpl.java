package services;
import common.CleanService;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;

public class CleanServiceImpl extends UnicastRemoteObject implements CleanService {

    public CleanServiceImpl() throws RemoteException { super(); }

    @Override
    public String cleanText(String rawText) throws RemoteException {
        System.out.println("Clean Service: Received raw text.");
        if (rawText == null) return "";
        String text = rawText.toLowerCase();
        // Java regex equivalent to Python's [^a-z0-9\s']+
        text = text.replaceAll("[^a-z0-9\\s']+", "");
        text = text.replaceAll("\\s+", " ").trim();
        System.out.println("Clean Service: Text cleaned.");
        return text;
    }

    public static void main(String[] args) {
        try {
            // Crucial for Docker: Tell RMI the hostname of this container
            System.setProperty("java.rmi.server.hostname", "service-clean");
            
            CleanServiceImpl obj = new CleanServiceImpl();
            // Create registry on port 1099 (default RMI port)
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("CleanService", obj);
            System.out.println("Clean Service ready on port 1099");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}