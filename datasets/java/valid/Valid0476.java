public class Valid0476 {
    private int value;
    
    public Valid0476(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0476 obj = new Valid0476(42);
        System.out.println("Value: " + obj.getValue());
    }
}
