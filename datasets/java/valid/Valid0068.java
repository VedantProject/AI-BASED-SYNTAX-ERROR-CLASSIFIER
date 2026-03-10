public class Valid0068 {
    private int value;
    
    public Valid0068(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0068 obj = new Valid0068(42);
        System.out.println("Value: " + obj.getValue());
    }
}
