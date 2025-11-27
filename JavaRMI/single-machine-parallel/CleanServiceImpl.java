import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;

public class CleanServiceImpl extends UnicastRemoteObject implements CleanService {

    public CleanServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public String cleanText(String rawText) throws RemoteException {
        System.out.println("Clean Service: Received raw text.");
        
        // Equivalent to Python: text.lower()
        String text = rawText.toLowerCase();
        
        // Equivalent to Python: re.sub(r"[^a-z0-9\s']+", '', text)
        text = text.replaceAll("[^a-z0-9\\s']+", "");
        
        // Equivalent to Python: re.sub(r'\s+', ' ', text).strip()
        text = text.replaceAll("\\s+", " ").trim();
        
        System.out.println("Clean Service: Text cleaned.");
        return text;
    }
}