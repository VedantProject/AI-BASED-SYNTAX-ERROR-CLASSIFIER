public class Valid0387 {
    private int value;
    
    public Valid0387(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0387 obj = new Valid0387(42);
        System.out.println("Value: " + obj.getValue());
    }
}
