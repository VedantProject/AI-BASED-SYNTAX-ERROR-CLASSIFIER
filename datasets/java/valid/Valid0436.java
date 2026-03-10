public class Valid0436 {
    private int value;
    
    public Valid0436(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0436 obj = new Valid0436(42);
        System.out.println("Value: " + obj.getValue());
    }
}
