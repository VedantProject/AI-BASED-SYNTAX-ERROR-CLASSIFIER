public class Valid0340 {
    private int value;
    
    public Valid0340(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0340 obj = new Valid0340(42);
        System.out.println("Value: " + obj.getValue());
    }
}
