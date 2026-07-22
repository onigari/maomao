// --- 1. Component Interfaces ---
interface Button { void render(); }
interface TextField { void render(); }
interface DialogBox { void render(); }

// --- 2. Concrete Components (Light Theme) ---
class LightButton implements Button { 
    public void render() { System.out.println("Rendering Light Button"); } 
}
class LightTextField implements TextField { 
    public void render() { System.out.println("Rendering Light TextField"); } 
}
class LightDialog implements DialogBox { 
    public void render() { System.out.println("Rendering Light Dialog Box"); } 
}

// --- 3. Concrete Components (Dark Theme) ---
class DarkButton implements Button { 
    public void render() { System.out.println("Rendering Dark Button"); } 
}
class DarkTextField implements TextField { 
    public void render() { System.out.println("Rendering Dark TextField"); } 
}
class DarkDialog implements DialogBox { 
    public void render() { System.out.println("Rendering Dark Dialog Box"); } 
}

// --- 4. Abstract Factory ---
interface GUIFactory {
    Button createButton();
    TextField createTextField();
    DialogBox createDialogBox();
}

// --- 5. Concrete Factories ---
class LightThemeFactory implements GUIFactory {
    public Button createButton() { return new LightButton(); }
    public TextField createTextField() { return new LightTextField(); }
    public DialogBox createDialogBox() { return new LightDialog(); }
}

class DarkThemeFactory implements GUIFactory {
    public Button createButton() { return new DarkButton(); }
    public TextField createTextField() { return new DarkTextField(); }
    public DialogBox createDialogBox() { return new DarkDialog(); }
}

// --- 6. Client Application ---
class Application {
    private Button button;
    private TextField textField;
    private DialogBox dialogBox;

    // The client accepts any factory and gets the right family of components
    public Application(GUIFactory factory) {
        button = factory.createButton();
        textField = factory.createTextField();
        dialogBox = factory.createDialogBox();
    }

    public void renderUI() {
        button.render();
        textField.render();
        dialogBox.render();
    }
}

// Client Demonstration
public class AbstractFactoryDemo {
    public static void main(String[] args) {
        System.out.println("--- Loading Light Theme ---");
        GUIFactory lightFactory = new LightThemeFactory();
        Application app1 = new Application(lightFactory);
        app1.renderUI();

        System.out.println("\n--- Switching to Dark Theme ---");
        GUIFactory darkFactory = new DarkThemeFactory();
        Application app2 = new Application(darkFactory);
        app2.renderUI();
    }
}
