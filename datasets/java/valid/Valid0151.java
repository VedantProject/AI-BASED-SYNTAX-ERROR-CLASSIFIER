public class Valid0151 {
    private int value;
    
    public Valid0151(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0151 obj = new Valid0151(42);
        System.out.println("Value: " + obj.getValue());
    }
}
