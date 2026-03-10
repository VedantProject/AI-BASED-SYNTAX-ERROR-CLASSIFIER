public class Valid0496 {
    private int value;
    
    public Valid0496(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0496 obj = new Valid0496(42);
        System.out.println("Value: " + obj.getValue());
    }
}
