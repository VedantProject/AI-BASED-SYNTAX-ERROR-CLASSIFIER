public class Valid0212 {
    private int value;
    
    public Valid0212(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0212 obj = new Valid0212(42);
        System.out.println("Value: " + obj.getValue());
    }
}
