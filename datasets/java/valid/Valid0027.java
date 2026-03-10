public class Valid0027 {
    private int value;
    
    public Valid0027(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0027 obj = new Valid0027(42);
        System.out.println("Value: " + obj.getValue());
    }
}
