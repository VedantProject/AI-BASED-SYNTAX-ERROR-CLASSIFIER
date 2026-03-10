public class Valid0189 {
    private int value;
    
    public Valid0189(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0189 obj = new Valid0189(42);
        System.out.println("Value: " + obj.getValue());
    }
}
