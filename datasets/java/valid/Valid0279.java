public class Valid0279 {
    private int value;
    
    public Valid0279(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0279 obj = new Valid0279(42);
        System.out.println("Value: " + obj.getValue());
    }
}
