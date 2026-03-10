public class Valid0110 {
    private int value;
    
    public Valid0110(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0110 obj = new Valid0110(42);
        System.out.println("Value: " + obj.getValue());
    }
}
