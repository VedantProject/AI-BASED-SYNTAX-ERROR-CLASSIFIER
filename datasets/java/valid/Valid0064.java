public class Valid0064 {
    private int value;
    
    public Valid0064(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0064 obj = new Valid0064(42);
        System.out.println("Value: " + obj.getValue());
    }
}
