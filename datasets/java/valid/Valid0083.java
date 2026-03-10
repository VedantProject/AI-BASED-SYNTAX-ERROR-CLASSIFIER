public class Valid0083 {
    private int value;
    
    public Valid0083(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0083 obj = new Valid0083(42);
        System.out.println("Value: " + obj.getValue());
    }
}
