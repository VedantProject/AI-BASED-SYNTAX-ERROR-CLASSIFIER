public class Valid0152 {
    private int value;
    
    public Valid0152(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0152 obj = new Valid0152(42);
        System.out.println("Value: " + obj.getValue());
    }
}
