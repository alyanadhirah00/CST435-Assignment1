package common;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface SentimentService extends Remote {
    String analyzeSentiment(List<String> tokens) throws RemoteException;
}