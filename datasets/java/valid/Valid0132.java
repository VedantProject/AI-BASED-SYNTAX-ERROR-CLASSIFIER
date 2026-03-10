public class Valid0132 {
    private int value;
    
    public Valid0132(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0132 obj = new Valid0132(42);
        System.out.println("Value: " + obj.getValue());
    }
}
