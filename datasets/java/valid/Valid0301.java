public class Valid0301 {
    private int value;
    
    public Valid0301(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0301 obj = new Valid0301(42);
        System.out.println("Value: " + obj.getValue());
    }
}
