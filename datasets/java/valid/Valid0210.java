public class Valid0210 {
    private int value;
    
    public Valid0210(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0210 obj = new Valid0210(42);
        System.out.println("Value: " + obj.getValue());
    }
}
