public class Valid0384 {
    private int value;
    
    public Valid0384(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0384 obj = new Valid0384(42);
        System.out.println("Value: " + obj.getValue());
    }
}
