public class Valid0315 {
    private int value;
    
    public Valid0315(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0315 obj = new Valid0315(42);
        System.out.println("Value: " + obj.getValue());
    }
}
