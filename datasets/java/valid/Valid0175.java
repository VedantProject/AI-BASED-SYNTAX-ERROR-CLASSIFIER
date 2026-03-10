public class Valid0175 {
    private int value;
    
    public Valid0175(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0175 obj = new Valid0175(42);
        System.out.println("Value: " + obj.getValue());
    }
}
