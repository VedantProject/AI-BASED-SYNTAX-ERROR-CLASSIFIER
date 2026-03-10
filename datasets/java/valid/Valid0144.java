public class Valid0144 {
    private int value;
    
    public Valid0144(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0144 obj = new Valid0144(42);
        System.out.println("Value: " + obj.getValue());
    }
}
