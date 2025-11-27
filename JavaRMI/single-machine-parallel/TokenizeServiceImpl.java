import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TokenizeServiceImpl extends UnicastRemoteObject implements TokenizeService {

    public TokenizeServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public List<String> tokenize(String cleanText) throws RemoteException {
        System.out.println("Tokenize Service: Received text.");
        
        List<String> tokens = new ArrayList<>();
        
        // Equivalent to Python: re.findall(r"[\w']+", clean_text)
        Pattern pattern = Pattern.compile("[\\w']+");
        Matcher matcher = pattern.matcher(cleanText);
        
        while (matcher.find()) {
            tokens.add(matcher.group());
        }
        
        System.out.println("Tokenize Service: Split text into " + tokens.size() + " tokens.");
        return tokens;
    }
}