public class Valid0099 {
    private int value;
    
    public Valid0099(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0099 obj = new Valid0099(42);
        System.out.println("Value: " + obj.getValue());
    }
}
