// 1. The Complex Product
class GamingSetup {
    private String monitor;
    private String keyboard;
    private String mouse;

    public void setMonitor(String monitor) { this.monitor = monitor; }
    public void setKeyboard(String keyboard) { this.keyboard = keyboard; }
    public void setMouse(String mouse) { this.mouse = mouse; }

    public void displaySetup() {
        System.out.println("Gaming Setup Contains: ");
        System.out.println(" - Monitor: " + monitor);
        System.out.println(" - Keyboard: " + keyboard);
        System.out.println(" - Mouse: " + mouse);
    }
}

// 2. The Builder Interface
interface SetupBuilder {
    void buildMonitor();
    void buildKeyboard();
    void buildMouse();
    GamingSetup getSetup();
}

// 3. Concrete Builders
class CompetitiveSetupBuilder implements SetupBuilder {
    private GamingSetup setup = new GamingSetup();

    public void buildMonitor() { setup.setMonitor("240 Hz Monitor"); }
    public void buildKeyboard() { setup.setKeyboard("Mechanical Keyboard"); }
    public void buildMouse() { setup.setMouse("Lightweight Mouse"); }
    public GamingSetup getSetup() { return setup; }
}

class CasualSetupBuilder implements SetupBuilder {
    private GamingSetup setup = new GamingSetup();

    public void buildMonitor() { setup.setMonitor("Standard Monitor"); }
    public void buildKeyboard() { setup.setKeyboard("Wireless Keyboard"); }
    public void buildMouse() { setup.setMouse("Wireless Mouse"); }
    public GamingSetup getSetup() { return setup; }
}

// 4. The Director (Controls Construction Process)
class SetupDirector {
    // Ensures components are added in the requested order: Monitor -> Keyboard -> Mouse
    public GamingSetup constructSetup(SetupBuilder builder) {
        builder.buildMonitor();
        builder.buildKeyboard();
        builder.buildMouse();
        return builder.getSetup();
    }
}

// Client Demonstration
public class BuilderDemo {
    public static void main(String[] args) {
        SetupDirector director = new SetupDirector();

        System.out.println("--- Building Competitive Setup ---");
        SetupBuilder competitiveBuilder = new CompetitiveSetupBuilder();
        GamingSetup competitiveSetup = director.constructSetup(competitiveBuilder);
        competitiveSetup.displaySetup();

        System.out.println("\n--- Building Casual Setup ---");
        SetupBuilder casualBuilder = new CasualSetupBuilder();
        GamingSetup casualSetup = director.constructSetup(casualBuilder);
        casualSetup.displaySetup();
    }
}
