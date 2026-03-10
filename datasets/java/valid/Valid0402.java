public class Valid0402 {
    private int value;
    
    public Valid0402(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0402 obj = new Valid0402(42);
        System.out.println("Value: " + obj.getValue());
    }
}
