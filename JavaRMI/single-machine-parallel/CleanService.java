import java.rmi.Remote;
import java.rmi.RemoteException;

public interface CleanService extends Remote {
    String cleanText(String rawText) throws RemoteException;
}