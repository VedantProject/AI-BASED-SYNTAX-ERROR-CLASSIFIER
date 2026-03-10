public class Valid0414 {
    private int value;
    
    public Valid0414(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0414 obj = new Valid0414(42);
        System.out.println("Value: " + obj.getValue());
    }
}
