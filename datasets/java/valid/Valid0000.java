public class Valid0000 {
    private int value;
    
    public Valid0000(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0000 obj = new Valid0000(42);
        System.out.println("Value: " + obj.getValue());
    }
}
