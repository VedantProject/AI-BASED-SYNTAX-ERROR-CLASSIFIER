public class Valid0446 {
    private int value;
    
    public Valid0446(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0446 obj = new Valid0446(42);
        System.out.println("Value: " + obj.getValue());
    }
}
