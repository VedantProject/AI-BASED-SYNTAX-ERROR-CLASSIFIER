public class Valid0398 {
    private int value;
    
    public Valid0398(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0398 obj = new Valid0398(42);
        System.out.println("Value: " + obj.getValue());
    }
}
