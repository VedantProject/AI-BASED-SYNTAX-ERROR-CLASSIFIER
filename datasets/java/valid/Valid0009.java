public class Valid0009 {
    private int value;
    
    public Valid0009(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0009 obj = new Valid0009(42);
        System.out.println("Value: " + obj.getValue());
    }
}
