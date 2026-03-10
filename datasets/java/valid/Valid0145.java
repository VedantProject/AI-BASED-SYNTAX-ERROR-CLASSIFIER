public class Valid0145 {
    private int value;
    
    public Valid0145(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0145 obj = new Valid0145(42);
        System.out.println("Value: " + obj.getValue());
    }
}
