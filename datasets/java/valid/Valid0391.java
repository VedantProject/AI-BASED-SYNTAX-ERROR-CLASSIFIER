public class Valid0391 {
    private int value;
    
    public Valid0391(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        Valid0391 obj = new Valid0391(42);
        System.out.println("Value: " + obj.getValue());
    }
}
