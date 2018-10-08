import java.util.HashSet;
import java.util.TreeMap;

public class Util {
    public static String findAttribute(TreeMap<String, String> attributes, String key){
        if(attributes.containsKey(key)){
            return attributes.get(key);
        }
        else {
            return "Not found";
        }
    }
}
