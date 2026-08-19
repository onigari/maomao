
public class State1 {

    public static void main(String[] args) {
        TrafficLight light = new TrafficLight();
        light.change();
        light.change();
        light.change();
    }
}

interface TrafficLightState {

    void handle(TrafficLight context);

    String getColor();
}

class RedState implements TrafficLightState {

    @Override
    public void handle(TrafficLight context) {
        System.out.println("RED");
        context.setState(new GreenState());
    }

    @Override
    public String getColor() {
        return "RED";
    }
}

class GreenState implements TrafficLightState {

    @Override
    public void handle(TrafficLight context) {
        System.out.println("GREEN");
        context.setState(new YellowState());
    }

    @Override
    public String getColor() {
        return "GREEN";
    }
}

class YellowState implements TrafficLightState {

    @Override
    public void handle(TrafficLight context) {
        System.out.println("YELLOW");
        context.setState(new RedState());
    }

    @Override
    public String getColor() {
        return "YELLOW";
    }
}

class TrafficLight {

    private TrafficLightState state;

    public TrafficLight() {
        this.state = new RedState();
    }

    public TrafficLight(TrafficLightState state) {
        this.state = state;
    }

    public void setState(TrafficLightState state) {
        this.state = state;
    }

    public TrafficLightState getState() {
        return state;
    }

    public void change() {
        state.handle(this);
    }
}
