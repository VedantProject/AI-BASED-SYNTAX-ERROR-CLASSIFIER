public class Valid0293 {
    private int value;
    
    public Valid0293(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0293 obj = new Valid0293(42);
        System.out.println("Value: " + obj.getValue());
    }
}
