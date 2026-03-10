public class Valid0040 {
    private int value;
    
    public Valid0040(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0040 obj = new Valid0040(42);
        System.out.println("Value: " + obj.getValue());
    }
}
