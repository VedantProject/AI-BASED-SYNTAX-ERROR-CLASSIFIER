public class Valid0481 {
    private int value;
    
    public Valid0481(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0481 obj = new Valid0481(42);
        System.out.println("Value: " + obj.getValue());
    }
}
