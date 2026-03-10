public class Valid0261 {
    private int value;
    
    public Valid0261(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0261 obj = new Valid0261(42);
        System.out.println("Value: " + obj.getValue());
    }
}
