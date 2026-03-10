public class Valid0061 {
    private int value;
    
    public Valid0061(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0061 obj = new Valid0061(42);
        System.out.println("Value: " + obj.getValue());
    }
}
