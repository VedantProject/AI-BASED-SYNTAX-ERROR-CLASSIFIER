public class Valid0244 {
    private int value;
    
    public Valid0244(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0244 obj = new Valid0244(42);
        System.out.println("Value: " + obj.getValue());
    }
}
