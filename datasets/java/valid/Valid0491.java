public class Valid0491 {
    private int value;
    
    public Valid0491(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0491 obj = new Valid0491(42);
        System.out.println("Value: " + obj.getValue());
    }
}
