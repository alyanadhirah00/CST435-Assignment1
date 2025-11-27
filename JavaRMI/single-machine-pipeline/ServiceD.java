import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class ServiceD extends UnicastRemoteObject implements ReportService {
    
    private static final String FILE_PATH = "reports/results.csv";

    public ServiceD() throws RemoteException {
        super();
        new File("reports").mkdirs();
        // Create header if not exists
        if (!new File(FILE_PATH).exists()) {
            try (FileWriter fw = new FileWriter(FILE_PATH)) {
                fw.write("filename,sentiment\n");
            } catch (IOException e) { e.printStackTrace(); }
        }
    }

    @Override
    public String logReport(String filename, String sentiment) throws RemoteException {
        try (FileWriter fw = new FileWriter(FILE_PATH, true)) {
            fw.write(filename + "," + sentiment + "\n");
            return "Logged"; // Return Success message to Client
        } catch (IOException e) {
            return "Write Failed";
        }
    }

    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            registry.rebind("ReportService", new ServiceD());
            System.out.println("Service D (Report) is ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}