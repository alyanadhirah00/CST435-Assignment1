import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ReportService extends Remote {
    String logReport(String filename, String sentiment) throws RemoteException;
}