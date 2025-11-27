import common.CleanService;
import common.TokenizeService;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

public class CleanServiceImpl extends UnicastRemoteObject implements CleanService {

    public CleanServiceImpl() throws java.rmi.RemoteException { super(); }

    @Override
    public String processPipeline(String rawText, String filename) throws java.rmi.RemoteException {
        System.out.println("Clean Service: Processing '" + filename + "'");
        
        // 1. Do the work
        String cleanText = rawText.toLowerCase().replaceAll("[^a-z0-9\\s']+", "").replaceAll("\\s+", " ").trim();

        // 2. Call the NEXT service (Tokenize)
        try {
            // Note: We connect to "service-tokenize" (Docker container name)
            Registry registry = LocateRegistry.getRegistry("service-tokenize", 1099);
            TokenizeService stub = (TokenizeService) registry.lookup("TokenizeService");
            
            // Pass the baton
            return stub.processTokenize(cleanText, filename);
            
        } catch (Exception e) {
            System.err.println("Clean Service Failed to call Tokenize: " + e.getMessage());
            throw new java.rmi.RemoteException("Pipeline broken at Clean Service", e);
        }
    }

    public static void main(String[] args) {
        try {
            System.setProperty("java.rmi.server.hostname", "service-clean");
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("CleanService", new CleanServiceImpl());
            System.out.println("Clean Service (Pipeline Mode) ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}