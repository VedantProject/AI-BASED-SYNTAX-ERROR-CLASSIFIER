public class Valid0092 {
    private int value;
    
    public Valid0092(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0092 obj = new Valid0092(42);
        System.out.println("Value: " + obj.getValue());
    }
}
