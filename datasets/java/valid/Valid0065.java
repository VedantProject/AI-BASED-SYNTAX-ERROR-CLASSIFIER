public class Valid0065 {
    private int value;
    
    public Valid0065(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0065 obj = new Valid0065(42);
        System.out.println("Value: " + obj.getValue());
    }
}
