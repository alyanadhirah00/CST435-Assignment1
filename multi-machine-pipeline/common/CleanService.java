package common;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface CleanService extends Remote {
    // Returns the final report string (e.g., "Logged successfully")
    // It will block until the END of the pipeline.
    String processPipeline(String rawText, String filename) throws RemoteException;
}