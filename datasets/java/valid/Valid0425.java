public class Valid0425 {
    private int value;
    
    public Valid0425(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0425 obj = new Valid0425(42);
        System.out.println("Value: " + obj.getValue());
    }
}
