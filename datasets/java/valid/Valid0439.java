public class Valid0439 {
    private int value;
    
    public Valid0439(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0439 obj = new Valid0439(42);
        System.out.println("Value: " + obj.getValue());
    }
}
