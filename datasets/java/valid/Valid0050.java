public class Valid0050 {
    private int value;
    
    public Valid0050(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0050 obj = new Valid0050(42);
        System.out.println("Value: " + obj.getValue());
    }
}
