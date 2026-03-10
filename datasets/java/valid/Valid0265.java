public class Valid0265 {
    private int value;
    
    public Valid0265(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0265 obj = new Valid0265(42);
        System.out.println("Value: " + obj.getValue());
    }
}
