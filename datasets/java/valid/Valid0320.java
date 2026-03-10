public class Valid0320 {
    private int value;
    
    public Valid0320(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0320 obj = new Valid0320(42);
        System.out.println("Value: " + obj.getValue());
    }
}
