public class Valid0112 {
    private int value;
    
    public Valid0112(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0112 obj = new Valid0112(42);
        System.out.println("Value: " + obj.getValue());
    }
}
