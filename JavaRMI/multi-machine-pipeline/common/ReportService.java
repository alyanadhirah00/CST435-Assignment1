package common;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ReportService extends Remote {
    // Returns a status message
    String logReport(String filename, String sentiment) throws RemoteException;
}