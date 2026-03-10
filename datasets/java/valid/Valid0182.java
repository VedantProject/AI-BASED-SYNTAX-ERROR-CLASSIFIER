public class Valid0182 {
    private int value;
    
    public Valid0182(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0182 obj = new Valid0182(42);
        System.out.println("Value: " + obj.getValue());
    }
}
