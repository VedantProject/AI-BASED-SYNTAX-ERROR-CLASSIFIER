public class Valid0205 {
    private int value;
    
    public Valid0205(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0205 obj = new Valid0205(42);
        System.out.println("Value: " + obj.getValue());
    }
}
