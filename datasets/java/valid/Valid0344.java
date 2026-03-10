public class Valid0344 {
    private int value;
    
    public Valid0344(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0344 obj = new Valid0344(42);
        System.out.println("Value: " + obj.getValue());
    }
}
