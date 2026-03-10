public class Valid0272 {
    private int value;
    
    public Valid0272(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0272 obj = new Valid0272(42);
        System.out.println("Value: " + obj.getValue());
    }
}
