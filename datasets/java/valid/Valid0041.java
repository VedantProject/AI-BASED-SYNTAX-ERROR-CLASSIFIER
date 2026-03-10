public class Valid0041 {
    private int value;
    
    public Valid0041(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0041 obj = new Valid0041(42);
        System.out.println("Value: " + obj.getValue());
    }
}
