
public class Mediator1 {

    public static void main(String[] args) {
        LoginDialog dialog = new LoginDialog();
        Checkbox cb = new Checkbox(dialog);
        Textbox tb = new Textbox(dialog);
        Button btn = new Button(dialog, "login");
        dialog.setComponents(cb, tb, btn);

        cb.toggle();
        btn.click();
    }
}

interface DialogMediator {

    void notify(Component sender, String event);
}

abstract class Component {

    protected DialogMediator mediator;

    public Component(DialogMediator mediator) {
        this.mediator = mediator;
    }

    public void click() {
        mediator.notify(this, "click");
    }
}

class Button extends Component {

    private String label;

    public Button(DialogMediator m, String label) {
        super(m);
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}

class Checkbox extends Component {

    private boolean checked = false;

    public Checkbox(DialogMediator m) {
        super(m);
    }

    public void toggle() {
        checked = !checked;
        mediator.notify(this, "check");
    }

    public boolean isChecked() {
        return checked;
    }
}

class Textbox extends Component {

    private boolean enabled = true;

    public Textbox(DialogMediator m) {
        super(m);
    }

    public void setEnabled(boolean e) {
        this.enabled = e;
    }

    public boolean isEnabled() {
        return enabled;
    }
}

class LoginDialog implements DialogMediator {

    private Checkbox rememberMe;
    private Textbox password;
    private Button login;

    public void setComponents(Checkbox cb, Textbox tb, Button btn) {
        this.rememberMe = cb;
        this.password = tb;
        this.login = btn;
    }

    @Override
    public void notify(Component sender, String event) {
        if (sender == rememberMe && event.equals("check")) {
            password.setEnabled(!rememberMe.isChecked());
            System.out.println("Password field " + (rememberMe.isChecked() ? "disabled" : "enabled"));
        }

        if (sender == login && event.equals("click")) {
            System.out.println("Login button clicked - validating,,,");

        }

    }

}
