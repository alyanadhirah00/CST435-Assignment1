package services;
import common.ReportService;
import java.rmi.server.UnicastRemoteObject;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class ReportServiceImpl extends UnicastRemoteObject implements ReportService {
    private static final String RESULTS_FILE = "/app/reports/results.csv";

    public ReportServiceImpl() throws RemoteException {
        super();
        try {
            File dir = new File("/app/reports");
            if (!dir.exists()) dir.mkdirs();
            File f = new File(RESULTS_FILE);
            if (!f.exists()) {
                try (PrintWriter pw = new PrintWriter(new FileWriter(f))) {
                    pw.println("filename,sentiment");
                }
            }
        } catch (IOException e) { e.printStackTrace(); }
    }

    // Synchronized to prevent concurrent write issues from multiple threads
    @Override
    public synchronized String logReport(String filename, String sentiment) throws RemoteException {
        System.out.println("Report Service: Logging " + filename + " -> " + sentiment);
        try (FileWriter fw = new FileWriter(RESULTS_FILE, true);
             PrintWriter pw = new PrintWriter(fw)) {
            pw.println(filename + "," + sentiment);
            return "Logged " + filename;
        } catch (IOException e) {
            e.printStackTrace();
            return "Error: " + e.getMessage();
        }
    }

    public static void main(String[] args) {
        try {
            System.setProperty("java.rmi.server.hostname", "service-report");
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("ReportService", new ReportServiceImpl());
            System.out.println("Report Service ready on port 1099");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}