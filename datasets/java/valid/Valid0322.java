public class Valid0322 {
    private int value;
    
    public Valid0322(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0322 obj = new Valid0322(42);
        System.out.println("Value: " + obj.getValue());
    }
}
