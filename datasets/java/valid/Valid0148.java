public class Valid0148 {
    private int value;
    
    public Valid0148(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0148 obj = new Valid0148(42);
        System.out.println("Value: " + obj.getValue());
    }
}
