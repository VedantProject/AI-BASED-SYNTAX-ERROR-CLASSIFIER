public class Valid0401 {
    private int value;
    
    public Valid0401(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0401 obj = new Valid0401(42);
        System.out.println("Value: " + obj.getValue());
    }
}
