public class Valid0408 {
    private int value;
    
    public Valid0408(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0408 obj = new Valid0408(42);
        System.out.println("Value: " + obj.getValue());
    }
}
