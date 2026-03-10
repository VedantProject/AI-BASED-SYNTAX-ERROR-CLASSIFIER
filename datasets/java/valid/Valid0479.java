public class Valid0479 {
    private int value;
    
    public Valid0479(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0479 obj = new Valid0479(42);
        System.out.println("Value: " + obj.getValue());
    }
}
