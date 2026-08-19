
public class DBPool {
    public static void main(String[] args) {
        DatabasePool dbpool1 = DatabasePool.getInstance();
        DatabasePool dbpool2 = DatabasePool.getInstance();
        System.out.println(dbpool1==dbpool2);
    }
}

class DatabasePool {
    private static DatabasePool instance;

    private DatabasePool() {
        System.out.println("Connecting to database...");
    }

    public static synchronized DatabasePool getInstance() {
        if(instance == null) instance = new DatabasePool();
        return instance;
    }

    /* extra altufaltu methods */
    public void query(String sql) {
        System.out.println("Running SQL: " + sql);
    }
}