public class Valid0490 {
    private int value;
    
    public Valid0490(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0490 obj = new Valid0490(42);
        System.out.println("Value: " + obj.getValue());
    }
}
