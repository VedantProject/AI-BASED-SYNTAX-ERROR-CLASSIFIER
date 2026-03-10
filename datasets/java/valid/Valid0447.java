public class Valid0447 {
    private int value;
    
    public Valid0447(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0447 obj = new Valid0447(42);
        System.out.println("Value: " + obj.getValue());
    }
}
