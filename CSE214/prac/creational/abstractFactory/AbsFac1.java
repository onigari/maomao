
public class AbsFac1 {
    public static void main(String[] args) {
        Application WinApp = new Application(new WinFactory());
        WinApp.render();

        Application MacApp = new Application(new MacFactory());
        MacApp.render();
    }
}

class Application {
    private Button button;
    private Checkbox checkbox;

    public Application(GUIFactory factory) {
        button = factory.createButton();
        checkbox = factory.createCheckbox();
    }

    public void render() {
        button.render();
        checkbox.render();
    }
}

interface Button { void render(); }
interface Checkbox { void render(); }

class WinButton implements Button {
    @Override
    public void render() {
        System.out.println("Windows Button");
        
    }
}

class MacButton implements Button {

    @Override
    public void render() {
        System.out.println("Mac Button");
        
    }
    
}

class WinCheckbox implements Checkbox {
    @Override
    public void render() {
        System.out.println("Windows Checkbox");
        
    }
}

class MacCheckbox implements Checkbox {

    @Override
    public void render() {
        System.out.println("Mac Checkbox");
        
    }
    
}

interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

class WinFactory implements GUIFactory {

    @Override
    public Button createButton() {
        return new WinButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new WinCheckbox();
    }
}

class MacFactory implements GUIFactory {

    @Override
    public Button createButton() {
        return new MacButton();
    }

    @Override
    public Checkbox createCheckbox() {
        return new MacCheckbox();
    }
    
}