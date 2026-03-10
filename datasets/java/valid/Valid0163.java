public class Valid0163 {
    public static int max(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    public static void main(String[] args) {
        System.out.println("Max: " + max(10, 20));
    }
}
