public class Valid0456 {
    private int value;
    
    public Valid0456(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0456 obj = new Valid0456(42);
        System.out.println("Value: " + obj.getValue());
    }
}
