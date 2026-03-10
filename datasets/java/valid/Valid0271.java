public class Valid0271 {
    private int value;
    
    public Valid0271(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0271 obj = new Valid0271(42);
        System.out.println("Value: " + obj.getValue());
    }
}
