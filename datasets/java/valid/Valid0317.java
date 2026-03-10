public class Valid0317 {
    private int value;
    
    public Valid0317(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0317 obj = new Valid0317(42);
        System.out.println("Value: " + obj.getValue());
    }
}
