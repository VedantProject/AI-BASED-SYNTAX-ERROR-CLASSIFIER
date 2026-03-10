public class Valid0368 {
    private int value;
    
    public Valid0368(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0368 obj = new Valid0368(42);
        System.out.println("Value: " + obj.getValue());
    }
}
