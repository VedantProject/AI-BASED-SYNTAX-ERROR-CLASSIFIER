public class Valid0088 {
    private int value;
    
    public Valid0088(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0088 obj = new Valid0088(42);
        System.out.println("Value: " + obj.getValue());
    }
}
