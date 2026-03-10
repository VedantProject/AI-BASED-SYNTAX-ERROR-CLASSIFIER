public class Valid0202 {
    private int value;
    
    public Valid0202(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0202 obj = new Valid0202(42);
        System.out.println("Value: " + obj.getValue());
    }
}
