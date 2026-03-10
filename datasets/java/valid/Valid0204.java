public class Valid0204 {
    private int value;
    
    public Valid0204(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0204 obj = new Valid0204(42);
        System.out.println("Value: " + obj.getValue());
    }
}
