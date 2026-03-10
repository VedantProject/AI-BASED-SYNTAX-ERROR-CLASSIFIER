public class Valid0291 {
    private int value;
    
    public Valid0291(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0291 obj = new Valid0291(42);
        System.out.println("Value: " + obj.getValue());
    }
}
