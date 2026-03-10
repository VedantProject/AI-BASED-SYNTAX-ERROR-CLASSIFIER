public class Valid0103 {
    private int value;
    
    public Valid0103(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0103 obj = new Valid0103(42);
        System.out.println("Value: " + obj.getValue());
    }
}
