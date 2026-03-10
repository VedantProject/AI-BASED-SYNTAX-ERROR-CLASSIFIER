public class Valid0038 {
    private int value;
    
    public Valid0038(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0038 obj = new Valid0038(42);
        System.out.println("Value: " + obj.getValue());
    }
}
