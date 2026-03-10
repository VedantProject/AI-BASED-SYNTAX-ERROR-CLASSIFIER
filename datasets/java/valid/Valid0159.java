public class Valid0159 {
    private int value;
    
    public Valid0159(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0159 obj = new Valid0159(42);
        System.out.println("Value: " + obj.getValue());
    }
}
