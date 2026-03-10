public class Valid0227 {
    private int value;
    
    public Valid0227(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0227 obj = new Valid0227(42);
        System.out.println("Value: " + obj.getValue());
    }
}
