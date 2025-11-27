package common;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface SentimentService extends Remote {
    String processSentiment(List<String> tokens, String filename) throws RemoteException;
}