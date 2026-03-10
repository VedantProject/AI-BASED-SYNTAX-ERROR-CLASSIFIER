public class Valid0134 {
    private int value;
    
    public Valid0134(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0134 obj = new Valid0134(42);
        System.out.println("Value: " + obj.getValue());
    }
}
