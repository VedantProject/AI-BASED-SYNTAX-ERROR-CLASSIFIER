public class Valid0422 {
    private int value;
    
    public Valid0422(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0422 obj = new Valid0422(42);
        System.out.println("Value: " + obj.getValue());
    }
}
