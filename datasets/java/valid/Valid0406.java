public class Valid0406 {
    private int value;
    
    public Valid0406(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0406 obj = new Valid0406(42);
        System.out.println("Value: " + obj.getValue());
    }
}
