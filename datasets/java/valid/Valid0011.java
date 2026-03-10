public class Valid0011 {
    private int value;
    
    public Valid0011(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0011 obj = new Valid0011(42);
        System.out.println("Value: " + obj.getValue());
    }
}
