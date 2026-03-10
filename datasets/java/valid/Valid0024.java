public class Valid0024 {
    private int value;
    
    public Valid0024(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0024 obj = new Valid0024(42);
        System.out.println("Value: " + obj.getValue());
    }
}
