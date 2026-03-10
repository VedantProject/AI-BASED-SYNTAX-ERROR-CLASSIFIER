public class Valid0381 {
    private int value;
    
    public Valid0381(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0381 obj = new Valid0381(42);
        System.out.println("Value: " + obj.getValue());
    }
}
