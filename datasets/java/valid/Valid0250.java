public class Valid0250 {
    private int value;
    
    public Valid0250(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0250 obj = new Valid0250(42);
        System.out.println("Value: " + obj.getValue());
    }
}
