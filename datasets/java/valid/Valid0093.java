public class Valid0093 {
    private int value;
    
    public Valid0093(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0093 obj = new Valid0093(42);
        System.out.println("Value: " + obj.getValue());
    }
}
