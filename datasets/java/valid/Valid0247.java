public class Valid0247 {
    private int value;
    
    public Valid0247(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0247 obj = new Valid0247(42);
        System.out.println("Value: " + obj.getValue());
    }
}
