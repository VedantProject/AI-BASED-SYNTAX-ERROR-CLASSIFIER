public class Valid0376 {
    private int value;
    
    public Valid0376(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0376 obj = new Valid0376(42);
        System.out.println("Value: " + obj.getValue());
    }
}
