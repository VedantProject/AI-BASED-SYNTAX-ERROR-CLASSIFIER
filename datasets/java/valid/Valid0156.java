public class Valid0156 {
    private int value;
    
    public Valid0156(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0156 obj = new Valid0156(42);
        System.out.println("Value: " + obj.getValue());
    }
}
