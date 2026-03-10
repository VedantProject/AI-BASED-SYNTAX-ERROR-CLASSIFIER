public class Valid0480 {
    private int value;
    
    public Valid0480(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0480 obj = new Valid0480(42);
        System.out.println("Value: " + obj.getValue());
    }
}
