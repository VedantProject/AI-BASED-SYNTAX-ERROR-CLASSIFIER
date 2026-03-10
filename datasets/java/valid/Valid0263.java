public class Valid0263 {
    private int value;
    
    public Valid0263(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0263 obj = new Valid0263(42);
        System.out.println("Value: " + obj.getValue());
    }
}
