import common.ReportService;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

public class ReportServiceImpl extends UnicastRemoteObject implements ReportService {
    
    private static final String FILE_PATH = "/app/reports/results.csv";

    public ReportServiceImpl() throws java.rmi.RemoteException { 
        super();
        try {
            File f = new File(FILE_PATH);
            f.getParentFile().mkdirs();
            if(!f.exists()) {
                try (PrintWriter pw = new PrintWriter(new FileWriter(f, true))) {
                    pw.println("filename,sentiment");
                }
            }
        } catch(Exception e) { e.printStackTrace(); }
    }

    @Override
    public String logReport(String filename, String sentiment) throws java.rmi.RemoteException {
        System.out.println("Report Service: Logging " + filename + " -> " + sentiment);
        try (PrintWriter pw = new PrintWriter(new FileWriter(FILE_PATH, true))) {
            pw.println(filename + "," + sentiment);
            
            // --- CHANGE HERE: Return the sentiment so the Client can print it ---
            return sentiment; 
            
        } catch (Exception e) {
            System.err.println("Report Error: " + e.getMessage());
            return "Error";
        }
    }

    public static void main(String[] args) {
        try {
            System.setProperty("java.rmi.server.hostname", "service-report");
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("ReportService", new ReportServiceImpl());
            System.out.println("Report Service (Pipeline Mode) ready.");
        } catch (Exception e) { e.printStackTrace(); }
    }
}