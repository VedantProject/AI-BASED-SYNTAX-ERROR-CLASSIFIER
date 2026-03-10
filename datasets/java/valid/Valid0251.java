public class Valid0251 {
    private int value;
    
    public Valid0251(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0251 obj = new Valid0251(42);
        System.out.println("Value: " + obj.getValue());
    }
}
