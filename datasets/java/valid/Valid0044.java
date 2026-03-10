public class Valid0044 {
    private int value;
    
    public Valid0044(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0044 obj = new Valid0044(42);
        System.out.println("Value: " + obj.getValue());
    }
}
