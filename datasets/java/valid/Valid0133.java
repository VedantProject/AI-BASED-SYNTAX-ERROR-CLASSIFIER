public class Valid0133 {
    private int value;
    
    public Valid0133(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0133 obj = new Valid0133(42);
        System.out.println("Value: " + obj.getValue());
    }
}
