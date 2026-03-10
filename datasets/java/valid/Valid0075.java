public class Valid0075 {
    private int value;
    
    public Valid0075(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0075 obj = new Valid0075(42);
        System.out.println("Value: " + obj.getValue());
    }
}
