public class Valid0349 {
    private int value;
    
    public Valid0349(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0349 obj = new Valid0349(42);
        System.out.println("Value: " + obj.getValue());
    }
}
