public class Valid0329 {
    private int value;
    
    public Valid0329(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0329 obj = new Valid0329(42);
        System.out.println("Value: " + obj.getValue());
    }
}
