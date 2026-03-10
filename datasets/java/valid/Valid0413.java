public class Valid0413 {
    private int value;
    
    public Valid0413(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0413 obj = new Valid0413(42);
        System.out.println("Value: " + obj.getValue());
    }
}
