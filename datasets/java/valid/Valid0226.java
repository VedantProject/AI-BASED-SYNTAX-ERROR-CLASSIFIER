public class Valid0226 {
    private int value;
    
    public Valid0226(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0226 obj = new Valid0226(42);
        System.out.println("Value: " + obj.getValue());
    }
}
