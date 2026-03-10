public class Valid0286 {
    private int value;
    
    public Valid0286(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0286 obj = new Valid0286(42);
        System.out.println("Value: " + obj.getValue());
    }
}
