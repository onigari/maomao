public class Singleton {
    private static Singleton instance;

    private Singleton() {
        System.out.println("Constructor");
        
    }

    public static synchronized Singleton getInstance() {
        if (instance == null) instance = new Singleton();
        return instance;
    }
}