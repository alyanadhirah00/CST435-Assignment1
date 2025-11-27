import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
import java.io.*;

public class ReportServiceImpl extends UnicastRemoteObject implements ReportService {

    private static final String REPORTS_DIR = "reports";
    private static final String RESULTS_FILE = REPORTS_DIR + "/results.csv";
    
    // We keep the writer as a class variable so it stays open
    private PrintWriter writer; 

    public ReportServiceImpl() throws RemoteException {
        super();
        setupFile();
    }

    private void setupFile() {
        try {
            // 1. Ensure Directory Exists
            File dir = new File(REPORTS_DIR);
            if (!dir.exists()) {
                dir.mkdirs();
            }

            File file = new File(RESULTS_FILE);
            boolean isNewFile = !file.exists();

            // 2. Open the file ONCE with 'append = true'
            // BufferedWriter improves performance by buffering characters
            FileWriter fw = new FileWriter(file, true);
            BufferedWriter bw = new BufferedWriter(fw);
            writer = new PrintWriter(bw, true); // 'true' enables auto-flush

            // 3. Write Header only if it's a new file
            if (isNewFile) {
                writer.println("filename,sentiment");
            }
            
            System.out.println("Report Service: File opened successfully.");

        } catch (IOException e) {
            System.err.println("Report Service Error: Could not open file.");
            e.printStackTrace();
        }
    }

    @Override
    public String logReport(String filename, String sentiment) throws RemoteException {
        // Logging to console is fast, so we can keep this
        System.out.println("Report Service: Logging " + filename + " -> " + sentiment);
        
        if (writer != null) {
            // We still need 'synchronized' to ensure lines don't get mixed up
            // BUT, writing to an already open RAM buffer is extremely fast (microseconds)
            synchronized (this) {
                writer.println(filename + "," + sentiment);
            }
            return "Logged " + filename + " as " + sentiment;
        } else {
            return "Error: Writer not initialized";
        }
    }
}