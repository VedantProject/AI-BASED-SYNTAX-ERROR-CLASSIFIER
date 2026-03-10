public class Valid0025 {
    private int value;
    
    public Valid0025(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0025 obj = new Valid0025(42);
        System.out.println("Value: " + obj.getValue());
    }
}
