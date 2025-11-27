package common;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface TokenizeService extends Remote {
    String processTokenize(String cleanText, String filename) throws RemoteException;
}