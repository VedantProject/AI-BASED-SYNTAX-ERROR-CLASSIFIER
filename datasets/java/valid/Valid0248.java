public class Valid0248 {
    private int value;
    
    public Valid0248(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0248 obj = new Valid0248(42);
        System.out.println("Value: " + obj.getValue());
    }
}
