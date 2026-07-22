// The Singleton Class
class AuditLogger {
    // 1. Static variable to hold the single instance
    private static AuditLogger instance;

    // 2. Private constructor prevents direct instantiation from client classes
    private AuditLogger() {
        System.out.println("AuditLogger instance created for the first time.");
    }

    // 3. Public static method to provide global access to the instance
    public static AuditLogger getInstance() {
        if (instance == null) {
            instance = new AuditLogger(); // Created only when requested
        }
        return instance;
    }

    public void logMessage(String message) {
        System.out.println("[AUDIT LOG]: " + message);
    }
}

// Client Demonstration
public class SingletonDemo {
    public static void main(String[] args) {
        // Module 1 requests the logger
        System.out.println("Module 1 requesting logger...");
        AuditLogger module1Logger = AuditLogger.getInstance();
        module1Logger.logMessage("Student Login processed.");

        // Module 2 requests the logger
        System.out.println("\nModule 2 requesting logger...");
        AuditLogger module2Logger = AuditLogger.getInstance();
        module2Logger.logMessage("Result Processing completed.");

        // Demonstrate both modules received the SAME instance
        System.out.println("\nVerification:");
        if (module1Logger == module2Logger) {
            System.out.println("Success! Both modules are using the exact same AuditLogger instance.");
        }
    }
}
