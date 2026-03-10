public class Valid0012 {
    private int value;
    
    public Valid0012(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0012 obj = new Valid0012(42);
        System.out.println("Value: " + obj.getValue());
    }
}
