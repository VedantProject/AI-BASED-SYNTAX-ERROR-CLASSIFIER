public class Valid0063 {
    private int value;
    
    public Valid0063(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0063 obj = new Valid0063(42);
        System.out.println("Value: " + obj.getValue());
    }
}
