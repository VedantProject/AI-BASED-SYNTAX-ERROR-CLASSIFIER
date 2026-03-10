public class Valid0498 {
    private int value;
    
    public Valid0498(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0498 obj = new Valid0498(42);
        System.out.println("Value: " + obj.getValue());
    }
}
