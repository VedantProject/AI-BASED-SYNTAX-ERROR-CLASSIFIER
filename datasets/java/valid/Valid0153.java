public class Valid0153 {
    private int value;
    
    public Valid0153(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0153 obj = new Valid0153(42);
        System.out.println("Value: " + obj.getValue());
    }
}
