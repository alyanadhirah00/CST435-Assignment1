package common;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface TokenizeService extends Remote {
    List<String> tokenize(String cleanText) throws RemoteException;
}