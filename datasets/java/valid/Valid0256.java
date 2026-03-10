public class Valid0256 {
    private int value;
    
    public Valid0256(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0256 obj = new Valid0256(42);
        System.out.println("Value: " + obj.getValue());
    }
}
