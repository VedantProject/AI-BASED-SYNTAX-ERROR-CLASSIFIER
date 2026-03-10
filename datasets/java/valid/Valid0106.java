public class Valid0106 {
    private int value;
    
    public Valid0106(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0106 obj = new Valid0106(42);
        System.out.println("Value: " + obj.getValue());
    }
}
