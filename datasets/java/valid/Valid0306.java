public class Valid0306 {
    private int value;
    
    public Valid0306(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0306 obj = new Valid0306(42);
        System.out.println("Value: " + obj.getValue());
    }
}
